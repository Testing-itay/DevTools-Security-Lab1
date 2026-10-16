
"""MCP Server: Dependency Analyzer — Analyze project dependencies and detect issues."""
import argparse
import json
import re
import sys
from pathlib import Path

MANIFEST_PARSERS = {
    "requirements.txt": "python",
    "package.json": "node",
    "go.mod": "go",
    "Cargo.toml": "rust",
    "pom.xml": "java",
}


def parse_requirements(content: str) -> list[dict]:
    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = re.match(r"^([a-zA-Z0-9_.-]+)\s*([><=!~]+\s*[\d.]+)?", line)
        if match:
            deps.append({"name": match.group(1), "version": (match.group(2) or "").strip()})
    return deps


def parse_package_json(content: str) -> list[dict]:
    deps = []
    try:
        pkg = json.loads(content)
        for section in ("dependencies", "devDependencies"):
            for name, version in pkg.get(section, {}).items():
                deps.append({"name": name, "version": version})
    except json.JSONDecodeError:
        pass
    return deps


def find_manifests(root: str, max_depth: int = 3) -> dict[str, list[dict]]:
    results = {}
    root_path = Path(root)
    for path in root_path.rglob("*"):
        if path.name in MANIFEST_PARSERS:
            rel_depth = len(path.relative_to(root_path).parts)
            if rel_depth > max_depth:
                continue
            try:
                content = path.read_text()
            except OSError:
                continue
            if path.name == "requirements.txt":
                deps = parse_requirements(content)
            elif path.name == "package.json":
                deps = parse_package_json(content)
            else:
                deps = [{"name": path.name, "version": "unparsed"}]
            results[str(path)] = {"ecosystem": MANIFEST_PARSERS[path.name], "dependencies": deps}
    return results


def read_jsonrpc():
    header = sys.stdin.readline()
    while header.strip():
        header = sys.stdin.readline()
    content = sys.stdin.readline()
    return json.loads(content) if content.strip() else None


def write_jsonrpc(response):
    body = json.dumps(response)
    sys.stdout.write(f"Content-Length: {len(body)}\r\n\r\n{body}")
    sys.stdout.flush()


def handle_request(request: dict, scan_depth: int) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "dependency-analyzer", "version": "1.3.0"},
                "capabilities": {"tools": {}},
            },
        }

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "analyze_dependencies",
                        "description": "Scan project for dependency manifests and list all dependencies",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "default": "."},
                            },
                        },
                    },
                    {
                        "name": "check_outdated",
                        "description": "Check for outdated dependencies in a manifest file",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"manifest": {"type": "string"}},
                            "required": ["manifest"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"].get("arguments", {})

        if tool_name == "analyze_dependencies":
            manifests = find_manifests(args.get("path", "."), scan_depth)
            total = sum(len(m["dependencies"]) for m in manifests.values())
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({
                            "manifests_found": len(manifests),
                            "total_dependencies": total,
                            "details": manifests,
                        }, indent=2),
                    }]
                },
            }

        if tool_name == "check_outdated":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"status": "not_implemented_in_offline_mode"})}]
                },
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    parser = argparse.ArgumentParser(description="Dependency Analyzer MCP Server")
    parser.add_argument("--scan-depth", type=int, default=3, help="Maximum directory depth to scan")
    args = parser.parse_args()

    sys.stderr.write(f"[dependency-analyzer] Server started, scan depth={args.scan_depth}\n")
    while True:
        try:
            request = read_jsonrpc()
            if request is None:
                break
            response = handle_request(request, args.scan_depth)
            write_jsonrpc(response)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()

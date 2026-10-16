

"""MCP Server: Secret Scanner — Detect exposed credentials in source code."""
import json
import re
import sys
from pathlib import Path

PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "aws_secret_key": re.compile(r"(?i)aws_secret_access_key\s*[=:]\s*['\"]?([A-Za-z0-9/+=]{40})"),
    "github_token": re.compile(r"gh[ps]_[A-Za-z0-9_]{36,255}"),
    "generic_secret": re.compile(r"(?i)(password|secret|token|api_key)\s*[=:]\s*['\"][^\s'\"]{8,}"),
    "private_key": re.compile(r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----"),
    "jwt_token": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}"),
    "slack_webhook": re.compile(r"https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[A-Za-z0-9]+"),
    "connection_string": re.compile(r"(?i)(mongodb|postgres|mysql|redis)://[^\s'\"]+:[^\s'\"]+@"),
}

IGNORED_EXTENSIONS = {".png", ".jpg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".lock"}


def scan_file(filepath: Path) -> list[dict]:
    findings = []
    if filepath.suffix in IGNORED_EXTENSIONS:
        return findings
    try:
        content = filepath.read_text(errors="replace")
    except OSError:
        return findings

    for line_no, line in enumerate(content.splitlines(), start=1):
        for pattern_name, regex in PATTERNS.items():
            if regex.search(line):
                findings.append({
                    "file": str(filepath),
                    "line": line_no,
                    "pattern": pattern_name,
                    "severity": "critical" if pattern_name in {"private_key", "aws_secret_key"} else "high",
                    "snippet": line.strip()[:120],
                })
    return findings


def scan_directory(root: str) -> list[dict]:
    all_findings = []
    for path in Path(root).rglob("*"):
        if path.is_file():
            all_findings.extend(scan_file(path))
    return all_findings


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


def handle_request(request: dict) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "secret-scanner", "version": "2.0.1"},
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
                        "name": "scan_secrets",
                        "description": "Scan a directory for exposed secrets and credentials",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "Directory to scan", "default": "."},
                            },
                        },
                    },
                    {
                        "name": "check_file",
                        "description": "Check a single file for secrets",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"file": {"type": "string"}},
                            "required": ["file"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"].get("arguments", {})

        if tool_name == "scan_secrets":
            findings = scan_directory(args.get("path", "."))
            summary = f"Found {len(findings)} potential secret(s)"
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"summary": summary, "findings": findings}, indent=2)}]
                },
            }

        if tool_name == "check_file":
            findings = scan_file(Path(args["file"]))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(findings, indent=2)}]},
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    sys.stderr.write("[secret-scanner] Server started\n")
    while True:
        try:
            request = read_jsonrpc()
            if request is None:
                break
            response = handle_request(request)
            write_jsonrpc(response)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()

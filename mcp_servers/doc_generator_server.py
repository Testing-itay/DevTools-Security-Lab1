

"""MCP Server: Documentation Generator — Generate docs from source code."""
import argparse
import ast
import json
import sys
from pathlib import Path


def extract_python_docs(filepath: Path) -> list[dict]:
    docs = []
    try:
        tree = ast.parse(filepath.read_text())
    except (SyntaxError, OSError):
        return docs

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node)
            args = [arg.arg for arg in node.args.args if arg.arg != "self"]
            docs.append({
                "type": "function",
                "name": node.name,
                "line": node.lineno,
                "args": args,
                "docstring": doc or "",
                "is_async": isinstance(node, ast.AsyncFunctionDef),
            })
        elif isinstance(node, ast.ClassDef):
            doc = ast.get_docstring(node)
            methods = [
                n.name for n in node.body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
            ]
            docs.append({
                "type": "class",
                "name": node.name,
                "line": node.lineno,
                "methods": methods,
                "docstring": doc or "",
            })
    return docs


def generate_markdown(filepath: str, entities: list[dict]) -> str:
    lines = [f"# `{filepath}`\n"]
    for entity in entities:
        if entity["type"] == "class":
            lines.append(f"## Class `{entity['name']}` (line {entity['line']})")
            if entity["docstring"]:
                lines.append(f"\n{entity['docstring']}\n")
            if entity["methods"]:
                lines.append(f"**Methods:** {', '.join(entity['methods'])}\n")
        elif entity["type"] == "function":
            prefix = "async " if entity["is_async"] else ""
            sig = f"{prefix}{entity['name']}({', '.join(entity['args'])})"
            lines.append(f"### `{sig}` (line {entity['line']})")
            if entity["docstring"]:
                lines.append(f"\n{entity['docstring']}\n")
    return "\n".join(lines)


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


def handle_request(request: dict, output_dir: str) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "doc-generator", "version": "1.0.0"},
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
                        "name": "generate_docs",
                        "description": "Generate Markdown documentation from Python source files",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "File or directory to document"},
                            },
                            "required": ["path"],
                        },
                    },
                    {
                        "name": "extract_api",
                        "description": "Extract public API surface from a Python file",
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

        if tool_name == "generate_docs":
            target = Path(args["path"])
            results = {}
            files = [target] if target.is_file() else list(target.rglob("*.py"))
            for f in files:
                entities = extract_python_docs(f)
                if entities:
                    md = generate_markdown(str(f), entities)
                    results[str(f)] = md
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"files_documented": len(results), "docs": results}, indent=2)}]
                },
            }

        if tool_name == "extract_api":
            entities = extract_python_docs(Path(args["file"]))
            public = [e for e in entities if not e["name"].startswith("_")]
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(public, indent=2)}]},
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    parser = argparse.ArgumentParser(description="Documentation Generator MCP Server")
    parser.add_argument("--output", default="./docs", help="Output directory for generated docs")
    args = parser.parse_args()

    sys.stderr.write(f"[doc-generator] Server started, output to {args.output}\n")
    while True:
        try:
            request = read_jsonrpc()
            if request is None:
                break
            response = handle_request(request, args.output)
            write_jsonrpc(response)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()

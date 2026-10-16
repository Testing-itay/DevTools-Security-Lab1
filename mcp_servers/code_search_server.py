
"""MCP Server: Code Search — Semantic search over project files."""
import argparse
import json
import sys
import os
from pathlib import Path


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


def build_index(index_path: str) -> dict[str, list[str]]:
    file_index: dict[str, list[str]] = {}
    root = Path(index_path)
    if not root.exists():
        return file_index
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".py", ".ts", ".go", ".rs", ".java", ".cs"}:
            try:
                lines = path.read_text(errors="replace").splitlines()
                file_index[str(path)] = lines
            except OSError:
                continue
    return file_index


def search(index: dict[str, list[str]], query: str, max_results: int = 20) -> list[dict]:
    results = []
    query_lower = query.lower()
    for filepath, lines in index.items():
        for line_no, line in enumerate(lines, start=1):
            if query_lower in line.lower():
                results.append({
                    "file": filepath,
                    "line": line_no,
                    "content": line.strip(),
                })
                if len(results) >= max_results:
                    return results
    return results


def handle_request(request: dict, index: dict[str, list[str]]) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "code-search", "version": "1.2.0"},
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
                        "name": "search_code",
                        "description": "Search code across the project for a given query string",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"},
                                "maxResults": {"type": "integer", "default": 20},
                            },
                            "required": ["query"],
                        },
                    },
                    {
                        "name": "list_files",
                        "description": "List all indexed files",
                        "inputSchema": {"type": "object", "properties": {}},
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"].get("arguments", {})

        if tool_name == "search_code":
            matches = search(index, args["query"], args.get("maxResults", 20))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(matches, indent=2)}]},
            }

        if tool_name == "list_files":
            files = list(index.keys())
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(files, indent=2)}]},
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    parser = argparse.ArgumentParser(description="Code Search MCP Server")
    parser.add_argument("--index-path", default="./src", help="Root directory to index")
    args = parser.parse_args()

    index = build_index(args.index_path)
    sys.stderr.write(f"[code-search] Indexed {len(index)} files from {args.index_path}\n")

    while True:
        try:
            request = read_jsonrpc()
            if request is None:
                break
            response = handle_request(request, index)
            write_jsonrpc(response)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()

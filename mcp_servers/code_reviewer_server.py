


"""MCP Server: Code Reviewer — Automated code review with pattern-based checks."""
import json
import re
import sys
from pathlib import Path

REVIEW_RULES = {
    "no_hardcoded_secrets": {
        "pattern": r"(?i)(api_key|secret|password|token)\s*=\s*['\"][^'\"]{8,}",
        "severity": "critical",
        "message": "Potential hardcoded secret detected",
    },
    "no_print_statements": {
        "pattern": r"^\s*print\(",
        "severity": "warning",
        "message": "Debug print statement should be replaced with proper logging",
    },
    "no_todo_in_production": {
        "pattern": r"(?i)\b(TODO|FIXME|HACK|XXX)\b",
        "severity": "info",
        "message": "Unresolved TODO/FIXME comment",
    },
    "no_wildcard_imports": {
        "pattern": r"^from\s+\S+\s+import\s+\*",
        "severity": "warning",
        "message": "Wildcard import — prefer explicit imports",
    },
    "no_bare_except": {
        "pattern": r"^\s*except\s*:",
        "severity": "warning",
        "message": "Bare except clause — specify exception type",
    },
    "no_eval": {
        "pattern": r"\beval\s*\(",
        "severity": "critical",
        "message": "Use of eval() is a security risk",
    },
    "no_exec": {
        "pattern": r"\bexec\s*\(",
        "severity": "critical",
        "message": "Use of exec() is a security risk",
    },
    "no_shell_true": {
        "pattern": r"subprocess\.\w+\(.*shell\s*=\s*True",
        "severity": "high",
        "message": "subprocess with shell=True is a command injection risk",
    },
}


def review_file(filepath: Path) -> list[dict]:
    issues = []
    try:
        lines = filepath.read_text(errors="replace").splitlines()
    except OSError:
        return issues

    for line_no, line in enumerate(lines, start=1):
        for rule_name, rule in REVIEW_RULES.items():
            if re.search(rule["pattern"], line):
                issues.append({
                    "rule": rule_name,
                    "severity": rule["severity"],
                    "message": rule["message"],
                    "line": line_no,
                    "content": line.strip()[:100],
                })
    return issues


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
                "serverInfo": {"name": "code-reviewer", "version": "1.4.0"},
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
                        "name": "review_file",
                        "description": "Run automated code review checks on a file",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"file": {"type": "string"}},
                            "required": ["file"],
                        },
                    },
                    {
                        "name": "review_directory",
                        "description": "Review all source files in a directory",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "default": "."},
                                "extensions": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "default": [".py", ".ts", ".js"],
                                },
                            },
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"].get("arguments", {})

        if tool_name == "review_file":
            issues = review_file(Path(args["file"]))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({"file": args["file"], "issues": len(issues), "details": issues}, indent=2),
                    }]
                },
            }

        if tool_name == "review_directory":
            exts = set(args.get("extensions", [".py", ".ts", ".js"]))
            root = Path(args.get("path", "."))
            all_issues = {}
            for f in root.rglob("*"):
                if f.is_file() and f.suffix in exts:
                    issues = review_file(f)
                    if issues:
                        all_issues[str(f)] = issues
            total = sum(len(v) for v in all_issues.values())
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps({
                            "files_reviewed": len(all_issues),
                            "total_issues": total,
                            "by_file": {k: len(v) for k, v in all_issues.items()},
                        }, indent=2),
                    }]
                },
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    sys.stderr.write("[code-reviewer] Server started\n")
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

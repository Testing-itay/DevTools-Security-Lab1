

"""MCP Server: Test Runner — Execute and report on test suites."""
import argparse
import json
import subprocess
import sys


def run_tests(framework: str, path: str = ".", pattern: str = "") -> dict:
    if framework == "pytest":
        cmd = ["python", "-m", "pytest", path, "--tb=short", "-q"]
        if pattern:
            cmd.extend(["-k", pattern])
    elif framework == "jest":
        cmd = ["npx", "jest", "--passWithNoTests"]
        if pattern:
            cmd.extend(["--testPathPattern", pattern])
    elif framework == "go":
        cmd = ["go", "test", "./...", "-count=1"]
    else:
        return {"error": f"Unsupported framework: {framework}"}

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout[-5000:] if len(result.stdout) > 5000 else result.stdout,
            "stderr": result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr,
            "passed": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"error": "Test execution timed out after 300s"}
    except FileNotFoundError:
        return {"error": f"Framework command not found for {framework}"}


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


def handle_request(request: dict, default_framework: str) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "test-runner", "version": "1.1.0"},
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
                        "name": "run_tests",
                        "description": "Run test suite using the configured framework",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "default": "."},
                                "framework": {"type": "string", "enum": ["pytest", "jest", "go"]},
                                "pattern": {"type": "string", "description": "Test name filter pattern"},
                            },
                        },
                    },
                    {
                        "name": "run_single",
                        "description": "Run a single test file",
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

        if tool_name == "run_tests":
            framework = args.get("framework", default_framework)
            result = run_tests(framework, args.get("path", "."), args.get("pattern", ""))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
            }

        if tool_name == "run_single":
            result = run_tests(default_framework, args["file"])
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    parser = argparse.ArgumentParser(description="Test Runner MCP Server")
    parser.add_argument("--framework", default="pytest", choices=["pytest", "jest", "go"])
    args = parser.parse_args()

    sys.stderr.write(f"[test-runner] Server started, framework={args.framework}\n")
    while True:
        try:
            request = read_jsonrpc()
            if request is None:
                break
            response = handle_request(request, args.framework)
            write_jsonrpc(response)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()


"""MCP Server: Risk Scorer — Calculate security risk scores for code changes."""
import argparse
import json
import sys
from pathlib import Path

RISK_WEIGHTS = {
    "auth_change": 8.0,
    "crypto_usage": 7.0,
    "external_api": 6.0,
    "file_io": 4.0,
    "network_call": 5.0,
    "env_access": 6.5,
    "sql_query": 7.0,
    "deserialization": 7.5,
}

HIGH_RISK_PATTERNS = {
    "auth_change": ["password", "token", "session", "auth", "credential", "login", "oauth"],
    "crypto_usage": ["encrypt", "decrypt", "hash", "hmac", "cipher", "bcrypt", "argon"],
    "external_api": ["requests.get", "requests.post", "fetch(", "http.get", "urllib"],
    "file_io": ["open(", "readFile", "writeFile", "os.path", "shutil"],
    "network_call": ["socket", "connect", "listen", "bind"],
    "env_access": ["os.environ", "process.env", "getenv", "dotenv"],
    "sql_query": ["execute(", "cursor.", "SELECT ", "INSERT ", "UPDATE ", "DELETE "],
    "deserialization": ["pickle.load", "yaml.load", "json.loads", "deserialize", "unmarshal"],
}


def score_file(filepath: Path) -> dict:
    try:
        content = filepath.read_text(errors="replace").lower()
    except OSError:
        return {"file": str(filepath), "score": 0, "findings": []}

    findings = []
    total_score = 0.0

    for category, patterns in HIGH_RISK_PATTERNS.items():
        matches = sum(1 for p in patterns if p.lower() in content)
        if matches > 0:
            category_score = RISK_WEIGHTS[category] * min(matches, 5)
            total_score += category_score
            findings.append({
                "category": category,
                "matches": matches,
                "score": round(category_score, 1),
            })

    return {
        "file": str(filepath),
        "score": round(min(total_score, 100), 1),
        "risk_level": "critical" if total_score >= 50 else "high" if total_score >= 30 else "medium" if total_score >= 15 else "low",
        "findings": findings,
    }


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


def handle_request(request: dict, model_version: str) -> dict:
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "risk-scorer", "version": "2.1.0"},
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
                        "name": "score_risk",
                        "description": "Calculate a security risk score for a file or directory",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "File or directory to score"},
                            },
                            "required": ["path"],
                        },
                    },
                    {
                        "name": "score_diff",
                        "description": "Score risk of a git diff (changed lines only)",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "diff": {"type": "string", "description": "Git diff content"},
                            },
                            "required": ["diff"],
                        },
                    },
                ]
            },
        }

    if method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"].get("arguments", {})

        if tool_name == "score_risk":
            target = Path(args["path"])
            if target.is_file():
                result = score_file(target)
            else:
                files = list(target.rglob("*"))
                scores = [score_file(f) for f in files if f.is_file() and f.suffix in {".py", ".ts", ".js", ".go", ".rs", ".java", ".cs"}]
                avg = sum(s["score"] for s in scores) / max(len(scores), 1)
                result = {
                    "model_version": model_version,
                    "files_analyzed": len(scores),
                    "average_score": round(avg, 1),
                    "top_risks": sorted(scores, key=lambda s: s["score"], reverse=True)[:10],
                }
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]},
            }

        if tool_name == "score_diff":
            diff_content = args["diff"].lower()
            findings = []
            total = 0.0
            for category, patterns in HIGH_RISK_PATTERNS.items():
                matches = sum(1 for p in patterns if p.lower() in diff_content)
                if matches:
                    score = RISK_WEIGHTS[category] * matches
                    total += score
                    findings.append({"category": category, "matches": matches, "score": round(score, 1)})
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({
                        "total_score": round(min(total, 100), 1),
                        "findings": findings,
                    }, indent=2)}]
                },
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}


def main():
    parser = argparse.ArgumentParser(description="Risk Scorer MCP Server")
    parser.add_argument("--model", default="v2", help="Scoring model version")
    args = parser.parse_args()

    sys.stderr.write(f"[risk-scorer] Server started, model={args.model}\n")
    while True:
        try:
            request = read_jsonrpc()
            if request is None:
                break
            response = handle_request(request, args.model)
            write_jsonrpc(response)
        except (EOFError, KeyboardInterrupt):
            break


if __name__ == "__main__":
    main()

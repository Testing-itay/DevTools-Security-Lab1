
/**
 * MCP Server: Metrics Collector — Collect and expose project health metrics.
 */
const readline = require("readline");

const rl = readline.createInterface({ input: process.stdin });

const PORT = process.argv.includes("--port")
  ? process.argv[process.argv.indexOf("--port") + 1]
  : "9090";

function writeJsonRpc(response) {
  const body = JSON.stringify(response);
  process.stdout.write(`Content-Length: ${body.length}\r\n\r\n${body}`);
}

function collectCodeMetrics(path) {
  const fs = require("fs");
  const pathMod = require("path");

  const stats = { files: 0, lines: 0, byExtension: {} };
  const extensions = new Set([
    ".py",
    ".ts",
    ".js",
    ".go",
    ".rs",
    ".java",
    ".cs",
  ]);

  function walk(dir) {
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const full = pathMod.join(dir, entry.name);
        if (entry.name === "node_modules" || entry.name === ".git") continue;
        if (entry.isDirectory()) {
          walk(full);
        } else if (entry.isFile()) {
          const ext = pathMod.extname(entry.name);
          if (extensions.has(ext)) {
            stats.files++;
            try {
              const content = fs.readFileSync(full, "utf-8");
              const lineCount = content.split("\n").length;
              stats.lines += lineCount;
              stats.byExtension[ext] = (stats.byExtension[ext] || 0) + lineCount;
            } catch {}
          }
        }
      }
    } catch {}
  }

  walk(path || ".");
  return stats;
}

function handleRequest(request) {
  const { method, id, params } = request;

  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: "2024-11-05",
        serverInfo: { name: "metrics-collector", version: "1.0.0" },
        capabilities: { tools: {} },
      },
    };
  }

  if (method === "tools/list") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        tools: [
          {
            name: "collect_metrics",
            description: "Collect code metrics (file count, lines of code)",
            inputSchema: {
              type: "object",
              properties: {
                path: { type: "string", default: "." },
              },
            },
          },
          {
            name: "health_check",
            description: "Check project health indicators",
            inputSchema: { type: "object", properties: {} },
          },
        ],
      },
    };
  }

  if (method === "tools/call") {
    const toolName = params.name;
    const args = params.arguments || {};

    if (toolName === "collect_metrics") {
      const metrics = collectCodeMetrics(args.path);
      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [{ type: "text", text: JSON.stringify(metrics, null, 2) }],
        },
      };
    }

    if (toolName === "health_check") {
      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  status: "healthy",
                  metricsPort: PORT,
                  uptime: process.uptime(),
                },
                null,
                2
              ),
            },
          ],
        },
      };
    }
  }

  return {
    jsonrpc: "2.0",
    id,
    error: { code: -32601, message: "Method not found" },
  };
}

let buffer = "";

rl.on("line", (line) => {
  buffer += line + "\n";
  if (line.trim() === "") {
    rl.once("line", (content) => {
      try {
        const request = JSON.parse(content);
        const response = handleRequest(request);
        writeJsonRpc(response);
      } catch {}
      buffer = "";
    });
  }
});

process.stderr.write(`[metrics-collector] Server started on port ${PORT}\n`);

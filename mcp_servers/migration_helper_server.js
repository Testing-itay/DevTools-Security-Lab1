

/**
 * MCP Server: Migration Helper — Assist with database and schema migrations.
 */
const readline = require("readline");

const rl = readline.createInterface({ input: process.stdin });

function writeJsonRpc(response) {
  const body = JSON.stringify(response);
  process.stdout.write(`Content-Length: ${body.length}\r\n\r\n${body}`);
}

const MIGRATION_TEMPLATES = {
  postgres: {
    createTable: (name, columns) =>
      `CREATE TABLE IF NOT EXISTS ${name} (\n${columns
        .map((c) => `  ${c.name} ${c.type}${c.nullable === false ? " NOT NULL" : ""}${c.default ? ` DEFAULT ${c.default}` : ""}`)
        .join(",\n")}\n);`,
    addColumn: (table, column) =>
      `ALTER TABLE ${table} ADD COLUMN IF NOT EXISTS ${column.name} ${column.type};`,
    addIndex: (table, columns) =>
      `CREATE INDEX IF NOT EXISTS idx_${table}_${columns.join("_")} ON ${table} (${columns.join(", ")});`,
  },
  mongodb: {
    createCollection: (name) =>
      `db.createCollection("${name}")`,
    addIndex: (collection, fields) =>
      `db.${collection}.createIndex(${JSON.stringify(
        Object.fromEntries(fields.map((f) => [f, 1]))
      )})`,
  },
};

function handleRequest(request) {
  const { method, id, params } = request;

  if (method === "initialize") {
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion: "2024-11-05",
        serverInfo: { name: "migration-helper", version: "1.2.0" },
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
            name: "generate_migration",
            description:
              "Generate a database migration script for a schema change",
            inputSchema: {
              type: "object",
              properties: {
                database: {
                  type: "string",
                  enum: ["postgres", "mongodb"],
                },
                operation: {
                  type: "string",
                  enum: ["createTable", "addColumn", "addIndex", "createCollection"],
                },
                table: { type: "string" },
                columns: {
                  type: "array",
                  items: {
                    type: "object",
                    properties: {
                      name: { type: "string" },
                      type: { type: "string" },
                      nullable: { type: "boolean" },
                      default: { type: "string" },
                    },
                  },
                },
              },
              required: ["database", "operation"],
            },
          },
          {
            name: "validate_migration",
            description: "Validate a migration script for common issues",
            inputSchema: {
              type: "object",
              properties: {
                script: { type: "string" },
                database: { type: "string" },
              },
              required: ["script"],
            },
          },
        ],
      },
    };
  }

  if (method === "tools/call") {
    const toolName = params.name;
    const args = params.arguments || {};

    if (toolName === "generate_migration") {
      const { database, operation, table, columns } = args;
      const templates = MIGRATION_TEMPLATES[database];
      if (!templates) {
        return {
          jsonrpc: "2.0",
          id,
          result: {
            content: [
              {
                type: "text",
                text: JSON.stringify({ error: `Unsupported database: ${database}` }),
              },
            ],
          },
        };
      }

      let sql = "";
      if (operation === "createTable" && templates.createTable) {
        sql = templates.createTable(table, columns || []);
      } else if (operation === "addColumn" && columns?.[0]) {
        sql = templates.addColumn(table, columns[0]);
      } else if (operation === "addIndex") {
        sql = templates.addIndex(
          table,
          (columns || []).map((c) => c.name)
        );
      } else if (operation === "createCollection") {
        sql = templates.createCollection(table);
      }

      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                { migration: sql, database, operation, reversible: true },
                null,
                2
              ),
            },
          ],
        },
      };
    }

    if (toolName === "validate_migration") {
      const warnings = [];
      const script = args.script || "";
      if (/DROP\s+TABLE/i.test(script))
        warnings.push("Destructive: DROP TABLE detected");
      if (/DROP\s+COLUMN/i.test(script))
        warnings.push("Destructive: DROP COLUMN detected — consider deprecation instead");
      if (/NOT NULL/i.test(script) && !/DEFAULT/i.test(script))
        warnings.push("NOT NULL without DEFAULT may fail on existing rows");
      if (!/IF\s+(NOT\s+)?EXISTS/i.test(script))
        warnings.push("Missing IF EXISTS / IF NOT EXISTS guard");

      return {
        jsonrpc: "2.0",
        id,
        result: {
          content: [
            {
              type: "text",
              text: JSON.stringify(
                {
                  valid: warnings.length === 0,
                  warnings,
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

process.stderr.write("[migration-helper] Server started\n");

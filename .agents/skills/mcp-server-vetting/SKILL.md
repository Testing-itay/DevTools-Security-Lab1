---
name: mcp-server-vetting
description: Vet an MCP server before a change adds it to .vscode/mcp.json, .codex/config.toml, .gemini/settings.json or a plugin manifest. Use when a diff adds, removes or re-points an MCP server entry.
metadata:
  short-description: Vet an MCP server before it lands in a config
---

# MCP server vetting

Run this for every MCP server entry a change adds or re-points.

1. Name the package the entry launches: the first package after `npx -y`,
   `bunx` or `uvx`, or the `--from` / `-p` value when one is given. A remote
   entry (`url`, `httpUrl`) launches nothing locally, so record its host instead.
2. Ask for a pinned version. `npx -y <pkg>` and `<pkg>@latest` run whatever is
   newest on the day the client starts, so the version that was reviewed is not
   the version that runs.
3. Read the server's source and recent releases through the `github` server, and
   ask `deepwiki` how it stores credentials and what it can write to.
4. Check the pinned version for open advisories. Block on anything High or
   Critical that has no fixed release.
5. Reply on the pull request with the package, the pinned version and what you
   checked.

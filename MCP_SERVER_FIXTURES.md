# MCP server fixtures

Real-shape MCP client configs for MCP server discovery (LIM-46325), and unpinned
servers for SCA on a package-cache miss (LIM-46347).

## Why these exist

`McpServersCollector` used to read only files with `mcp` in the name, only a
top-level `mcpServers` key in JSON, and only `[mcpServers.<name>]` sections in
TOML. The clients most often committed to repositories use other shapes, so their
servers were never inventoried:

| Client | File | Server key |
|---|---|---|
| VS Code / Copilot | `.vscode/mcp.json` | top-level `servers` |
| Codex | `.codex/config.toml` | `[mcp_servers.<name>]` |
| Gemini CLI | `.gemini/settings.json` | `mcpServers` |
| Claude Code plugin | `<plugin>/.claude-plugin/plugin.json` | inline `mcpServers` |

The older MCP fixtures here (`.cursor/mcp.json`, `.claude/mcp.json`,
`mcp-servers.toml`) all use shapes the collector already read, which is why they
never caught this.

Separately, a server launched without a version (`npx -y <pkg>`) was resolved only
when the tenant already had the package cached, for example as a regular
dependency of another repository. Otherwise it got no CVE or malware check.

## Discovery (LIM-46325)

17 servers in 6 files. No existing server changes.

| File:line | Server | Mode | Source | Rule exercised |
|---|---|---|---|---|
| `.vscode/mcp.json:11` | `vscode-github` | Remote | `https://api.githubcopilot.com/mcp/` | `servers` alias; `type: http` with `headers` and an `inputs` prompt |
| `.vscode/mcp.json:18` | `vscode-deepwiki` | Remote | `https://mcp.deepwiki.com/sse` | `type: sse` |
| `.vscode/mcp.json:22` | `vscode-database` | Local | `@executeautomation/database-server` | `type: stdio` with `envFile`; unpinned |
| `.vscode/mcp.json:28` | `vscode-git-pinned` | Local | `mcp-server-git@2026.8.18` | pinned `uvx` control |
| `.codex/config.toml:9` | `codex-openai-docs` | Remote | `https://developers.openai.com/mcp` | `[mcp_servers.*]` after the unrelated `[Plugins]` table |
| `.codex/config.toml:12` | `codex-sentry` | Remote | `https://mcp.sentry.dev/mcp` | `bearer_token_env_var` |
| `.codex/config.toml:16` | `codex-taskwarrior` | Local | `mcp-server-taskwarrior` | `[mcp_servers.<name>.env]` subtable is not a server |
| `.codex/config.toml:24` | `codex-calculator` | Local | `mcp-server-calculator` | multi-line `args` array |
| `.codex/config.toml:32` | `codex-release-notes` | Local | `uv run --with mcp[cli] mcp run tools/release_notes/server.py` | `]` inside an argument (see Findings) |
| `services/api/.codex/config.toml:1` | `api-mysql` | Local | `@benborla29/mcp-server-mysql@2.0.9` | path rule below the repository root |
| `.gemini/settings.json:12` | `gemini-deepwiki` | Remote | `https://mcp.deepwiki.com/mcp` | `httpUrl` when `url` is absent |
| `.gemini/settings.json:16` | `gemini-atlassian` | Remote | `https://mcp.atlassian.com/v1/sse` | `url` (SSE) |
| `.gemini/settings.json:19` | `gemini-browser` | Local | `@browsermcp/mcp@latest` | beside unrelated `ui`, `context` and `mcp` keys |
| `plugins/code-guardian/.claude-plugin/plugin.json:21` | `guardian-semgrep` | Local | `mcp-remote` | array form: the `./.mcp.json` string is skipped, the object is read |
| `plugins/code-guardian/.claude-plugin/plugin.json:25` | `guardian-taint-index` | Local | `python ${CLAUDE_PLUGIN_ROOT}/servers/taint_index.py --stdio` | `${CLAUDE_PLUGIN_ROOT}` paths |
| `skills/3rd-party/superpowers/.claude-plugin/plugin.json:15` | `superpowers-transcripts` | Local | `@kimtaeyoon83/mcp-server-youtube-transcript` | inline map form |
| `skills/3rd-party/superpowers/.claude-plugin/plugin.json:19` | `superpowers-context7` | Remote | `https://mcp.context7.com/mcp` | `type: http` in a plugin |

### Must yield no server

| File | Why |
|---|---|
| `mcp_servers/catalog/mcp-registry-servers.json` | An MCP Registry listing. Its `servers` is an array, and the `servers` alias only counts an object. |
| `.claude-plugin/plugin.json` | `mcpServers` is a string path. Paths are not followed. |
| `.agents/skills/mcp-server-vetting/agents/openai.yaml` | Declares two servers in a file the collector does not read (see Findings). |

### Relations

- Codex rows link to the Codex agent. `services/api/.codex/` becomes a second
  Codex definition.
- Gemini rows link to the Gemini agent.
- VS Code rows link to no agent (see Findings).
- `guardian-*` link to `code-guardian`, and not to `tab-navigator` beside it.
  `superpowers-*` link to `superpowers`.
- Every server also links to the repo-root plugins, because a root plugin owns
  every path (finding 3 in [AGENT_PLUGIN_FIXTURES.md](AGENT_PLUGIN_FIXTURES.md)).

## Unpinned servers (LIM-46347)

Latest registry versions as of 30 Sep 2026.

| Server | Package | Latest | Expected after the fix |
|---|---|---|---|
| `vscode-database` | npm `@executeautomation/database-server` | 1.1.0 | resolved to 1.1.0, carrying CVE-2025-59333 (High, read-only mode bypass, no fixed release) |
| `codex-taskwarrior` | npm `mcp-server-taskwarrior` | 1.0.1 | resolved to 1.0.1, carrying CVE-2026-5833 (Low, command injection, no fixed release) |
| `codex-calculator` | PyPI `mcp-server-calculator` | 0.2.1 | resolved, no advisory |
| `gemini-browser` | npm `@browsermcp/mcp` | 0.1.3 | resolved; `@latest` counts as unpinned |
| `superpowers-transcripts` | npm `@kimtaeyoon83/mcp-server-youtube-transcript` | 0.1.1 | resolved, no advisory |
| `guardian-semgrep` | npm `mcp-remote` | 0.14.3 | resolved to 0.14.3 with no finding: CVE-2025-6514 affects 0.0.5 up to, not including, 0.1.16 |
| `tm1-fork` in `.cursor/mcp.json` | npm `@ffschrattenecker/tm1-mcp-server` | 9.2.0 | resolved to 9.2.0 by the second fetch one minute after the first: a fork created on 25 Sep 2026 that the SCA content service had never seen, so the first answer has no version |

Controls:

| Server | Expected |
|---|---|
| `vscode-git-pinned`, `api-mysql` | Pinned. Same result as before the fix. |
| `t13-flags-after-command`, `t14-npx-port-flag` in `.cursor/mcp.json` | `acme-usage-mcp` and `acme-mcp-gateway` exist on neither registry. They stay unresolved, and the extraction still completes. |
| `t05-npx-scoped-package`, `t07-npx-latest-tag` in `.cursor/mcp.json` | Earlier scans have already seen these packages. If the tenant has them cached, they resolve from the cache without a fetch. |

A package proves the cache-miss path only once per tenant. The first extraction
after the fix stores the package's content, and every later extraction reads it
from the cache. To test the miss again on a tenant that has already scanned this
commit, add a server whose package that tenant has never seen.

The resolved version is fixed at extraction. If one of these packages publishes a
new release, the inventory keeps the old version until the repository is extracted
again. That is out of scope for LIM-46347.

## The skill

`.agents/skills/mcp-server-vetting/` is a Codex repository skill: a `SKILL.md`
plus `agents/openai.yaml`, the metadata file Codex reads beside it. The
`dependencies.tools` entries in that file declare the two MCP servers the skill
needs, `github` and `deepwiki`. That is how a Codex skill brings its own servers.

Expected:

- the skill is detected as an agent skill and linked to the `spend-control`
  plugin (`.agents/plugin.json`);
- no MCP server comes from `openai.yaml`.

## Findings

1. **A `]` inside a TOML argument truncates `args`.** The TOML array pattern ends
   at the first `]`, so `"mcp[cli]"` closes the array early. `codex-release-notes`
   is reported with the source `uv run --with` instead of the full command. The
   same code reads `[mcpServers.*]`, so the bug predates LIM-46325. The fix makes
   Codex configs reachable, though, and this is the launch line the MCP Python SDK
   writes (`uv run --with mcp[cli] mcp run <server.py>`). With a package runner
   (`uvx`, `npx`), the package can be one of the dropped arguments. The server then
   has no package and gets no SCA check.
2. **VS Code servers link to no AI agent.** Copilot is detected from `.github/`,
   and nothing maps `.vscode/` to an agent, so the four `vscode-*` servers have no
   related agent.
3. **Servers declared by a skill are not inventoried.** The two servers in
   `.agents/skills/mcp-server-vetting/agents/openai.yaml` are real Codex
   configuration, and neither fix reads that file.

## Checking

Both fixes must be deployed on the environment that scans this repository.

1. Before scanning, confirm that the tenant's package cache has none of the six
   packages in the unpinned table. A package that is already cached tests the
   cache-hit path, not the miss.
2. Scan the commit.
3. MCP servers for this repository: the 17 rows above appear with the listed file,
   line, mode and source. `codex-taskwarrior` appears once. No server comes from
   `mcp-registry-servers.json` or `openai.yaml`.
4. Relations match the list above.
5. Each unpinned row has a linked dependency at the version in the table, and the
   two vulnerable ones carry their CVEs. `t13` and `t14` have no dependency, and the
   scan did not fail.

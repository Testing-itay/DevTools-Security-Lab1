---
name: update-text
description: >
  Self-service UI text changes for PMs — find hardcoded strings, replace them,
  validate, create a Jira task, and open a PR with deploy preview link.
  Use when the user wants to "update text", "change copy", "rename a label",
  "fix a typo in the UI", or provides old text and new text for a string swap.
disable-model-invocation: true
---

# update-text — PM self-service copy changes

Replace hardcoded UI strings, validate the build, create a Jira task, and open a PR.

## Inputs

Collect all three from the user before starting:

- **Current text** — exact string as it appears in the UI
- **New text** — replacement string
- **Location hint** — where in the app (e.g. "reports page", "settings panel", or a URL like `https://protect.sharegate-stg.com/reports`). If a URL is provided, extract the pathname and match it against route paths registered via `runtime.registerRoute` in each module's `register.tsx` to narrow the search scope.

If any input is missing, ask for it.

---

## Workflow

### 1. Validate MCP availability

Before doing any work, confirm both MCP integrations are reachable:

- **GitHub MCP**: call `mcp__claude_ai_github_mcp__list_pull_requests` with `owner: "gsoft-inc"`, `repo: "sg-protect-web"`, `perPage: 1`.
- **Jira MCP**: call `mcp__claude_ai_Atlassian__getJiraIssue` for `SGPD-6484`.

Run both calls in parallel. If either fails, stop immediately and tell the PM which integration is unavailable.

### 2. Find matches

Use the Grep tool with glob `"*.{ts,tsx}"` to find the exact current text. Paths ignored by `.gitignore` are automatically excluded. Additionally filter out `*.test.*` and `*.stories.*` files from results. If a location hint was given, narrow results to the matching app/module directory.

- If **0 matches**: tell the user the text was not found and ask them to verify.
- If **>3 matches** after filtering: ask the user for more specificity.

### 3. Confirm with PM

Show each match with ~3 lines of context. Wait for **explicit confirmation** before editing. Do not proceed without a clear "yes".

### 4. Edit files

Replace old text with new text using the `Edit` tool. Process **one occurrence at a time** — the same string may appear in unrelated contexts (e.g. a tooltip and a heading), so `replace_all` would silently change all of them without confirmation.

### 5. Validate

Run the applicable validation commands for the affected package(s). Refer to `docs/agents/commands.md` for available commands. Fix errors before continuing.

### 6. Create Jira task

Use `mcp__claude_ai_Atlassian__createJiraIssue` with:

| Field | Value |
|-------|-------|
| `projectKey` | `SGPD` |
| `issueTypeName` | `Sub-task` |
| `parent` | `SGPD-6484` |
| `summary` | `Update UI text: "<old>" -> "<new>"` (truncate if long) |
| `description` | Old text, new text, list of changed file paths |
| `additional_fields` | `{"customfield_10001": "SG Protect F1"}` |

### 7. Branch + commit + PR (via GitHub MCP)

All git operations go through the GitHub MCP — no local `git` or `gh` CLI commands.

1. **Create branch**: `mcp__claude_ai_github_mcp__create_branch` with `owner: "gsoft-inc"`, `repo: "sg-protect-web"`, `branch: "<ISSUE_KEY>_update-text"`, `from_branch: "main"`.

2. **Push files**: `mcp__claude_ai_github_mcp__push_files` with `owner: "gsoft-inc"`, `repo: "sg-protect-web"`, `branch: "<ISSUE_KEY>_update-text"`, `message: "[<ISSUE_KEY>] Update UI text: \"<old>\" -> \"<new>\""`, `files`: array of `{ path, content }` for each modified file. Read each file's full content after editing to supply the `content` field.

3. **Open PR**: `mcp__claude_ai_github_mcp__create_pull_request` with `owner: "gsoft-inc"`, `repo: "sg-protect-web"`, `title: "[<ISSUE_KEY>] Update UI text"`, `head: "<ISSUE_KEY>_update-text"`, `base: "main"`, `draft: false`, and body:
   ```
   ## Summary
   - Updated UI text: `<old>` -> `<new>`
   - Files changed: <list>
   - Jira: https://workleap.atlassian.net/browse/<ISSUE_KEY>

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   ```

### 8. Wait for deploy preview

Poll PR comments every 30s, up to 5 min, using `mcp__claude_ai_github_mcp__pull_request_read` with `method: "get_comments"`, `owner: "gsoft-inc"`, `repo: "sg-protect-web"`, `pullNumber: <PR_NUMBER>`.

Look for a comment by the `netlify` bot containing "Deploy Preview". Extract the deploy preview URL (pattern: `https://deploy-preview-<PR_NUMBER>--sg-protect-preview.netlify.app`).

If the timeout expires, report the PR URL and tell the PM to check back for the preview.

---

## Final output

Report to the PM:

- Files changed
- Jira task key + link (`https://workleap.atlassian.net/browse/<ISSUE_KEY>`)
- PR URL
- Deploy preview URL (or note that it's still building)
- "A developer will review and approve the PR before it is merged."
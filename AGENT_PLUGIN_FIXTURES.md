# Agent plugin fixtures

Real-shape fixtures for the agent-plugin detection surfaces (LIM-44969).

## Why these exist

The `AgentPluginsCollector` looks for five files that no vendor ships
(`.claude/plugins.json`, `.codex/config.toml`, `.cursor/extensions.json`,
`.gemini/extension.yaml`, `.gemini/extension.yml`), so it reports zero plugins
everywhere. Its unit tests pass because they feed it the same invented formats,
and this repo's original fixtures were built from those formats too — which is
why smoke was green against a collector that cannot find anything real.

Every fixture below is modelled on a layout measured in
`plugin_json_ALL-25-8-2026.csv` (env-explorer, 25 Aug 2026 — 1,718 `plugin.json`
files across 323 repositories and 30 customers). Where a fixture has no measured
instance it is labelled as such.

**The fictional fixtures are deliberately left in place.** Removing them turns
smoke red between merges. The sequence is: real-shape fixtures here first, the
collector change second, the true-set flip third.

## The rules being exercised

A file is an agent-plugin manifest if **either** structural test passes; both are
computed from the tree index with no file reads. Content is read only when both
are silent.

- **Test A** — parent directory matches `^\.([a-z0-9][a-z0-9-]*-)?plugin$`.
  The leading dot is load-bearing: it is what separates `.cursor-plugin` from
  `python-api-plugin` and `dataops-ai-plugins`.
- **Test B** — a sibling of `plugin.json` is one of
  `skills/ agents/ commands/ prompts/ skill-sources/ .mcp.json mcp.json
  skill.json SKILL.md AGENTS.md .claude-plugin/`, or matches
  `*-skills/ *-agents/ *-commands/ *-prompts/ *.agent.md`, or is `hooks/` with no
  Grafana marker present (`module.ts`, `module.tsx`, `panelcfg.cue`,
  `datasource.ts`, `MANIFEST.txt`).
- **Test C** — for a `plugin.json` alone in its directory, parse it and accept on
  an `agent-plugins.org` `$schema` **host** (not the literal `1.0.0` URL) or a
  conforming manifest shape.

## Manifest fixtures

58 `plugin.json` files: 46 must be detected, 12 must not. Six sit at depth 1–2
and the remaining 52 at depth 3–6, matching the measured distribution where
1,702 of 1,718 files are nested deeper than the repository's top level. Today's
`GetRelevantFilePathsAsync` override restricts lookup to top-level directories,
so the traversal change is the feature and not an edge case.

### Test A — the directory names the vendor

| Fixture | Exercises | Signal | Expected | Modelled on |
|---|---|---|---|---|
| `plugins/code-apps-preview/.plugin/plugin.json` | Legacy bare `.plugin` | `.plugin` | **accept** | Prudential UAT / Fiserv, 5 files |
| `plugins/code-guardian/.claude-plugin/plugin.json` | Full Claude package | `.claude-plugin` | **accept** | 646 `.claude-plugin` files |
| `plugins/devin-triage/.devin-plugin/plugin.json` | Devin — undocumented vendor | `.devin-plugin` | **accept** | Tesco `agent-tools`, 1 file |
| `plugins/gemini-translate/.gemini-plugin/plugin.json` | Gemini — convention only | `.gemini-plugin` | **accept** | absent from the scan; this repo ships a `.gemini/` surface |
| `plugins/kimi-context/.kimi-plugin/plugin.json` | Kimi — undocumented vendor | `.kimi-plugin` | **accept** | Tesco `agent-tools`, 1 file |
| `plugins/mem-palace/.antigravity-plugin/plugin.json` | Antigravity — undocumented vendor | `.antigravity-plugin` | **accept** | Capital Group `mempalace`, 1 file |
| `plugins/repo-refactor/.codex-plugin/plugin.json` | Codex | `.codex-plugin` | **accept** | 83 `.codex-plugin` files |
| `plugins/tab-navigator/.cursor-plugin/plugin.json` | Cursor | `.cursor-plugin` | **accept** | 98 `.cursor-plugin` files |
| `plugins/windsurf-flow/.windsurf-plugin/plugin.json` | Windsurf — convention only | `.windsurf-plugin` | **accept** | absent from the scan and from all vendor docs |

### Deduplication — one logical plugin, many sibling manifests

| Fixture | Exercises | Signal | Expected | Modelled on |
|---|---|---|---|---|
| `.claude-plugin/plugin.json` | Root multi-vendor group 1/3 | `.claude-plugin` | **accept** | Capital Group `mempalace` — 9 repos carry several vendor dirs at the repo root |
| `.codex-plugin/plugin.json` | Root multi-vendor group 3/3 | `.codex-plugin` | **accept** | Capital Group `mempalace` |
| `.cursor-plugin/plugin.json` | Root multi-vendor group 2/3 | `.cursor-plugin` | **accept** | Capital Group `mempalace` |
| `skills/3rd-party/superpowers/.claude-plugin/plugin.json` | Dedup group 1/5 | `.claude-plugin` | **accept** | Tesco `agent-tools` |
| `skills/3rd-party/superpowers/.codex-plugin/plugin.json` | Dedup group 2/5 | `.codex-plugin` | **accept** | Tesco `agent-tools` |
| `skills/3rd-party/superpowers/.cursor-plugin/plugin.json` | Dedup group 3/5 | `.cursor-plugin` | **accept** | Tesco `agent-tools` |
| `skills/3rd-party/superpowers/.devin-plugin/plugin.json` | Dedup group 4/5 | `.devin-plugin` | **accept** | Tesco `agent-tools` |
| `skills/3rd-party/superpowers/.kimi-plugin/plugin.json` | Dedup group 5/5 | `.kimi-plugin` | **accept** | Tesco `agent-tools` |

### Test B — the neighbours give it away

| Fixture | Exercises | Signal | Expected | Modelled on |
|---|---|---|---|---|
| `.agents/plugin.json` | `.agents/` container | `AGENTS.md` | **accept** | BHP `spend-control` / `agent-pricelister` |
| `bundles/plugins/ai-documentation-workflow/agents/doc-orchestrator/plugin.json` | `*.agent.md` + `.apm/` | `doc-orchestrator.agent.md` | **accept** | Shell `ide-elevate-ai-marketplace` |
| `bundles/plugins/ai-documentation-workflow/agents/doc-writer/plugin.json` | `*.agent.md` + `.apm/` | `doc-writer.agent.md` | **accept** | Shell `ide-elevate-ai-marketplace` |
| `bundles/plugins/ai-documentation-workflow/plugin.json` | Bundle level | `agents/` | **accept** | Shell `ide-elevate-ai-marketplace` |
| `bundles/plugins/python-api-plugin/agents/py-plugin-endpoint-designer/plugin.json` | `*.agent.md`, depth 6 | `.mcp.json` | **accept** | Shell `ewai-test-backend-project` |
| `bundles/plugins/python-api-plugin/plugin.json` | Bundle level | `agents/` | **accept** | Shell `ewai-test-backend-project` |
| `bundles/plugins/sds-frontend-plugin/agents/sds-plugin-form-builder/plugin.json` | `*.agent.md`, depth 6 | `sds-plugin-form-builder.agent.md` | **accept** | Shell `ewai-test-frontend-project` |
| `bundles/plugins/sds-frontend-plugin/plugin.json` | Bundle level | `agents/` | **accept** | Shell `ewai-test-frontend-project` |
| `bundles/plugins/sds-frontend-plugin/skills/sds-plugin-a11y-check/plugin.json` | `SKILL.md` at depth 6 | `SKILL.md` | **accept** | Shell `ewai-test-frontend-project` |
| `hooks/secrets-scanner/plugin.json` | `hooks/` with no Grafana marker | `hooks/` (guarded) | **accept** | Shell `dnr-ts-geneva-ai-marketplace` |
| `plugin.json` | Repo root is the plugin | `.claude-plugin/` | **accept** | BASF `python_dev_plugin` — 16 of 1,718 files sit at depth 1 |
| `plugins/appstore-migrator/plugin.json` | No vendor dir | `.mcp.json` | **accept** | BASF `appstore-taskforce-ai` |
| `plugins/archie/plugin.json` | `plugin-skills/` + `plugin-agents/` | `.claude-plugin/` | **accept** | Capital Group `Archie` — 5 files lost to the missing `*-skills/` pattern |
| `plugins/cfa-common/plugin.json` | Python package | `.mcp.json` | **accept** | C. H. Robinson `CFA_All_Projects` |
| `plugins/check-duplicate-skill/plugin.json` | `.claude-plugin/` as sibling | `.claude-plugin/` | **accept** | Capital Group `cg-ig-marketplace-plugins` |
| `plugins/copilot-marketplace/plugin.json` | Copilot marketplace | `.mcp.json` | **accept** | Nasdaq `Calypso Copilot Plugins`, 63 plugins |
| `plugins/doctopus/plugin.json` | APM package manager | `skills/` | **accept** | C. H. Robinson `Doctopus` — `.apm/` + `apm.yml` |
| `plugins/inline-skill/plugin.json` | `skill.json` | `skill.json` | **accept** | marker list |
| `plugins/mcp-bridge/plugin.json` | plain `mcp.json` | `mcp.json` | **accept** | marker list, non-dot variant |
| `plugins/mdt-ai-skills/plugin.json` | `prompts/` only | `prompts/` | **accept** | Capital Group `mdt-ai-skills` |
| `plugins/release-pack/plugin.json` | `*-commands/` + `*-prompts/` | `release-commands/` | **accept** | pattern markers, no measured instance |
| `plugins/sds/plugin.json` | Non-dot parent that IS a plugin | `agents/` | **accept** | Shell `plugins/sds/` |
| `plugins/skill-registry/plugin.json` | `skill-sources/` | `skill-sources/` | **accept** | marker list |
| `skills/checkout/optimization-triage/plugin.json` | Manifest inside a skill | `SKILL.md` | **accept** | Capital Group `psm-agent-skills` — 30 files lost to the missing `SKILL.md` marker |
| `skills/get-prices/plugin.json` | Minimal pair | `SKILL.md` | **accept** | Capital Group `psm-agent-skills` |
| `web/i18n/en-US/plugin.json` | Dify i18n bundle | `skill.json` | **accept** | Crest / Free_AutoFix `dify` — 24 files |

### Test C — content decides, only when A and B are silent

| Fixture | Exercises | Signal | Expected | Modelled on |
|---|---|---|---|---|
| `plugins/hourglass/.github/plugin.json` | Alone under `.github/` | `$schema` host `agent-plugins.org` | **accept** | Capital Group — 22 of the 162 ambiguous files |
| `plugins/invalid-plugin-json/plugin/plugin.json` | Alone, malformed JSON | unparseable | **reject** | real parent-dir name in the scan |
| `plugins/panel-only/plugin/plugin.json` | Alone, Grafana panel content | non-conforming shape | **reject** | content-shape rejection |
| `plugins/planning/plugin/plugin.json` | Alone, no `$schema` | manifest shape | **accept** | accepted on manifest shape alone |
| `plugins/testiq/plugin/plugin.json` | Alone, **future** schema revision | `$schema` host `agent-plugins.org` | **accept** | the 99 files under a folder named `plugin` |

### Rejects — must yield no plugin

| Fixture | Exercises | Signal | Expected | Modelled on |
|---|---|---|---|---|
| `feedgen-plugins/commerce_media_random_selected_brand/lt/plugin.json` | Feed generator, `lt` | no marker (2 siblings) | **reject** | Rakuten `adextools` |
| `feedgen-plugins/commerce_media_random_selected_brand/prod/plugin.json` | Feed generator, `prod` | no marker (2 siblings) | **reject** | Rakuten `adextools` |
| `feedgen-plugins/commerce_media_random_selected_brand/qa/plugin.json` | Feed generator, `qa` | no marker (2 siblings) | **reject** | Rakuten `adextools` |
| `grafana/cloudwatch-datasource/plugin.json` | Grafana datasource | no marker (2 siblings) | **reject** | Apiiro_Website `grafana` |
| `grafana/heatmap-panel/plugin.json` | Grafana panel **with `hooks/`** | no marker (3 siblings) | **reject** | the 4 measured false positives the guard removes |
| `grafana/test-app/plugin.json` | Grafana app, `MANIFEST.txt` | no marker (2 siblings) | **reject** | Apiiro_Website `grafana` |
| `grafana/zero-button-plugin/src/plugin.json` | Grafana panel | no marker (3 siblings) | **reject** | BHP `DASH` |
| `lib/dataops-ai-plugins/plugin.json` | npm package named `*-plugins` | no marker (6 siblings) | **reject** | Payoneer `payo-ai-marketplace-packages` |
| `lib/extract-text-webpack-plugin/schema/plugin.json` | webpack JSON schema | no marker (1 sibling) | **reject** | Cigna `database-frontend` |
| `plugin/plugin.json` | Plain `plugin/` folder | no marker (1 sibling) | **reject** | Apiiro_Website `grafana` installer testdata |

## Declaration surfaces

These are the other half of the feature and the half with **no customer
measurement at all** — the scan covered manifests only. Public GitHub suggests
roughly 4,900 repositories carry an `enabledPlugins` block, which makes it likely
but not measured.

A declaration holds an object **map** keyed `"name@marketplace"`, not an array,
and the value is a real boolean.

| Fixture | Exercises |
|---|---|
| `.claude/settings.json` | Six entries: four enabled, two explicitly `false`. Also `"@acme/security-tools@acme-internal"`, which only splits correctly on the **last** `@`. |
| `services/api/.claude/settings.json` | A nested declaration. Today's traversal only reads top-level directories. |
| `.github/copilot/settings.json` | The Copilot-side declaration surface. |
| `.cursor/extensions.json` | Correctly spelled IDE surface. Belongs to `IdeExtensionsCollector` and must yield **zero** plugin entities, or one file produces two entity types. |

Two entries are `false` on purpose. A `?? true` fallback that reports unknown
enablement as enabled is a fabricated fact in a column a customer reads; a
manifest sitting in a repository states nothing about enablement and should
record null, not true.

## Deduplication

Two groups, because the two shapes are different code paths:

- `skills/3rd-party/superpowers/` ships **five** sibling vendor manifests over one
  shared nested tree — the measured worst case (Tesco `agent-tools`).
- The repository root carries **three** vendor manifests under one name, so the
  group's root is the string `.`. Nine repositories in the scan look like this;
  Capital Group `mempalace` carries four at its root.

Collapsing by `(plugin name, plugin root directory)` gives 40 distinct plugins
from 46 accepted manifests. Collapsing by manifest path gives 46 and inflates the
inventory by 15%.

The repository root also carries a **second, differently named** plugin: a bare
`plugin.json` alongside `.claude-plugin/plugin.json`. One repository in the scan
does this (Shell `ddni-sei-arscontexta`), and it means a single plugin root can
hold two plugins — which is what makes content ownership at the root ambiguous
rather than merely broad.

## Linkage

Detection produces entities; linkage decides what each one owns. The old rule
compared the **first path segment**, which is broken in both directions: under
`plugins/` every plugin shares that segment, so each one claims every other one's
content.

A skill or MCP server belongs to a plugin when its path sits under that plugin's
**root directory**. A vendor directory is packaging, not identity, so the root of
`plugins/archie/.claude-plugin/plugin.json` is `plugins/archie`:

```
plugins/archie/.claude-plugin/plugin.json   root is plugins/archie
plugins/archie/plugin-skills/adr-review/    linked
plugins/archie/.mcp.json                    linked
plugins/sds/skills/review/SKILL.md          not linked to archie
.claude/settings.json                       declared only, holds nothing here
```

### Content to plugin

104 content files (`SKILL.md`, `.mcp.json`, `mcp.json`) against 40 plugin roots.

| Case | Fixture | Expected |
|---|---|---|
| Same skill path under two roots sharing a parent segment | `plugins/code-guardian/skills/review/SKILL.md` vs `plugins/sds/skills/review/SKILL.md` | one owner each; a first-segment or name rule links both to both |
| Same MCP **server name** under three roots | `code-search` in `code-guardian`, `mcp-bridge`, `tab-navigator` | resolved by containment, never by server name |
| Nested plugin roots | `bundles/plugins/python-api-plugin/agents/py-plugin-endpoint-designer/{skills/schema-draft,.mcp.json}` | owned by the inner plugin, not by the bundle |
| Bundle's own content | `bundles/plugins/python-api-plugin/skills/endpoint-review/` | owned by the bundle |
| Three-level nesting | `bundles/plugins/sds-frontend-plugin/skills/sds-plugin-a11y-check/SKILL.md` | innermost of three candidate roots |
| Declared but not shipped | `@acme/security-tools`, `flaky-test-quarantine`, `doc-agent`, `legacy-pr-summarizer` | plugin entity with no content and no manifest |

10 plugin-to-MCP-server pairs across 7 manifests exercise `RelatedMcpServerIds`
and `RelatedAgentPluginIds` in both directions.

### Plugin to agent

There is no provider field, but the surface identifies the agent: `.claude/settings.json`
is Claude Code, `.github/copilot/settings.json` is Copilot, `.codex-plugin/` is
Codex. Current attribution across the 46 accepted manifests and 3 declaration
surfaces:

| Agent | Plugins | Root surface for `AiAgentsCollector` |
|---|---|---|
| claude-code | 9 | `.claude/` present |
| copilot | 3 | `.github/` present |
| cursor | 3 | `.cursor/` present |
| codex | 3 | `.codex/` present |
| gemini | 1 | `.gemini/` present |
| antigravity, devin, kimi, windsurf | 6 | **absent** — no agent entity to link to |
| none | 30 | no vendor directory and no declaration |

Two things that fixture the caveats directly. First, `superpowers` and the
repo-root group each carry several vendor directories for **one** plugin, which is
"supports these agents", not "these agents use it". Second, four vendors named in
the fixtures have no matching root surface in this repository, so a plugin can
name an agent that `AiAgentsCollector` never produced — reproducible here without
building a second repo.

## Findings

1. **`skill.json` admits the Dify i18n bundles.** `web/i18n/en-US/plugin.json`
   is a translation-strings file, but its directory contains a literal
   `skill.json`, so the exact-name marker accepts it. This is 24 of the 180 files
   Test B adds — inside the accepted set, not the rejected one. The `agent-v-2.json`
   substring hazard was recorded for this same directory; the `skill.json`
   collision in it was not. Either drop `skill.json` from the marker list or
   guard it the way `hooks/` is guarded. The fixture makes the consequence
   concrete: that file has no `name` field at all, so it becomes a plugin row the
   inventory cannot label — `verify_agent_plugin_fixtures.py` reports it under
   *accepted but carries no name field*.

2. **Nested bundles count twice.** Shell's `bundles/plugins/<pkg>/` carries a
   bundle-level manifest with `agents/` and `skills/` siblings, and each agent
   below it carries its own manifest. Both pass Test B, and because they have
   different names and different roots, dedup does not collapse them. A bundle of
   N agents yields N+1 entities. Whether that is right is a product question, but
   it is not currently a decision.

3. **A repo-root manifest absorbs the whole repository under pure containment.**
   16 of 1,718 measured manifests sit at the repository root, so the plugin root is
   `.` and every path is under it. Here that means **73 of 104 content files are
   claimed by the root plugin and by nothing else** — including `.claude/skills/`,
   `.cursor/skills/`, `.github/skills/` and `lib/ai-skills/`, which are agent-level
   skills that belong to an agent and not to any plugin. 31 files have more than
   one owning root, up to three deep. Containment as written is therefore not
   enough on its own: it needs nearest-ancestor resolution to pick one owner, and
   agent-surface directories need excluding from plugin content. The verifier
   prints both readings so the gap is a number rather than an opinion.

4. **`packages/` and `dist/` are gitignored in this repo.** The nested declaration
   fixture therefore sits at `services/api/.claude/settings.json` rather than the
   `packages/api/...` path named in the plan, and the npm reject sits at
   `lib/dataops-ai-plugins/` rather than `packages/dataops-ai-plugins/`. Same
   depth, same sibling sets, tracked by git.

## Checking

```
python3 verify_agent_plugin_fixtures.py
```

It applies the three tests to every `plugin.json` in the tree and asserts each one
lands on the verdict this document claims. It then resolves every `SKILL.md`,
`.mcp.json` and `mcp.json` to its owning plugin root and asserts that too, and
reports:

- the dedup collapse, per group
- the parsed declaration surfaces, with each key split on its last `@`
- content owned by a nested plugin, by a repo-root manifest only, or by nothing
- content names that appear under more than one plugin root
- plugin-to-MCP-server pairs
- where containment and nearest-ancestor disagree, and how deep
- plugin-to-agent attribution, and which named vendors have no root surface
- plugins declared in a `settings.json` that ship no manifest here

Exit 0 means the fixtures match. It checks the fixtures, not the collector — the
collector is expected to reproduce these verdicts once it is rebased on
`BaseFilesContentPropertiesCollector`.

`plugins/invalid-plugin-json/plugin/plugin.json` is intentionally malformed: it
must be rejected at parse time without failing extraction. It is the only invalid
JSON in the tree, so a validity sweep should report exactly one failure.

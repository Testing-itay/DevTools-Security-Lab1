#!/usr/bin/env python3
"""Check the agent-plugin fixtures against the LIM-44969 detection rules.

Applies Test A (vendor directory convention), Test B (sibling markers) and
Test C (content fallback) to every plugin.json in the tree and asserts each
fixture lands on the verdict AGENT_PLUGIN_FIXTURES.md claims for it.

    python3 verify_agent_plugin_fixtures.py

Exit 0 when every fixture matches, 1 otherwise. No dependencies beyond the
standard library. This checks the fixtures, not the collector.
"""
import collections
import json
import os
import pathlib
import re
import sys
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent

TEST_A = re.compile(r"^\.([a-z0-9][a-z0-9-]*-)?plugin$")
EXACT_MARKERS = {
    "skills/", "agents/", "commands/", "prompts/", "skill-sources/",
    ".mcp.json", "mcp.json", "skill.json", "SKILL.md", "AGENTS.md",
    ".claude-plugin/",
}
PATTERN_MARKERS = [
    re.compile(r".*-skills/$"), re.compile(r".*-agents/$"),
    re.compile(r".*-commands/$"), re.compile(r".*-prompts/$"),
    re.compile(r".*\.agent\.md$"),
]
# hooks/ is too generic on its own: React projects have one. Guard it against
# the Grafana file set, which is where the measured false positives came from.
GRAFANA_MARKERS = {"module.ts", "module.tsx", "panelcfg.cue", "datasource.ts",
                   "MANIFEST.txt"}
MANIFEST_REQUIRED = {"name", "version", "description"}
SCHEMA_HOST = "agent-plugins.org"


def siblings(directory, self_name):
    """Directory entries beside the manifest, directories suffixed with '/'."""
    return [
        entry + "/" if (directory / entry).is_dir() else entry
        for entry in sorted(os.listdir(directory))
        if entry != self_name
    ]


def test_c(path):
    """Content fallback. Gate on the schema host so a future revision of the
    specification does not silently drop out. Malformed JSON is a reject."""
    try:
        obj = json.loads((ROOT / path).read_text())
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return False, "unparseable (%s)" % type(exc).__name__
    if not isinstance(obj, dict):
        return False, "not an object"
    schema = obj.get("$schema")
    if isinstance(schema, str):
        host = urllib.parse.urlparse(schema).hostname or ""
        if host == SCHEMA_HOST:
            return True, "$schema host %s" % host
        return False, "$schema host %s" % host
    if MANIFEST_REQUIRED <= set(obj) and not {"info", "type"} & set(obj):
        return True, "conforming manifest shape"
    return False, "no $schema, non-conforming shape"


def classify(rel):
    """Return (verdict, reason) for one manifest path."""
    path = ROOT / rel
    directory = path.parent
    parent_name = directory.name if directory != ROOT else "<repo root>"
    sibs = siblings(directory, path.name)

    if TEST_A.match(parent_name):
        return "A", "parent directory %s" % parent_name

    for sib in sibs:
        if sib in EXACT_MARKERS:
            return "B", "sibling %s" % sib
        if any(p.match(sib) for p in PATTERN_MARKERS):
            return "B", "sibling %s (pattern)" % sib
        if sib == "hooks/" and not set(sibs) & GRAFANA_MARKERS:
            return "B", "sibling hooks/ (guarded, no Grafana marker)"

    if not sibs:
        accepted, why = test_c(rel)
        return ("C-accept" if accepted else "C-reject"), why

    return "reject", "no marker among %d sibling(s)" % len(sibs)


def plugin_root(rel, verdict):
    """A vendor directory is packaging, not identity: the plugin root is its
    parent. Dedup keys on (name, root) so sibling manifests collapse."""
    directory = pathlib.Path(rel).parent
    if TEST_A.match(directory.name):
        return str(directory.parent)
    return str(directory)


EXPECT = {
 # depth 1: the repo root is itself a plugin package (16 real files)
 'plugin.json':'B',
 # A: vendor conventions
 '.claude-plugin/plugin.json':'A',
 # multi-vendor packaging at the repo root: one logical plugin, three manifests,
 # all resolving to root "." (Capital Group mempalace shape, 9 repos)
 '.cursor-plugin/plugin.json':'A',
 '.codex-plugin/plugin.json':'A',
 'plugins/code-guardian/.claude-plugin/plugin.json':'A',
 'plugins/tab-navigator/.cursor-plugin/plugin.json':'A',
 'plugins/repo-refactor/.codex-plugin/plugin.json':'A',
 'plugins/mem-palace/.antigravity-plugin/plugin.json':'A',
 'plugins/devin-triage/.devin-plugin/plugin.json':'A',
 'plugins/kimi-context/.kimi-plugin/plugin.json':'A',
 'plugins/gemini-translate/.gemini-plugin/plugin.json':'A',
 'plugins/windsurf-flow/.windsurf-plugin/plugin.json':'A',
 'plugins/code-apps-preview/.plugin/plugin.json':'A',
 # A: dedup group (5 manifests, one logical plugin)
 'skills/3rd-party/superpowers/.claude-plugin/plugin.json':'A',
 'skills/3rd-party/superpowers/.codex-plugin/plugin.json':'A',
 'skills/3rd-party/superpowers/.cursor-plugin/plugin.json':'A',
 'skills/3rd-party/superpowers/.devin-plugin/plugin.json':'A',
 'skills/3rd-party/superpowers/.kimi-plugin/plugin.json':'A',
 # B: structural markers
 'plugins/appstore-migrator/plugin.json':'B',
 'plugins/copilot-marketplace/plugin.json':'B',
 'skills/checkout/optimization-triage/plugin.json':'B',
 'skills/get-prices/plugin.json':'B',
 '.agents/plugin.json':'B',
 'plugins/archie/plugin.json':'B',
 'plugins/check-duplicate-skill/plugin.json':'B',
 'plugins/release-pack/plugin.json':'B',
 'plugins/skill-registry/plugin.json':'B',
 'plugins/mcp-bridge/plugin.json':'B',
 'plugins/inline-skill/plugin.json':'B',
 'plugins/mdt-ai-skills/plugin.json':'B',
 'plugins/doctopus/plugin.json':'B',
 'plugins/cfa-common/plugin.json':'B',
 'bundles/plugins/python-api-plugin/agents/py-plugin-endpoint-designer/plugin.json':'B',
 'bundles/plugins/sds-frontend-plugin/agents/sds-plugin-form-builder/plugin.json':'B',
 'bundles/plugins/ai-documentation-workflow/agents/doc-orchestrator/plugin.json':'B',
 'bundles/plugins/ai-documentation-workflow/agents/doc-writer/plugin.json':'B',
 'hooks/secrets-scanner/plugin.json':'B',
 # C: content decides
 'plugins/hourglass/.github/plugin.json':'C-accept',
 'plugins/testiq/plugin/plugin.json':'C-accept',
 'plugins/planning/plugin/plugin.json':'C-accept',
 'plugins/invalid-plugin-json/plugin/plugin.json':'C-reject',
 'plugins/panel-only/plugin/plugin.json':'C-reject',
 # negatives
 'grafana/zero-button-plugin/src/plugin.json':'reject',
 'grafana/heatmap-panel/plugin.json':'reject',
 'grafana/cloudwatch-datasource/plugin.json':'reject',
 'grafana/test-app/plugin.json':'reject',
 'feedgen-plugins/commerce_media_random_selected_brand/lt/plugin.json':'reject',
 'feedgen-plugins/commerce_media_random_selected_brand/prod/plugin.json':'reject',
 'feedgen-plugins/commerce_media_random_selected_brand/qa/plugin.json':'reject',
 'lib/dataops-ai-plugins/plugin.json':'reject',
 # bundle-level manifests: accepted structurally, same as the agents nested
 # under them (measured Shell shape README.md;agents/;apm.yml;skills/)
 'bundles/plugins/python-api-plugin/plugin.json':'B',
 'bundles/plugins/sds-frontend-plugin/plugin.json':'B',
 'bundles/plugins/ai-documentation-workflow/plugin.json':'B',
 'bundles/plugins/sds-frontend-plugin/skills/sds-plugin-a11y-check/plugin.json':'B',
 'plugins/sds/plugin.json':'B',
 'plugin/plugin.json':'reject',
 'lib/extract-text-webpack-plugin/schema/plugin.json':'reject',
 # known collision: exact-name marker skill.json admits a Dify i18n bundle
 'web/i18n/en-US/plugin.json':'B',
}

# --- linkage ---------------------------------------------------------------
# A skill or MCP server belongs to a plugin when its path sits under that
# plugin's root directory. A vendor directory is packaging, not identity, so
# the root of `plugins/archie/.claude-plugin/plugin.json` is `plugins/archie`.
#
# Two readings of "under the root" diverge as soon as plugin roots nest:
#   containment      every plugin root that is an ancestor owns the file
#   nearest ancestor exactly one owner, the innermost root
# Both are reported, because a repo-root manifest makes them differ sharply.

CONTENT_NAMES = {"SKILL.md", ".mcp.json", "mcp.json"}

# Which agent a plugin is attributable to. The surface identifies the agent;
# there is no provider field to read.
VENDOR_AGENT = {
    ".claude-plugin": "claude-code",
    ".cursor-plugin": "cursor",
    ".codex-plugin": "codex",
    ".gemini-plugin": "gemini",
    ".antigravity-plugin": "antigravity",
    ".devin-plugin": "devin",
    ".kimi-plugin": "kimi",
    ".windsurf-plugin": "windsurf",
    ".plugin": None,  # legacy, carries no vendor
}
DECLARATION_AGENT = {
    ".claude/settings.json": "claude-code",
    ".github/copilot/settings.json": "copilot",
}
# Root surfaces AiAgentsCollector can see. It only looks at the repo root, so a
# plugin naming a vendor with no root surface has no agent entity to link to.
ROOT_AGENT_SURFACES = {
    ".claude": "claude-code", ".cursor": "cursor", ".codex": "codex",
    ".gemini": "gemini", ".github": "copilot",
}

# Expected nearest owner for every content file whose owner is a nested plugin
# root. Content owned only by a repo-root manifest is asserted by count below.
EXPECT_OWNER = {
    # cross-link trap: same skill path under two roots sharing a parent segment
    "plugins/code-guardian/skills/review/SKILL.md": "code-guardian",
    "plugins/sds/skills/review/SKILL.md": "sds",
    # same MCP server name under two roots: linkage cannot key on server name
    "plugins/code-guardian/.mcp.json": "code-guardian",
    "plugins/tab-navigator/.mcp.json": "tab-navigator",
    # nested roots: the inner plugin owns its content, not the bundle
    "bundles/plugins/python-api-plugin/agents/py-plugin-endpoint-designer/skills/schema-draft/SKILL.md": "py-plugin-endpoint-designer",
    "bundles/plugins/python-api-plugin/agents/py-plugin-endpoint-designer/.mcp.json": "py-plugin-endpoint-designer",
    "bundles/plugins/python-api-plugin/skills/endpoint-review/SKILL.md": "python-api-plugin",
    "bundles/plugins/ai-documentation-workflow/skills/doc-outline/SKILL.md": "ai-documentation-workflow",
    "bundles/plugins/sds-frontend-plugin/skills/sds-plugin-a11y-check/SKILL.md": "sds-plugin-a11y-check",
    # ordinary packaging
    "plugins/appstore-migrator/.mcp.json": "appstore-migrator",
    "plugins/appstore-migrator/skills/schema-diff/SKILL.md": "appstore-migrator",
    "plugins/archie/plugin-skills/adr-review/SKILL.md": "archie",
    "plugins/cfa-common/.mcp.json": "cfa-common",
    "plugins/cfa-common/skills/registry-lookup/SKILL.md": "cfa-common",
    "plugins/check-duplicate-skill/plugin-skills/similarity-scan/SKILL.md": "check-duplicate-skill",
    "plugins/code-guardian/skills/taint-tracing/SKILL.md": "code-guardian",
    "plugins/copilot-marketplace/.mcp.json": "copilot-marketplace",
    "plugins/copilot-marketplace/skills/calypso-backend-development/SKILL.md": "copilot-marketplace",
    "plugins/copilot-marketplace/skills/calypso-backend-review/SKILL.md": "copilot-marketplace",
    "plugins/copilot-marketplace/skills/calypso-frontend-development/SKILL.md": "copilot-marketplace",
    "plugins/devin-triage/skills/flaky-quarantine/SKILL.md": "devin-triage",
    "plugins/doctopus/skills/doc-audit/SKILL.md": "doctopus",
    "plugins/gemini-translate/skills/port-service/SKILL.md": "gemini-translate",
    "plugins/mcp-bridge/mcp.json": "mcp-bridge",
    "plugins/mem-palace/skills/session-recall/SKILL.md": "mem-palace",
    "plugins/sds/skills/token-audit/SKILL.md": "sds",
    "skills/3rd-party/superpowers/skills/brainstorming/SKILL.md": "superpowers",
    "skills/3rd-party/superpowers/skills/root-cause-tracing/SKILL.md": "superpowers",
    "skills/checkout/optimization-triage/SKILL.md": "optimization-triage",
    "skills/get-prices/SKILL.md": "get-prices",
    ".agents/skills/anomaly-review/SKILL.md": "spend-control",
}


def plugin_roots(manifests):
    """root path -> set of plugin names declared at that root."""
    roots = collections.defaultdict(set)
    for rel in manifests:
        verdict, _ = classify(rel)
        if verdict not in ("A", "B", "C-accept"):
            continue
        try:
            name = json.loads((ROOT / rel).read_text()).get("name")
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if name:
            roots[plugin_root(rel, verdict)].add(name)
    return roots


def content_files():
    out = []
    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        rel_dir = pathlib.Path(dirpath).relative_to(ROOT)
        for name in sorted(filenames):
            if name in CONTENT_NAMES:
                out.append(str(rel_dir / name))
    return sorted(out)


def owning_roots(rel, roots):
    """Plugin roots containing this file, innermost first."""
    found = []
    node = pathlib.Path(rel).parent
    while True:
        key = str(node)
        if key in roots:
            found.append(key)
        if key in (".", ""):
            break
        node = node.parent
    return found


def main():
    manifests = sorted(
        str(pathlib.Path(dirpath).relative_to(ROOT) / "plugin.json")
        for dirpath, _, filenames in os.walk(ROOT)
        if ".git" not in dirpath.split(os.sep) and "plugin.json" in filenames
    )

    failures = []
    counts = collections.Counter()
    for rel in manifests:
        verdict, why = classify(rel)
        counts[verdict] += 1
        expected = EXPECT.get(rel)
        if expected is None:
            failures.append("no expectation recorded: %s -> %s" % (rel, verdict))
        elif expected != verdict:
            failures.append("%s: expected %s, got %s (%s)"
                            % (rel, expected, verdict, why))
    for rel in EXPECT:
        if rel not in manifests:
            failures.append("fixture missing from tree: %s" % rel)

    accepted = counts["A"] + counts["B"] + counts["C-accept"]
    rejected = counts["reject"] + counts["C-reject"]
    print("manifests            %d" % len(manifests))
    print("  Test A  accept     %d" % counts["A"])
    print("  Test B  accept     %d" % counts["B"])
    print("  Test C  accept     %d" % counts["C-accept"])
    print("  Test C  reject     %d" % counts["C-reject"])
    print("  no marker, reject  %d" % counts["reject"])
    print("accepted %d / rejected %d" % (accepted, rejected))

    groups = collections.defaultdict(list)
    for rel in manifests:
        verdict, _ = classify(rel)
        if verdict not in ("A", "B", "C-accept"):
            continue
        try:
            name = json.loads((ROOT / rel).read_text()).get("name")
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        groups[(name, plugin_root(rel, verdict))].append(rel)

    print("\ndedup by (name, plugin root)")
    print("  accepted manifests %d" % sum(len(v) for v in groups.values()))
    print("  logical plugins    %d" % len(groups))
    for (name, root), rels in sorted(groups.items(),
                                     key=lambda kv: (kv[0][0] or "", kv[0][1])):
        if len(rels) > 1:
            print("  %s @ %s collapses %d manifests" % (name, root, len(rels)))

    # An accepted manifest with no name is a plugin the inventory cannot label.
    # web/i18n/en-US/plugin.json reaches here because its directory holds a
    # literal skill.json, which the exact-name marker list admits.
    nameless = sorted(rel for (name, _), rels in groups.items()
                      if not name for rel in rels)
    if nameless:
        print("\naccepted but carries no name field (%d)" % len(nameless))
        for rel in nameless:
            print("  %s" % rel)

    declarations = []
    for dirpath, _, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep) or "settings.json" not in filenames:
            continue
        rel = str(pathlib.Path(dirpath).relative_to(ROOT) / "settings.json")
        try:
            obj = json.loads((ROOT / rel).read_text())
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        enabled = obj.get("enabledPlugins")
        if isinstance(enabled, dict):
            declarations.append((rel, enabled))

    print("\ndeclaration surfaces")
    for rel, enabled in sorted(declarations):
        print("  %s" % rel)
        for key, value in enabled.items():
            name, _, marketplace = key.rpartition("@")
            print("    name=%-26s marketplace=%-26s enabled=%s"
                  % (repr(name), repr(marketplace), value))

    # ---- linkage: skills and MCP servers to their plugin --------------------
    roots = plugin_roots(manifests)
    contents = content_files()

    print("\nlinkage: content -> plugin")
    print("  plugin roots       %d" % len(roots))
    print("  content files      %d  (SKILL.md, .mcp.json, mcp.json)" % len(contents))

    nested_owned, root_only, unowned, multi = [], [], [], []
    for rel in contents:
        owners = owning_roots(rel, roots)
        if not owners:
            unowned.append(rel)
            continue
        if len(owners) > 1:
            multi.append((rel, owners))
        if owners[0] == ".":
            root_only.append(rel)
        else:
            nested_owned.append((rel, owners[0]))

    for rel, owner in nested_owned:
        names = sorted(roots[owner])
        expected = EXPECT_OWNER.get(rel)
        if expected is None:
            failures.append("no owner expectation recorded: %s -> %s" % (rel, names))
        elif expected not in names:
            failures.append("%s: expected owner %s, got %s"
                            % (rel, expected, names))
    for rel in EXPECT_OWNER:
        if rel not in dict(nested_owned):
            failures.append("owner fixture missing or not nested-owned: %s" % rel)

    print("  owned by a nested plugin   %d" % len(nested_owned))
    print("  owned only by a repo-root manifest %d" % len(root_only))
    print("  owned by no plugin         %d" % len(unowned))

    # Same content name under more than one plugin root: linkage must resolve by
    # containment, never by name.
    by_name = collections.defaultdict(set)
    for rel, owner in nested_owned:
        path = pathlib.Path(rel)
        key = path.parent.name if path.name == "SKILL.md" else path.name
        by_name[key].add(owner)
    collisions = {k: v for k, v in by_name.items() if len(v) > 1}
    print("\n  same content name under >1 plugin root (name matching would cross-link)")
    if not collisions:
        failures.append("no name-collision fixture: the cross-link trap is untested")
    for key, owners in sorted(collisions.items()):
        print("    %-14s %s" % (key, ", ".join(sorted(owners))))

    # MCP <-> plugin, both directions.
    print("\n  MCP servers declared inside a plugin root")
    mcp_pairs = 0
    for rel, owner in nested_owned:
        if pathlib.Path(rel).name not in (".mcp.json", "mcp.json"):
            continue
        try:
            servers = sorted(json.loads((ROOT / rel).read_text())
                             .get("mcpServers", {}))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        mcp_pairs += len(servers)
        print("    %-28s %s" % (sorted(roots[owner])[0], ", ".join(servers)))
    print("    %d plugin/server pairs across %d manifests"
          % (mcp_pairs, sum(1 for r, _ in nested_owned
                            if pathlib.Path(r).name in (".mcp.json", "mcp.json"))))

    # Where the two readings of "under the root" disagree.
    print("\n  containment vs nearest ancestor")
    print("    files with more than one owning root %d" % len(multi))
    deepest = max(multi, key=lambda kv: len(kv[1])) if multi else None
    if deepest:
        print("    deepest nesting: %s" % deepest[0])
        print("      owners innermost-first: %s" % ", ".join(deepest[1]))

    # ---- linkage: plugin to agent ------------------------------------------
    print("\nlinkage: plugin -> agent")
    attributed, unattributed = collections.defaultdict(list), []
    for rel in manifests:
        verdict, _ = classify(rel)
        if verdict not in ("A", "B", "C-accept"):
            continue
        parent = pathlib.Path(rel).parent.name
        agent = VENDOR_AGENT.get(parent)
        if agent:
            attributed[agent].append(rel)
        else:
            unattributed.append(rel)
    for rel, enabled in sorted(declarations):
        agent = DECLARATION_AGENT.get(rel)
        if agent:
            attributed[agent].extend("%s#%s" % (rel, k) for k in enabled)
    for agent in sorted(attributed):
        surface = "root surface present" if agent in ROOT_AGENT_SURFACES.values() \
                  else "NO root surface, nothing to link to"
        print("  %-12s %2d  (%s)" % (agent, len(attributed[agent]), surface))
    print("  %-12s %2d  (no vendor directory, no declaration: agent unknown)"
          % ("-", len(unattributed)))

    missing_surface = sorted(a for a in attributed
                             if a not in ROOT_AGENT_SURFACES.values())
    if missing_surface:
        print("\n  vendor named with no root agent surface in this repo:")
        print("    %s" % ", ".join(missing_surface))

    # A plugin declared in settings.json but shipping no manifest here.
    declared = {k.rpartition("@")[0] for _, e in declarations for k in e}
    shipped = {n for names in roots.values() for n in names}
    print("\n  declared in settings.json but no manifest in the repo:")
    print("    %s" % ", ".join(sorted(declared - shipped)))

    if failures:
        print("\nFAILED (%d)" % len(failures))
        for line in failures:
            print("  %s" % line)
        return 1
    print("\nOK: every fixture matches its recorded expectation")
    return 0


if __name__ == "__main__":
    sys.exit(main())

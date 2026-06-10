---
name: status
description: Use when the user wants MemPalace health, counts, storage state, hook activity, MCP availability, or a quick palace overview.
allowed-tools: Bash, Read
---

# MemPalace Status

Report whether MemPalace is installed, reachable, populated, and healthy.

## When To Use

Use this skill for health checks, palace counts, storage inspection, hook diagnostics, MCP availability checks, or quick summaries of what is stored.

Do not use this skill to mine or search content beyond a small verification query.

## Workflow

1. Check CLI availability:

```bash
mempalace --version
```

If unavailable, report that setup is incomplete and route to `init`.

2. Run the main status command:

```bash
mempalace status
```

3. If MCP tools are available, prefer structured status from `mempalace_status` and supplement with:

- `mempalace_kg_stats` for knowledge graph counts.
- `mempalace_graph_stats` for connectivity.
- `mempalace_list_wings` for a compact wing list.

4. For hook diagnostics, inspect:

```bash
ls -la ~/.mempalace/hook_state
tail -50 ~/.mempalace/hook_state/hook.log
```

If the hook log is absent, say that no local hook activity was observed yet. Do not treat absence as proof the plugin is broken.

5. For Codex plugin status, use:

```bash
codex plugin list
```

Confirm whether `mempalace@mempalace` is installed and enabled when relevant.

## Verification

Status is verified by a successful `mempalace status` or structured MCP status response. Hook health is verified by trusted hooks plus recent hook log activity, not by plugin installation alone.

## Output Style

Use a compact summary:

- CLI version
- Total drawers
- Wings and largest rooms
- MCP configured or unavailable
- Hook activity observed or not observed
- One recommended next action

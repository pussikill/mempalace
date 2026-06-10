---
name: help
description: Use when the user asks what MemPalace can do, how to use MemPalace commands, MCP tools, hooks, skills, setup, mining, search, status, or troubleshooting.
allowed-tools: Bash, Read
---

# MemPalace Help

MemPalace is a local AI memory system. It stores project and conversation content in a palace made of wings, rooms, closets, and drawers, then exposes search and write operations through CLI commands and MCP tools.

## When To Use

Use this skill when the user asks about MemPalace capabilities, available commands, setup flow, MCP tools, auto-save hooks, mining, searching, or general troubleshooting.

Do not use this skill for generic memory concepts when the user is not asking about MemPalace. For actual setup, mining, search, or status work, prefer the more specific MemPalace skill after giving any requested orientation.

## Workflow

1. Check whether the CLI is available:

```bash
mempalace --version
```

If the command fails, explain that MemPalace is not on PATH and direct the user to the `init` skill.

2. Give the shortest useful map of the system:

- CLI: `mempalace init`, `mempalace mine`, `mempalace search`, `mempalace status`, `mempalace mcp`, `mempalace hook run`.
- MCP: prefer MCP tools when available because they return structured data.
- Hooks: Codex `SessionStart`, `Stop`, and `PreCompact` hooks preserve session context.
- Storage: local `~/.mempalace` palace data, no cloud service required by default.

3. If the user asks for tool inventory, list these groups:

- Palace read: status, list wings, list rooms, taxonomy, search, duplicate check, AAAK spec.
- Palace write: add drawer, delete drawer.
- Knowledge graph: query, add, invalidate, timeline, stats.
- Navigation: traverse, tunnels, graph stats.
- Agent diary: diary write and diary read.

4. Route the user to the right next action:

- New install or broken CLI: use `init`.
- Add project or conversation data: use `mine`.
- Retrieve stored knowledge: use `search`.
- Inspect health and counts: use `status`.
- Hook issue: inspect Codex `/hooks`, trust state, and `~/.mempalace/hook_state/hook.log`.

## Verification

For CLI availability, trust only a successful `mempalace --version` run. For MCP availability, use the currently available MCP tool list; do not assume MCP is configured just because the CLI exists.

## Output Style

Keep help answers concise. Give commands the user can run, but do not run setup or mining commands unless the user asks for that action.

---
name: search
description: Use when the user wants to search, recall, retrieve, inspect, compare, or navigate memories stored in MemPalace.
allowed-tools: Bash, Read
---

# MemPalace Search

Retrieve relevant memories from MemPalace with source context.

## When To Use

Use this skill when the user asks what they previously decided, remembered, mined, discussed, implemented, debugged, or stored in MemPalace.

Do not use this skill for web search or for mining new data.

## Workflow

1. Extract the query. Preserve names, project terms, dates, error messages, and exact phrases.

2. Identify optional scope:

- Wing: top-level project, person, or domain.
- Room: topic within a wing.
- Global: use when scope is unclear.

3. Prefer MCP tools when available:

- `mempalace_search` for semantic search.
- `mempalace_list_wings` when resolving a wing.
- `mempalace_list_rooms` when resolving a room.
- `mempalace_get_taxonomy` for a broad map.
- `mempalace_traverse` for related memories.
- `mempalace_find_tunnels` for cross-wing relationships.

4. If MCP tools are unavailable, use CLI fallback:

```bash
mempalace search "<query>"
mempalace search "<query>" --wing <wing>
mempalace search "<query>" --wing <wing> --room <room>
```

5. Present results with provenance:

- Wing
- Room
- Drawer or source identifier when available
- Score or rank when available
- Short quote or concise summary

6. If results are weak, refine once before giving up:

- Broaden by removing wing or room.
- Search exact names or error text.
- List wings/rooms to find the right scope.

## Verification

Do not claim there are no memories unless a real MCP or CLI search completed successfully. If the tool is unavailable, say the search could not be performed and give the setup command or `init` next step.

## Output Style

Lead with the answer, then show the supporting memories. Keep raw output short unless the user asks for full details.

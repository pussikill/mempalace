---
name: mine
description: Use when the user wants to add projects, files, notes, chat exports, Codex/Claude sessions, or other source material into MemPalace.
allowed-tools: Bash, Read, Glob, Grep
---

# MemPalace Mine

Mine source material into MemPalace so it can be searched later.

## When To Use

Use this skill when the user asks to import, index, mine, remember, save, or preserve project files, documentation, notes, conversation exports, or session transcripts.

Do not use this skill for searching existing memory. Use `search` instead.

## Workflow

1. Identify the source path. If the user did not provide one, ask for it. Use the current working directory only when the user clearly wants this project mined.

2. Classify the source:

- Project files, code, docs, notes: project mining.
- Conversation exports or agent session JSONL: conversation mining.
- Mixed conversation content where decisions/problems/milestones matter: conversation mining with general extraction.

3. Check CLI availability:

```bash
mempalace --version
```

If unavailable, stop and use `init`.

4. For very large transcript files, preview splitting first:

```bash
mempalace split <dir> --dry-run
```

Only run the non-dry split after explaining what will change.

5. Build the mining command:

```bash
mempalace mine <dir>
mempalace mine <dir> --mode convos
mempalace mine <dir> --mode convos --extract general
```

Add a wing only when the user names one:

```bash
mempalace mine <dir> --wing <wing_name>
```

6. Run the selected command and watch the output. Report skipped files, warnings, or errors instead of hiding them.

7. Verify that data landed:

```bash
mempalace status
```

For a targeted check, run a small search using a distinctive term from the source.

## Verification

Mining is verified by successful command exit plus changed status counts or a search result from the newly mined material. If counts do not change, report that explicitly and inspect whether the content was already mined or skipped.

## Safety Notes

Do not mine secrets, credential dumps, private keys, or unrelated home directories without explicit user consent. Prefer the smallest directory that contains the intended source material.

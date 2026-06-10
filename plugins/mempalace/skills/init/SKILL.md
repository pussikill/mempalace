---
name: init
description: Use when the user wants to install, initialize, repair setup, configure MCP, verify hooks, or make MemPalace available to Codex.
allowed-tools: Bash, Read, Write, Edit
---

# MemPalace Init

Set up MemPalace so the CLI, local palace storage, MCP server, and Codex plugin hooks can work together.

## When To Use

Use this skill for first-time setup, broken setup, missing `mempalace` command, MCP configuration, plugin verification, hook troubleshooting, or when the user asks to make MemPalace work in Codex.

Do not mine user data during init unless the user explicitly asks. Setup should leave the system ready and verified.

## Workflow

1. Confirm Python:

```bash
python3 --version
```

Python must be 3.9 or newer. If `python3` is unavailable, try `python --version`.

2. Check CLI availability:

```bash
mempalace --version
```

If this succeeds, keep the installed version and continue. If it fails, install with the first available option:

```bash
uv tool install mempalace
```

Fallbacks, in order:

```bash
pip install mempalace
pip3 install mempalace
python3 -m pip install mempalace
python -m pip install mempalace
```

3. Choose the palace seed directory. Use the current working directory as the default when the user has not named a directory. Do not guess a different project.

4. Initialize:

```bash
mempalace init --yes <dir>
```

5. Configure Codex MCP when Codex is the target client:

```bash
codex mcp add mempalace -- mempalace-mcp
```

If MCP already exists, verify rather than duplicating config.

6. Verify the installed plugin state when the user is using the Codex plugin:

```bash
codex plugin list
```

Confirm `mempalace@mempalace` is installed and enabled when that marketplace is expected.

7. Verify hooks:

- Ask the user to open `/hooks` in Codex if hook trust is pending.
- Check `~/.codex/config.toml` for the plugin enabled entry only when local file access is appropriate.
- Check `~/.mempalace/hook_state/hook.log` after a session-start or manual hook test.

8. Final health check:

```bash
mempalace status
```

## Verification

Setup is not complete until `mempalace --version` and `mempalace status` both run successfully. MCP setup is verified only by Codex config or an available `mempalace` MCP tool. Hook setup is verified by `/hooks` trust state or hook log activity.

## Failure Handling

If install fails with native build errors, tell the user which dependency failed and suggest platform build tools. If Codex MCP configuration fails, continue with CLI verification and report MCP as the remaining setup gap.

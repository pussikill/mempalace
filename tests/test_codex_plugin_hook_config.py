"""Schema tests for the Codex plugin hook config."""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK_CONFIGS = [
    REPO_ROOT / ".codex-plugin" / "hooks.json",
    REPO_ROOT / "plugins" / "mempalace" / "hooks" / "hooks.json",
    REPO_ROOT / "plugins" / "mempalace" / ".codex-plugin" / "hooks.json",
]

EVENT_TIMEOUT_BOUNDS: dict[str, tuple[int, int]] = {
    "SessionStart": (5, 10),
    "Stop": (30, 60),
    "PreCompact": (90, 120),
}


@pytest.mark.parametrize("hook_config_path", HOOK_CONFIGS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_codex_plugin_hook_timeout_within_bounds(hook_config_path: Path) -> None:
    """Codex hook commands must not fall back to the 600s default timeout."""
    hook_config = json.loads(hook_config_path.read_text(encoding="utf-8"))

    assert set(hook_config.get("hooks", {})) == set(EVENT_TIMEOUT_BOUNDS)
    for event, entries in hook_config["hooks"].items():
        floor, ceiling = EVENT_TIMEOUT_BOUNDS[event]
        assert len(entries) == 1
        sub_hooks = entries[0].get("hooks")
        assert isinstance(sub_hooks, list) and len(sub_hooks) == 1
        hook = sub_hooks[0]
        assert hook.get("type") == "command"
        assert "statusMessage" in hook
        timeout = hook.get("timeout")
        assert isinstance(timeout, int) and not isinstance(timeout, bool)
        assert floor <= timeout <= ceiling


@pytest.mark.parametrize("hook_config_path", HOOK_CONFIGS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_codex_plugin_hook_commands_use_plugin_root(hook_config_path: Path) -> None:
    """Installed plugin hooks must resolve from CODEX_PLUGIN_ROOT."""
    hook_config = json.loads(hook_config_path.read_text(encoding="utf-8"))

    for entries in hook_config["hooks"].values():
        command = entries[0]["hooks"][0]["command"]
        assert "${CODEX_PLUGIN_ROOT}/hooks/mempal-hook.sh" in command

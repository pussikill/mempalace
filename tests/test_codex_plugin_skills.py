"""Quality checks for bundled Codex skills."""

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = [
    REPO_ROOT / "skills",
    REPO_ROOT / ".codex-plugin" / "skills",
    REPO_ROOT / "plugins" / "mempalace" / "skills",
    REPO_ROOT / "plugins" / "mempalace" / ".codex-plugin" / "skills",
]
SKILL_NAMES = ["help", "init", "mine", "search", "status"]


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
@pytest.mark.parametrize("skill_name", SKILL_NAMES)
def test_codex_skill_contains_operational_workflow(skill_dir: Path, skill_name: str) -> None:
    path = skill_dir / skill_name / "SKILL.md"
    content = path.read_text(encoding="utf-8")

    assert "## When To Use" in content
    assert "## Workflow" in content
    assert "## Verification" in content
    assert "mempalace instructions" not in content
    assert len(content.splitlines()) >= 35

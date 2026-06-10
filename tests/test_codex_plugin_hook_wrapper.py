"""Execution tests for Codex plugin hook wrapper scripts."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATHS = [
    REPO_ROOT / ".codex-plugin" / "hooks" / "mempal-hook.sh",
    REPO_ROOT / "plugins" / "mempalace" / "hooks" / "mempal-hook.sh",
    REPO_ROOT / "plugins" / "mempalace" / ".codex-plugin" / "hooks" / "mempal-hook.sh",
]
BASH = shutil.which("bash")

pytestmark = pytest.mark.skipif(BASH is None, reason="bash required for Codex hook wrapper tests")


def _shell_path(path: Path) -> str:
    return path.as_posix()


def _write_executable(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")
    path.chmod(0o755)


def _make_bin_dir(tmp_path: Path, executables: dict[str, str]) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, content in executables.items():
        _write_executable(bin_dir / name, content)
    return bin_dir


def _capture_stdin_to(output_path: Path) -> str:
    return (
        'stdin_payload=""\n'
        'while IFS= read -r line || [ -n "$line" ]; do\n'
        '  stdin_payload="${stdin_payload}${line}"\n'
        "done\n"
        f'printf \'%s\' "$stdin_payload" > "{_shell_path(output_path)}"\n'
    )


def _run_hook(script_path: Path, hook_name: str, payload: str, bin_dir: Path) -> subprocess.CompletedProcess[str]:
    assert BASH is not None

    env = os.environ.copy()
    env["PATH"] = str(bin_dir)
    env["CODEX_PLUGIN_ROOT"] = str(script_path.parents[1])

    return subprocess.run(
        [BASH, _shell_path(script_path), hook_name],
        input=payload,
        text=True,
        capture_output=True,
        cwd=REPO_ROOT,
        env=env,
    )


@pytest.mark.parametrize("script_path", SCRIPT_PATHS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_codex_hook_wrapper_prefers_mempalace_cli(tmp_path: Path, script_path: Path) -> None:
    args_file = tmp_path / "args.txt"
    stdin_file = tmp_path / "stdin.json"
    bin_dir = _make_bin_dir(
        tmp_path,
        {
            "mempalace": (
                "#!/bin/sh\n"
                f'printf \'%s\' "$*" > "{_shell_path(args_file)}"\n'
                f"{_capture_stdin_to(stdin_file)}"
                "printf '{}\\n'\n"
            ),
            "python": "#!/bin/sh\nexit 99\n",
            "python3": "#!/bin/sh\nexit 99\n",
        },
    )

    payload = '{"session_id":"abc123"}'
    result = _run_hook(script_path, "stop", payload, bin_dir)

    assert result.returncode == 0
    assert result.stdout == "{}\n"
    assert args_file.read_text(encoding="utf-8") == "hook run --hook stop --harness codex"
    assert stdin_file.read_text(encoding="utf-8") == payload


@pytest.mark.parametrize("script_path", SCRIPT_PATHS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
@pytest.mark.parametrize("python_name", ["python3", "python"])
def test_codex_hook_wrapper_falls_back_to_importable_python(
    tmp_path: Path, script_path: Path, python_name: str
) -> None:
    args_file = tmp_path / "args.txt"
    stdin_file = tmp_path / "stdin.json"
    python_stub = (
        "#!/bin/sh\n"
        'if [ "$1" = "-c" ]; then\n'
        "  exit 0\n"
        "fi\n"
        f'printf \'%s\' "$*" > "{_shell_path(args_file)}"\n'
        f"{_capture_stdin_to(stdin_file)}"
        "printf '{}\\n'\n"
    )
    bin_dir = _make_bin_dir(tmp_path, {python_name: python_stub})

    payload = '{"session_id":"xyz789"}'
    result = _run_hook(script_path, "precompact", payload, bin_dir)

    assert result.returncode == 0
    assert result.stdout == "{}\n"
    assert args_file.read_text(encoding="utf-8") == "-m mempalace hook run --hook precompact --harness codex"
    assert stdin_file.read_text(encoding="utf-8") == payload


@pytest.mark.parametrize("script_path", SCRIPT_PATHS, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_codex_hook_wrapper_errors_cleanly_when_no_runner_exists(
    tmp_path: Path, script_path: Path
) -> None:
    bin_dir = _make_bin_dir(tmp_path, {})

    result = _run_hook(script_path, "session-start", '{"session_id":"none"}', bin_dir)

    assert result.returncode != 0
    assert result.stdout == ""
    assert "could not find a runnable mempalace command or module" in result.stderr

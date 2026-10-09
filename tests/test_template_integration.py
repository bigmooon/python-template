"""End-to-end test for creating a project from this template."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run(
    project: Path,
    *command: str,
    env: dict[str, str],
    check: bool = True,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=project,
        env=env,
        check=check,
        capture_output=capture_output,
        text=True,
        timeout=300,
    )


@pytest.mark.integration
def test_initialized_project_workflow_and_partial_staging(tmp_path: Path) -> None:
    project = tmp_path / "sample-project"
    ignored = shutil.ignore_patterns(
        ".git",
        ".venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "__pycache__",
        "*.egg-info",
    )
    shutil.copytree(ROOT, project, ignore=ignored)
    run(project, "git", "init", "-q", env=dict(os.environ))
    environment = {**os.environ, "PYTHON": sys.executable}

    run(project, "make", "init", "NAME=sample_project", env=environment)
    run(project, "make", "install-dev", env=environment)
    run(project, "make", "ci-check", env=environment)

    assert (project / "src" / "sample_project" / "__init__.py").is_file()
    assert not (project / "src" / "your_project").exists()

    run(project, "git", "config", "user.name", "Template Integration", env=environment)
    run(
        project,
        "git",
        "config",
        "user.email",
        "integration@example.com",
        env=environment,
    )
    probe = project / "src" / "sample_project" / "hook_probe.py"
    probe.write_text("value = 1\n", encoding="utf-8")
    run(project, "git", "add", ".", env=environment)
    run(
        project,
        "git",
        "-c",
        "core.hooksPath=/dev/null",
        "commit",
        "-qm",
        "test: baseline",
        env=environment,
    )

    probe.write_text("value=2\n", encoding="utf-8")
    run(project, "git", "add", str(probe.relative_to(project)), env=environment)
    probe.write_text("value=3\n", encoding="utf-8")
    hook_environment = {
        **environment,
        "PRE_COMMIT_HOME": str(tmp_path / "pre-commit-cache"),
    }
    hook = run(
        project,
        str(project / ".venv" / "bin" / "pre-commit"),
        "run",
        "--hook-stage",
        "pre-commit",
        env=hook_environment,
        check=False,
        capture_output=True,
    )

    cached = run(
        project,
        "git",
        "show",
        ":src/sample_project/hook_probe.py",
        env=environment,
        capture_output=True,
    )
    assert hook.returncode == 1, hook.stdout + hook.stderr
    assert "index는 변경하지 않았습니다" in hook.stdout + hook.stderr
    assert cached.stdout == "value=2\n"
    assert probe.read_text(encoding="utf-8") == "value=3\n"

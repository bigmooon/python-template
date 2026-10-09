"""Unit tests for the fail-only formatter review hook."""

from __future__ import annotations

from pathlib import Path
import subprocess

import pytest
from scripts import stage_fixes


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def create_repository(tmp_path: Path) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.name", "Template Tests")
    git(repo, "config", "user.email", "tests@example.com")
    target = repo / "sample.py"
    target.write_text("value = 1\n", encoding="utf-8")
    git(repo, "add", "sample.py")
    git(repo, "commit", "-qm", "test: initial")
    return repo, target


def test_main_reports_hook_fix_without_changing_index(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repo, target = create_repository(tmp_path)
    target.write_text("value=2\n", encoding="utf-8")
    git(repo, "add", "sample.py")
    target.write_text("value = 2\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    cached_before = git(repo, "show", ":sample.py")
    assert stage_fixes.main(["sample.py"]) == 1

    assert git(repo, "show", ":sample.py") == cached_before == "value=2\n"
    assert target.read_text(encoding="utf-8") == "value = 2\n"
    assert "git add -p" in capsys.readouterr().err


def test_main_preserves_partial_staging_on_same_hunk(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, target = create_repository(tmp_path)
    target.write_text("value=2\n", encoding="utf-8")
    git(repo, "add", "sample.py")
    target.write_text("value=3\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    assert stage_fixes.main(["sample.py"]) == 1

    assert git(repo, "show", ":sample.py") == "value=2\n"
    assert target.read_text(encoding="utf-8") == "value=3\n"


def test_main_ignores_empty_or_unrelated_file_lists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo, target = create_repository(tmp_path)
    target.write_text("value = 2\n", encoding="utf-8")
    monkeypatch.chdir(repo)

    assert stage_fixes.main([]) == 0
    assert stage_fixes.main(["other.py"]) == 0

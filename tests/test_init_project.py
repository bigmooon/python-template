"""Unit tests for the template initialization script."""

from __future__ import annotations

from pathlib import Path

import pytest
from scripts import init_project


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("my_app", "my_app"),
        ("My-App", "my_app"),
        ("my app", "my_app"),
    ],
)
def test_to_snake_normalizes_supported_names(raw: str, expected: str) -> None:
    assert init_project.to_snake(raw) == expected


@pytest.mark.parametrize("raw", ["123-app", "has.dot", "한글"])
def test_to_snake_rejects_invalid_package_names(raw: str) -> None:
    with pytest.raises(ValueError, match="유효한 Python 패키지명"):
        init_project.to_snake(raw)


def test_to_kebab_normalizes_distribution_name() -> None:
    assert init_project.to_kebab("My_project name") == "my-project-name"


def test_replace_in_file_updates_both_placeholders(tmp_path: Path) -> None:
    target = tmp_path / "example.txt"
    target.write_text("your-project imports your_project\n", encoding="utf-8")

    init_project.replace_in_file(target, "sample_app", "sample-app")

    assert target.read_text(encoding="utf-8") == ("sample-app imports sample_app\n")


def test_replace_in_file_leaves_unrelated_content_unchanged(tmp_path: Path) -> None:
    target = tmp_path / "example.txt"
    target.write_text("already initialized\n", encoding="utf-8")

    init_project.replace_in_file(target, "sample_app", "sample-app")

    assert target.read_text(encoding="utf-8") == "already initialized\n"


def test_main_renames_package_and_updates_template_files(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    package = tmp_path / "src" / "your_project"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text('NAME = "your-project"\n', encoding="utf-8")
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_smoke.py").write_text("import your_project\n", encoding="utf-8")
    for filename in (
        "pyproject.toml",
        "CLAUDE.md",
        "README.md",
        "Makefile",
        "requirements-dev.lock",
    ):
        (tmp_path / filename).write_text(
            "your-project / your_project\n", encoding="utf-8"
        )

    assert init_project.main("Sample_App", root=tmp_path) == 0

    renamed = tmp_path / "src" / "sample_app"
    assert renamed.is_dir()
    assert not package.exists()
    assert "sample-app" in (renamed / "__init__.py").read_text(encoding="utf-8")
    assert "import sample_app" in (tests / "test_smoke.py").read_text(encoding="utf-8")
    assert "sample-app / sample_app" in (tmp_path / "README.md").read_text(
        encoding="utf-8"
    )
    assert "snake=sample_app, kebab=sample-app" in capsys.readouterr().out


def test_main_refuses_to_overwrite_existing_package(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "src" / "your_project").mkdir(parents=True)
    destination = tmp_path / "src" / "sample_app"
    destination.mkdir()

    assert init_project.main("sample_app", root=tmp_path) == 1

    assert "이미 존재합니다" in capsys.readouterr().err
    assert (tmp_path / "src" / "your_project").is_dir()
    assert destination.is_dir()


def test_main_is_safe_when_optional_template_files_are_missing(tmp_path: Path) -> None:
    package = tmp_path / "src" / "your_project"
    package.mkdir(parents=True)

    assert init_project.main("your_project", root=tmp_path) == 0

    assert package.is_dir()

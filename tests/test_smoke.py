"""Smoke test — anchors the test suite so pytest never returns exit code 5.

Replace or expand this as your project grows. The template ships with one
test on purpose: pytest treats "0 tests collected" as a failure (exit 5),
which would block the pre-push gate on every fresh clone.
"""

from __future__ import annotations

import your_project


def test_package_imports() -> None:
    assert your_project is not None


def test_version_is_a_string() -> None:
    assert isinstance(your_project.__version__, str)
    assert your_project.__version__

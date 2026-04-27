"""pre-commit이 넘긴 원본 staged 파일 목록만 다시 git add.

pre-commit 프레임워크는 훅에 "원래 staged였던 파일 목록"을 인자로 넘긴다
(즉 ``git diff --cached --name-only --diff-filter=ACMR``). Ruff/Ruff-format
같은 자동수정 훅이 그 파일들을 수정한 뒤, 이 스크립트가 동일 목록만
정확히 다시 ``git add``하여 자동수정 결과를 같은 커밋에 포함시킨다.

``git add -A``/``git add -u``를 의도적으로 회피하여
``git add -p`` 부분 stage 워크플로우의 unstaged hunk가 함께 끌려가는
사고를 방지한다.
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main(files: list[str]) -> int:
    if not files:
        return 0

    existing = [f for f in files if Path(f).exists()]
    if not existing:
        return 0

    subprocess.run(["git", "add", "--", *existing], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

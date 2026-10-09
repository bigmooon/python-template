"""pre-commit이 넘긴 파일 중 실제 staged 파일만 다시 git add.

일반 commit에서는 pre-commit이 staged 파일을 넘기지만 ``--all-files``로
실행하면 모든 tracked 파일을 넘긴다. 따라서 현재 index의 staged 파일을
다시 조회하고 전달받은 목록과의 교집합만 ``git add``한다.

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

    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
        check=True,
        capture_output=True,
        text=True,
    )
    staged = {f for f in result.stdout.split("\0") if f}
    existing = [f for f in files if f in staged and Path(f).exists()]
    if not existing:
        return 0

    subprocess.run(["git", "add", "--", *existing], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

"""Ruff가 수정한 staged 파일을 커밋하지 않도록 안내한다.

이 훅은 의도적으로 index를 변경하지 않는다. pre-commit은 부분 stage된
파일의 unstaged hunk를 임시로 숨긴 뒤 훅을 실행한다. 이 중에 ``git add``로
index를 바꾸면 자동 수정과 숨겨진 hunk가 같은 부분에서 충돌할 때
사용자의 unstaged 변경을 복원하지 못할 수 있다.

따라서 Ruff 후 staged 파일에 worktree 변경이 생기면 실패 메시지만
출력한다. 사용자가 ``git diff``와 ``git diff --cached``를 확인한 뒤
``git add -p``로 원하는 hunk만 다시 stage하는 것이 안전한 워크플로우다.
"""

from __future__ import annotations

import subprocess
import sys


def git_paths(*args: str) -> set[str]:
    """Git의 NUL 구분 파일 목록을 set으로 반환한다."""
    result = subprocess.run(
        ["git", *args, "-z"],
        check=True,
        capture_output=True,
        text=True,
    )
    return {path for path in result.stdout.split("\0") if path}


def files_requiring_review(files: list[str]) -> list[str]:
    """Staged이면서 worktree에도 변경이 있는 전달 파일을 찾는다."""
    if not files:
        return []
    staged = git_paths("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    modified = git_paths("diff", "--name-only", "--diff-filter=ACMR")
    return sorted(set(files) & staged & modified)


def main(files: list[str]) -> int:
    review = files_requiring_review(files)
    if not review:
        return 0

    print(
        "Ruff가 staged 파일을 수정했습니다. index는 변경하지 않았습니다.\n"
        "다음 파일을 검토한 뒤 `git add -p`로 원하는 hunk만 stage하세요:\n"
        + "\n".join(f"  - {path}" for path in review),
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

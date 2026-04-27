"""your-project / your_project 플레이스홀더를 새 프로젝트명으로 일괄 치환.

크로스플랫폼(macOS/Linux/Windows) 안전. ``sed -i`` 변종 차이를 피하려고
Python stdlib만 사용한다.

치환 규칙:
- ``your-project`` → kebab-case 이름 (PEP 503 정규화)
- ``your_project`` → snake_case 이름 (Python 패키지명)
- ``src/your_project/`` 디렉토리 → ``src/<snake>/``로 이동

사용:
    python scripts/init_project.py my_app
    # 또는 Makefile 경유:
    make init NAME=my_app
"""

from __future__ import annotations

from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parent.parent


def to_snake(name: str) -> str:
    """패키지명용 snake_case로 정규화."""
    cleaned = re.sub(r"[-\s]+", "_", name).lower()
    if not re.fullmatch(r"[a-z_][a-z0-9_]*", cleaned):
        msg = (
            f"'{name}'은 유효한 Python 패키지명이 아닙니다 "
            "(영문 소문자/숫자/언더스코어만 허용, 숫자로 시작 금지)"
        )
        raise ValueError(msg)
    return cleaned


def to_kebab(name: str) -> str:
    """배포용 kebab-case로 정규화."""
    return re.sub(r"[_\s]+", "-", name).lower()


def replace_in_file(path: Path, snake: str, kebab: str) -> None:
    text = path.read_text(encoding="utf-8")
    new = text.replace("your-project", kebab).replace("your_project", snake)
    if new != text:
        path.write_text(new, encoding="utf-8")


def main(name: str) -> int:
    snake = to_snake(name)
    kebab = to_kebab(name)

    src_old = ROOT / "src" / "your_project"
    src_new = ROOT / "src" / snake
    if src_old.exists() and src_old != src_new:
        if src_new.exists():
            print(f"오류: {src_new}가 이미 존재합니다.", file=sys.stderr)
            return 1
        shutil.move(str(src_old), str(src_new))

    targets = [
        ROOT / "pyproject.toml",
        src_new / "__init__.py",
    ]
    for f in targets:
        if f.exists():
            replace_in_file(f, snake, kebab)

    print(
        f"✓ '{name}' (snake={snake}, kebab={kebab})로 초기화 완료.\n"
        "다음 단계: make install-dev && make ci-check"
    )
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/init_project.py <project_name>",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        sys.exit(main(sys.argv[1]))
    except ValueError as exc:
        print(f"오류: {exc}", file=sys.stderr)
        sys.exit(1)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python 3.12 프로젝트 템플릿. Ruff(린터+포매터), pre-commit 훅, Commitizen(Conventional Commits)을 통한 자동화된 코드 품질 검사 시스템.

## Commands

```bash
# 개발 환경 설치 (venv + dev deps + git hooks)
make install-dev

# 린트 (자동 수정 포함)
make lint

# 포매팅
make format

# 코드 스타일 검사 (lint + format)
make check

# 커밋 전 전체 검증 (lint + format + test + typecheck)
make validate

# CI용 검사 (수정 없이 검증만)
make ci-check

# 테스트 (pytest + coverage)
make test

# 타입 검사 (mypy)
make typecheck

# 대화형 커밋 (Conventional Commits)
make commit

# 버전 자동 증가 + 태그
make bump-version

# 캐시 정리
make clean
```

Ruff 직접 실행:
```bash
.venv/bin/ruff check src tests --fix
.venv/bin/ruff format src tests
```

## Architecture

- `src/your_project/` — 소스 코드 패키지 (TODO: 프로젝트명으로 변경)
- `tests/` — 테스트 디렉토리
- `pyproject.toml` — 프로젝트 메타데이터, Ruff 설정, Commitizen 설정 통합
- `.pre-commit-config.yaml` — Git 훅 (파일 검사, Ruff, Commitizen)
- `Makefile` — 개발 자동화 명령어

## Code Style

- Ruff 린터: E, W, F, I, N, UP, B, C4, SIM, PTH, RUF, S(보안), T20(print 감지) 규칙 활성화
- Ruff 포매터: Black 호환 (double quotes, 88자)
- mypy: strict 모드
- import 정렬: isort via Ruff (`known-first-party = ["your_project"]` — 프로젝트명에 맞게 변경 필요)

## Commit Convention

`<type>(<scope>): <subject>` 형식. Commitizen이 commit-msg 훅에서 검증.

허용 타입: `feat`, `fix`, `docs`, `refactor`, `chore`, `revert`, `perf`

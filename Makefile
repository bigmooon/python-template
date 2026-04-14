# ============================================================================
# Makefile - Python 프로젝트 개발 자동화
# Python 3.12+ 프로젝트용
# ============================================================================
# 사용법:
#   make help       - 사용 가능한 명령어 목록
#   make install    - 개발 환경 설치
#   make lint       - 코드 품질 검사
#   make format     - 코드 자동 포매팅
#   make check      - 전체 검사
#   make commit     - 대화형 커밋 생성
# ============================================================================

# ANSI 색상 코드
COLOR_RESET   := \033[0m
COLOR_BOLD    := \033[1m
COLOR_GREEN   := \033[32m
COLOR_YELLOW  := \033[33m
COLOR_BLUE    := \033[34m
COLOR_CYAN    := \033[36m

# 프로젝트 설정
PYTHON := python3.12
VENV := .venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTHON_VENV := $(VENV_BIN)/python

# 소스 디렉토리
SRC_DIR := src
TEST_DIR := tests
ALL_DIRS := $(SRC_DIR) $(TEST_DIR)

# 도구 실행 경로
RUFF := $(VENV_BIN)/ruff
PRE_COMMIT := $(VENV_BIN)/pre-commit
COMMITIZEN := $(VENV_BIN)/cz

# ============================================================================
# 기본 타겟
# ============================================================================
.DEFAULT_GOAL := help

.PHONY: help install install-dev install-hooks clean lint format \
        check ci-check validate test typecheck commit bump-version pre-commit run-all update-hooks

# ============================================================================
# help - 사용 가능한 명령어 목록
# ============================================================================
help:
	@echo "$(COLOR_BOLD)$(COLOR_CYAN)사용 가능한 Make 명령어:$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_GREEN)설치 관련:$(COLOR_RESET)"
	@echo "  make install         - 프로덕션 환경 설치"
	@echo "  make install-dev     - 개발 환경 전체 설치 (권장)"
	@echo "  make install-hooks   - Git 훅 설치"
	@echo "  make clean           - 임시 파일 및 캐시 삭제"
	@echo ""
	@echo "$(COLOR_GREEN)코드 품질:$(COLOR_RESET)"
	@echo "  make lint            - 코드 품질 검사 (자동 수정)"
	@echo "  make format          - 코드 포매팅 (자동 정리)"
	@echo "  make test            - 테스트 실행 (pytest + coverage)"
	@echo "  make typecheck       - 타입 검사 (mypy)"
	@echo ""
	@echo "$(COLOR_GREEN)통합 명령어:$(COLOR_RESET)"
	@echo "  make check           - 코드 스타일 검사 (lint+format)"
	@echo "  make validate        - 커밋 전 전체 검증 (lint+format+test+typecheck)"
	@echo "  make ci-check        - CI용 검사 (수정 없이 검증만)"
	@echo "  make pre-commit      - pre-commit 훅 수동 실행"
	@echo "  make run-all         - 모든 파일에 pre-commit 실행"
	@echo ""
	@echo "$(COLOR_GREEN)Git 관련:$(COLOR_RESET)"
	@echo "  make commit          - 대화형 커밋 생성 (Conventional Commits)"
	@echo "  make bump-version    - 버전 자동 증가 및 태그 생성"
	@echo ""
	@echo "$(COLOR_GREEN)유지보수:$(COLOR_RESET)"
	@echo "  make update-hooks    - pre-commit 훅 업데이트"
	@echo ""

# ============================================================================
# install - 프로덕션 환경 설치
# ============================================================================
install:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)프로덕션 환경 설치 중...$(COLOR_RESET)"
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e .
	@echo "$(COLOR_GREEN)✓ 설치 완료$(COLOR_RESET)"

# ============================================================================
# install-dev - 개발 환경 전체 설치 (권장)
# ============================================================================
install-dev:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)개발 환경 설치 중...$(COLOR_RESET)"
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e ".[dev]"
	@$(MAKE) install-hooks
	@echo "$(COLOR_GREEN)✓ 개발 환경 설치 완료$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)다음 명령어로 환경 활성화:$(COLOR_RESET)"
	@echo "  source $(VENV)/bin/activate"

# ============================================================================
# install-hooks - Git 훅 설치
# ============================================================================
install-hooks:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)Git 훅 설치 중...$(COLOR_RESET)"
	@$(PRE_COMMIT) install
	@$(PRE_COMMIT) install --hook-type commit-msg
	@echo "$(COLOR_GREEN)✓ Git 훅 설치 완료$(COLOR_RESET)"

# ============================================================================
# clean - 임시 파일 및 캐시 삭제
# ============================================================================
clean:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)임시 파일 삭제 중...$(COLOR_RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache 2>/dev/null || true
	@rm -rf .mypy_cache 2>/dev/null || true
	@rm -rf .ruff_cache 2>/dev/null || true
	@rm -rf build dist 2>/dev/null || true
	@echo "$(COLOR_GREEN)✓ 정리 완료$(COLOR_RESET)"

# ============================================================================
# lint - 코드 품질 검사 (자동 수정 포함)
# ============================================================================
lint:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)코드 품질 검사 중...$(COLOR_RESET)"
	@$(RUFF) check $(ALL_DIRS) --fix
	@echo "$(COLOR_GREEN)✓ 린트 검사 완료$(COLOR_RESET)"

# ============================================================================
# format - 코드 자동 포매팅
# ============================================================================
format:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)코드 포매팅 중...$(COLOR_RESET)"
	@$(RUFF) format $(ALL_DIRS)
	@echo "$(COLOR_GREEN)✓ 포매팅 완료$(COLOR_RESET)"

# ============================================================================
# check - 전체 검사 파이프라인 (로컬용, 자동 수정)
# ============================================================================
check: lint format
	@echo ""
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)========================================$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)  ✓ 모든 검사 통과!$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)========================================$(COLOR_RESET)"
	@echo ""

# ============================================================================
# validate - 커밋 전 전체 검증 (lint + format + test + typecheck)
# ============================================================================
validate: lint format test typecheck
	@echo ""
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)========================================$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)  ✓ 전체 검증 통과! 커밋 가능$(COLOR_RESET)"
	@echo "$(COLOR_BOLD)$(COLOR_GREEN)========================================$(COLOR_RESET)"
	@echo ""

# ============================================================================
# ci-check - CI용 검사 (수정 없이 검증만)
# ============================================================================
ci-check:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)CI 검사 중...$(COLOR_RESET)"
	@$(RUFF) check $(ALL_DIRS) --no-fix
	@$(RUFF) format $(ALL_DIRS) --check
	@$(VENV_BIN)/mypy $(SRC_DIR)
	@$(VENV_BIN)/pytest --no-header -q
	@echo "$(COLOR_GREEN)✓ CI 검사 통과$(COLOR_RESET)"

# ============================================================================
# test - 테스트 실행
# ============================================================================
test:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)테스트 실행 중...$(COLOR_RESET)"
	@$(VENV_BIN)/pytest
	@echo "$(COLOR_GREEN)✓ 테스트 완료$(COLOR_RESET)"

# ============================================================================
# typecheck - 타입 검사
# ============================================================================
typecheck:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)타입 검사 중...$(COLOR_RESET)"
	@$(VENV_BIN)/mypy $(SRC_DIR)
	@echo "$(COLOR_GREEN)✓ 타입 검사 완료$(COLOR_RESET)"

# ============================================================================
# pre-commit - pre-commit 훅 수동 실행 (staged 파일만)
# ============================================================================
pre-commit:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)Pre-commit 훅 실행 중...$(COLOR_RESET)"
	@$(PRE_COMMIT) run

# ============================================================================
# run-all - 모든 파일에 pre-commit 실행
# ============================================================================
run-all:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)모든 파일에 Pre-commit 실행 중...$(COLOR_RESET)"
	@$(PRE_COMMIT) run --all-files

# ============================================================================
# commit - 대화형 커밋 생성 (Conventional Commits)
# ============================================================================
commit:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)대화형 커밋 생성...$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_YELLOW)커밋 타입:$(COLOR_RESET)"
	@echo "  feat      - 새로운 기능"
	@echo "  fix       - 버그 수정"
	@echo "  docs      - 문서 변경"
	@echo "  refactor  - 리팩토링"
	@echo "  perf      - 성능 개선"
	@echo "  chore     - 기타 변경"
	@echo ""
	@$(COMMITIZEN) commit

# ============================================================================
# bump-version - 버전 자동 증가 및 태그 생성
# ============================================================================
bump-version:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)버전 자동 증가 중...$(COLOR_RESET)"
	@$(COMMITIZEN) bump --yes
	@echo "$(COLOR_GREEN)✓ 버전 업데이트 완료$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)다음 명령어로 푸시:$(COLOR_RESET)"
	@echo "  git push --follow-tags"

# ============================================================================
# update-hooks - pre-commit 훅 업데이트
# ============================================================================
update-hooks:
	@echo "$(COLOR_BOLD)$(COLOR_BLUE)Pre-commit 훅 업데이트 중...$(COLOR_RESET)"
	@$(PRE_COMMIT) autoupdate
	@echo "$(COLOR_GREEN)✓ 훅 업데이트 완료$(COLOR_RESET)"

# ============================================================================
# 개발 워크플로우 예시
# ============================================================================
# 1. 초기 설정:
#    make install-dev
#
# 2. 코드 작성 후:
#    make lint format
#
# 3. 커밋 전 전체 검사:
#    make check
#
# 4. 커밋:
#    git add .
#    make commit           # 또는 git commit (자동으로 pre-commit 실행)
#
# 5. 버전 업데이트 (릴리스시):
#    make bump-version
#    git push --follow-tags
# ============================================================================

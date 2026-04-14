# Python 3.12 자동화 검사 시스템

Python 3.12 기반의 자동화된 코드 품질 검사 시스템

## ✨ 주요 기능

### 자동화된 검사 시스템

- **Ruff**:

### Git 훅 자동 실행

```bash
git commit -m "feat: 커밋 메시지"
# ↓ 자동 실행
# 1. 파일 검사
# 2. Ruff 린팅 (자동 수정)
# 3. Ruff 포매팅 (자동 정리)
# 4. Commitizen (메시지 검증)
```

### 개발 편의성

- Makefile을 통한 원클릭 명령어
- 상세 에러 메시지 및 자동 수정
- IDE 무관

## 📦 사전 요구사항

```bash
# Python 3.12 이상 필수
python --version # Python 3.12.x

# Git 설치 확인
git --version
```

## 🚀 설치 방법

### 1. 프로젝트 설정

```bash
# 프로젝트 디렉토리로 이동
cd your-project

# 설정 파일들을 프로젝트 루트에 복사
# - pyproject.toml
# - .pre-commit-config.yaml
# - Makefile
# - .gitignore
```

### 2. 개발 환경 설치

```bash
# 개발 의존성 + Git 훅 자동 설치 (권장)
make install-dev

# 또는 수동 설치
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pre-commit install --hook-type commit-msg
```

## 💻 사용 방법

### 기본 워크플로우

```bash
# 1. 코드 작성 후 검사
make lint          # 코드 품질 검사 + 자동 수정
make format        # 코드 포매팅

# 2. 전체 검사 (CI/CD 파이프라인과 동일)
make check         # lint + format

# 3. 커밋 (자동으로 pre-commit 훅 실행)
git add .
git commit -m "feat(api): 사용자 인증 기능 추가"

# 또는 대화형 커밋
make commit
```

### Makefile 명령어 전체 목록

```bash
# 도움말
make help

# 설치
make install         # 프로덕션 환경
make install-dev     # 개발 환경 (권장)
make install-hooks   # Git 훅만 설치

# 코드 품질
make lint            # 린트 검사 + 자동 수정
make format          # 포매팅

# 통합
make check           # 전체 검사 파이프라인
make pre-commit      # pre-commit 수동 실행
make run-all         # 모든 파일에 pre-commit 실행

# Git
make commit          # 대화형 커밋 생성
make bump-version    # 버전 자동 증가

# 유지보수
make clean           # 캐시 삭제
make update-hooks    # pre-commit 훅 업데이트
```

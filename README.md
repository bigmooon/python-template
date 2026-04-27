# Python 3.12 프로젝트 템플릿

Python 3.12 프로젝트 자동화 검사 시스템. 이 템플릿 자체가 **체크 시스템의 최종 산물**입니다. — pre-commit과 pre-push 훅, 그리고 GitHub Actions CI가 깨진 코드나 포맷되지 않은 코드가 main에 절대 닿지 못하도록 보장합니다.

## 주요 기능

- **Ruff** — 린팅 + 포매팅을 한 도구로, **자동 수정**과 **자동 스테이징** 포함
- **mypy** — strict 모드 타입 검사
- **pytest + coverage** — 테스트와 80%+ 커버리지 게이트 (CI)
- **pre-commit + pre-push** — 2단계 훅 파이프라인
- **Commitizen** — Conventional Commits 강제
- **GitHub Actions CI** — `--no-verify` 우회에 대한 원격 안전망

## 아키텍처: 3중 안전망

```
git commit -m "feat: add user auth"
  ├─ pre-commit 단계 (빠른, 파일 단위 검사)
  │   ├─ 파일 끝 개행 / 줄 끝 공백
  │   ├─ YAML / TOML / JSON 문법 검사
  │   ├─ 시크릿 탐지 (개인 키, AWS 자격증명)
  │   ├─ 대용량 파일 차단 (>1MB)
  │   ├─ Ruff 린트 (--fix로 자동 수정)
  │   ├─ Ruff 포매팅
  │   └─ 자동 수정 파일 다시 stage
  └─ commit-msg 단계
      └─ Commitizen 메시지 검증

git push
  └─ pre-push 단계 (프로젝트 전체)
      ├─ pytest -x --no-cov -q  (빠른 실패 모드)
      └─ mypy src

GitHub Actions CI (main으로 push, PR)
  └─ make ci-check
      ├─ ruff check --no-fix
      ├─ ruff format --check
      ├─ mypy src
      └─ pytest --cov  (80% 게이트)
```

## 필수 사항

- Python 3.12 이상
- Git

## 빠른 시작

```bash
# 1. 저장소 복제
git clone https://github.com/bigmooon/python-template.git
cd python-template

# 2. 프로젝트명으로 초기화
make init NAME=my_app

# 3. 개발 환경 설치 (venv + 의존성 + git 훅)
make install-dev
```

## 일상 워크플로우

```bash
# 코드 편집 → add → commit → push (훅이 자동으로 검사)
git add src/foo.py
git commit -m "feat(foo): add bar"
git push
# pre-push에서 pytest + mypy 자동 실행
```

## 첫 커밋이 실패하는 이유 — 의도된 마찰

Ruff가 코드를 자동 수정하면(예: import 정렬, 따옴표 스타일), pre-commit은 **non-zero 종료 코드**를 반환하여 변경사항을 검토하게 합니다.

```bash
git add src/foo.py
git commit -m "feat: add foo"
# ⚠️  Ruff가 src/foo.py를 수정했음 — 첫 번째 커밋 실패
git commit -m "feat: add foo"
# ✓ 두 번째 시도 통과 (자동 수정이 이미 staged됨)
```

**의도**: Ruff가 적용한 diff를 사용자가 한 번 확인하도록 만들기 위함입니다.

내부 동작:
- Ruff 가 자동 수정하면 pre-commit은 non-zero로 종료됨
- `scripts/stage_fixes.py` 가 **원래 staged 되었던 파일만** 다시 `git add`
- `git add -p` 로 의도적으로 남긴 unstaged hunk는 보호됨 (휴리스틱)
- 두 번째 `git commit` 에서 통과

## 수동 검사 명령어

커밋/푸시 전에 로컬에서 검사 실행:

```bash
make quick-check       # commit 단계 훅 시뮬 (lint + format + 파일 검사)
make full-check        # commit + push 단계 훅 시뮬 (추가: pytest + mypy)
make ci-check          # CI 모드 (자동 수정 없음, 커버리지 게이트 포함)
make list-checks       # 정의된 모든 검사 목록
```

## Makefile 명령어 레퍼런스

### 설치 관련

| 명령어 | 설명 |
|--------|------|
| `make install` | 프로덕션 환경 설치 (패키지만) |
| `make install-dev` | 개발 환경 전체 설치 **권장** (venv + dev deps + git 훅) |
| `make install-hooks` | git 훅만 설치 (pre-commit / commit-msg / pre-push) |
| `make init NAME=foo` | `your_project` / `your-project` 플레이스홀더를 `foo` 로 치환 |
| `make clean` | 캐시 정리 (\_\_pycache\_\_, .pytest_cache, .ruff_cache 등) |

### 코드 품질

| 명령어 | 설명 |
|--------|------|
| `make lint` | Ruff 린트 + 자동 수정 |
| `make format` | Ruff 포매팅 |
| `make check` | 코드 스타일 검사 (lint + format) |
| `make test` | pytest 실행 (커버리지 포함) |
| `make typecheck` | mypy strict 타입 검사 |
| `make validate` | 전체 검증 (lint + format + test + typecheck) |

### 통합 검사

| 명령어 | 설명 |
|--------|------|
| `make ci-check` | CI 모드 (자동 수정 없음, 80% 커버리지 게이트) |
| `make quick-check` | pre-commit 단계만 시뮬 |
| `make full-check` | pre-commit + pre-push 단계 시뮬 |
| `make list-checks` | 정의된 모든 pre-commit 훅 목록 |

### Git 관련

| 명령어 | 설명 |
|--------|------|
| `make commit` | 대화형 커밋 생성 (Conventional Commits) |
| `make bump-version` | 버전 자동 증가 + 태그 생성 |
| `make update-hooks` | pre-commit 훅 리비전 자동 업데이트 |

## Conventional Commits

허용 타입: `feat`, `fix`, `docs`, `refactor`, `chore`, `revert`, `perf`

```bash
feat(auth): add login endpoint
fix(parser): handle empty input
docs: update README
```

**MAJOR 버전 업데이트**: 인라인 `!` 문법 사용 — `feat!: rewrite API`.
Commitizen 훅에서 `BREAKING CHANGE:` 푸터는 검증되지 않으므로 (스키마 제한), 인라인 `!` 이 신뢰할 수 있는 신호입니다.

## 2단계 훅 파이프라인 상세

### Pre-commit 단계 (커밋 시)

파일 단위 빠른 검사. `.pre-commit-config.yaml` 에서 정의:

1. **파일 무결성 검사**
   - 파일 끝 개행 자동 추가
   - 줄 끝 공백 자동 제거
   - YAML / TOML / JSON 문법 검사

2. **보안 검사**
   - Private 키 (SSH, 인증서) 탐지
   - AWS 자격증명 탐지

3. **대용량 파일 차단** (1MB 초과)

4. **코드 품질**
   - Ruff 린트 (문제 자동 수정, `--fix --exit-non-zero-on-fix`)
   - Ruff 포매팅

5. **자동 수정 재스테이징**
   - `scripts/stage_fixes.py` 가 수정된 파일만 다시 `git add`
   - `git add -p` 로 남긴 unstaged hunk 보호

### Commit-msg 단계 (메시지 검증)

Commitizen이 커밋 메시지를 `<type>(<scope>): <subject>` 형식으로 검증.

### Pre-push 단계 (푸시 시)

프로젝트 전체 검사. 빠른 모드로 30초 이내 완료:

- `pytest -x --no-cov -q` — 첫 실패 시 즉시 중단 (커버리지 생략)
- `mypy src` — 타입 검사

80% 커버리지 게이트는 **CI 에서만** 실행하여 로컬 푸시 속도 유지.

## `make init` 템플릿 초기화

`make init NAME=my_app` 은 다음을 자동으로 수행:

1. **Snake case 검증**: `my_app` 이 유효한 Python 패키지명인지 확인
2. **Kebab case 변환**: `my-app` (배포 이름) 생성
3. **디렉토리 이동**: `src/your_project/` → `src/my_app/`
4. **파일 치환**:
   - `pyproject.toml`: `your-project` → `my-app`, `your_project` → `my_app`
   - `src/my_app/__init__.py`: 동일하게 치환
   - (필요시) `pyproject.toml` 의 `known-first-party` 값도 자동 갱신

실행 후:
```bash
make install-dev
make ci-check  # 검증
```

## Auto-fix + 재커밋 메커니즘

Ruff 가 자동 수정하면 의도적으로 첫 커밋이 실패합니다:

1. **첫 번째 `git commit`**
   ```
   → pre-commit 훅 실행
   → Ruff 가 `src/foo.py` 수정
   → pre-commit 은 exit code 1 반환
   → 커밋 실패 (하지만 파일은 수정됨)
   ```

2. **상황 확인**
   ```bash
   git diff src/foo.py  # Ruff 가 무엇을 바꿨는지 확인
   ```

3. **두 번째 `git commit`**
   ```
   → pre-commit 훅 실행
   → stage_fixes.py 가 원래 staged 파일만 다시 add
   → 수정된 파일이 이미 staged 되어 있음
   → pre-commit 통과 (변경 없음)
   → 커밋 성공
   ```

**이 마찰은 의도적입니다**. 자동 수정 내용을 눈으로 검토하도록 강제하여 대형 diff 실수를 방지합니다.

## Troubleshooting

### pre-push 체크가 너무 느리다

pre-push 는 `pytest -x --no-cov -q` 와 `mypy src` 를 실행합니다. 30초 초과 시 `--no-verify` 우회 유혹이 증가합니다.

**해결책:**
- 느린 테스트를 `@pytest.mark.slow` 로 마킹 후 pre-push에서 제외
- 80% 커버리지 게이트는 CI 에서만 실행하므로, 로컬 푸시 땐 커버리지 재계산 안 됨

### `git push --no-verify` 를 사용했다

로컬 훅은 언제든 우회 가능합니다. 하지만 GitHub Actions 워크플로우(`.github/workflows/ci.yml`)는 **main 으로의 모든 푸시와 PR 에서** `make ci-check` 를 재실행하므로, 이것이 최종 게이트입니다.

### `make init` 이 어떤 참조를 못 바꿨다

`scripts/init_project.py` 는 `pyproject.toml` 과 `src/<pkg>/__init__.py` 에서만 `your-project` (kebab) / `your_project` (snake) 을 치환합니다. 다른 파일을 추가했다면:

```bash
grep -r your_project .
```

로 수동 확인 후 직접 편집하세요.

### Ruff 와 pre-commit ruff 버전이 어긋난다

`pyproject.toml` 의 `ruff==0.8.4` 와 `.pre-commit-config.yaml` 의 `rev: v0.8.4` 는 **정확히 같아야 합니다**. 버전 업그레이드 시:

```bash
# 두 파일을 같은 커밋에서 함께 수정
# pyproject.toml: ruff==X.Y.Z
# .pre-commit-config.yaml: rev: vX.Y.Z (Ruff 섹션)
git add pyproject.toml .pre-commit-config.yaml
make commit
```

로컬과 CI 동작 불일치 ("로컬 통과, CI 실패" 드리프트)를 방지합니다.

## SSOT(Single Source of Truth) 아키텍처

모든 체크 정의의 단일 출처:

```
.pre-commit-config.yaml  ← 모든 체크 정의의 SSOT
        ↑
   Makefile (얇은 래퍼)
        ↑
   .github/workflows/ci.yml (make ci-check 호출)
```

- `.pre-commit-config.yaml` — pre-commit, pre-push, commit-msg 훅 정의
- `Makefile` — `.pre-commit-config.yaml` 를 래핑하고 `ruff`, `mypy`, `pytest` 를 직접 호출하는 편의 도구
- `ci.yml` — 원격 CI에서 `make ci-check` 호출로 로컬/CI 일관성 유지

## 라이선스

MIT

# Python Project Quality Template

[![CI](https://github.com/bigmooon/python-template/actions/workflows/ci.yml/badge.svg)](https://github.com/bigmooon/python-template/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-3776AB?logo=python&logoColor=white)
![Ruff](https://img.shields.io/badge/Ruff-0.16.10-D7FF64?logo=ruff&logoColor=261230)
![Coverage](https://img.shields.io/badge/coverage-gate%2080%25-brightgreen)

Python 3.12–3.13 프로젝트를 시작할 때 패키지 구조, 품질 검사, Git hook과 CI를 함께 재사용할 수 있는 템플릿입니다. Ruff, mypy strict, pytest, coverage, pre-commit, Commitizen을 하나의 Make 워크플로우로 묶습니다.

## 바로 시작하기

필요한 환경은 Git, Make, POSIX shell(macOS/Linux), 그리고 `python3`가 Python 3.12 또는 3.13을 가리키는 환경입니다. 기본 명령과 다른 실행 파일을 써야 하면 `PYTHON=python3.12`처럼 오버라이드하면 됩니다.

```bash
git clone https://github.com/bigmooon/python-template.git my-project
cd my-project

make init NAME=my_project
make install-dev
make ci-check
```

`NAME`은 Python 패키지에 쓸 수 있는 `snake_case`를 권장합니다. `make init`은 다음 변경을 적용합니다.

- `src/your_project/`를 새 패키지명으로 이동
- 배포 이름은 `kebab-case`, import 이름은 `snake_case`로 치환
- `pyproject.toml`, 기본 테스트, README, Makefile, lock 파일의 플레이스홀더 갱신

`make install-dev`는 `.venv`를 만들고 `requirements-dev.lock`을 constraints로 사용해 개발 의존성을 설치한 뒤 pre-commit, commit-msg, pre-push hook을 설치합니다.

## 지원 범위와 검사 범위

| 항목 | 현재 설정 |
|---|---|
| Python | `>=3.12,<3.14`; CI matrix는 3.12, 3.13 |
| 실행 환경 | macOS/Linux, Make, POSIX shell |
| Ruff | `src`, `tests`, `scripts`; CLI와 hook 모두 0.16.10 |
| mypy | `src`, `scripts`; strict mode |
| pytest/coverage | 단위 테스트, `src`+`scripts` branch coverage 80% gate |
| Commitizen | CLI와 commit-msg hook 모두 4.19.1 |
| CI runner | `ubuntu-24.04`, `permissions: contents: read` |
| 자동 의존성 갱신 | Dependabot의 pip, GitHub Actions 주간 검사 |
| 라이선스 | MIT `LICENSE`, PEP 639 SPDX `license = "MIT"` |

CI는 Python 3.12와 3.13 각각에서 constraints 파일로 환경을 설치하고 `make ci-check`와 `make test-integration`을 순서대로 실행합니다.

## 사용 가능한 명령

| 명령 | 동작 |
|---|---|
| `make init NAME=my_app` | 프로젝트와 패키지 플레이스홀더 치환 |
| `make install-dev` | 고정 개발 환경과 Git hook 설치 |
| `make lint` | `src`, `tests`, `scripts`에 Ruff 자동 수정 |
| `make format` | `src`, `tests`, `scripts` 포매팅 |
| `make typecheck` | `src`, `scripts` mypy strict 검사 |
| `make test` | 단위 테스트와 80% coverage gate |
| `make ci-check` | 자동 수정 없이 Ruff, mypy, 단위 테스트, coverage 검증 |
| `make test-integration` | 임시 Git 저장소에서 `init → install-dev → ci-check` 검증 |
| `make quick-check` | pre-commit 단계의 모든 hook 실행 |
| `make full-check` | pre-commit과 pre-push 단계 모두 실행 |
| `make commit` | Commitizen 대화형 Conventional Commit 생성 |
| `make lock-dev` | uv로 공통 개발 constraints 재생성 |
| `make update-hooks` | pre-commit repository revision 갱신 |

통합 테스트는 설치를 반복하므로 기본 pytest 실행에서는 제외됩니다. CI와 `make test-integration`이 이 테스트를 명시적으로 실행합니다.

## Git hook과 부분 staging 보호

pre-commit 단계는 파일·YAML·TOML·JSON 무결성, 충돌 마커, 디버그 구문, private key/AWS 자격 증명, 대용량 파일, Ruff lint/format을 검사합니다. commit-msg는 Commitizen, pre-push는 pytest와 mypy를 실행합니다.

Ruff가 파일을 수정하면 hook은 실패하고 커밋을 중단합니다. `stage_fixes.py`는 수정된 파일과 `git add -p` 안내를 보여주지만 index를 절대 변경하지 않습니다. hook 실행 중 자동으로 `git add`하면 pre-commit이 임시로 숨긴 unstaged hunk와 충돌해 사용자 변경을 복원하지 못할 수 있기 때문입니다. `git diff`와 `git diff --cached`를 확인한 뒤 원하는 hunk만 수동으로 stage하세요.

통합 테스트는 같은 줄에 staged·unstaged 변경이 동시에 있는 최악의 충돌 상황에서 실제 pre-commit 훅을 실행합니다. hook은 코드 1로 실패하고, staged 내용과 unstaged 내용이 각각 그대로 남아야 테스트가 통과합니다.

## 의존성 고정과 갱신

`requirements-dev.lock`은 Python 3.12–3.13과 주요 플랫폼을 위한 universal constraints 파일입니다. 일반 사용자는 uv가 필요 없고, 의존성을 변경하는 유지보수자만 uv를 설치한 뒤 다음을 실행합니다.

```bash
make lock-dev
make install-dev
make ci-check
make test-integration
```

Ruff와 Commitizen을 올릴 때는 `pyproject.toml`의 CLI 버전과 `.pre-commit-config.yaml`의 hook revision을 함께 바꾸어야 합니다. Dependabot은 pip과 GitHub Actions를 주간으로 점검하지만 pre-commit repository revision은 `make update-hooks`로 관리합니다.

## 현재 검증 결과

2026-10-10에 macOS, Python 3.12.12에서 이 저장소의 복사본으로 다음을 확인했습니다. 아래는 GitHub Actions의 원격 실행 결과가 아니라 로컬 실행 결과입니다.

| 검증 | 결과 |
|---|---|
| `make ci-check` | 통과; Ruff 9개 Python 파일, mypy 3개 소스 파일 |
| 단위 테스트 | 17개 통과, 1개 integration marker 제외 |
| branch coverage | 85.39%; 기준 80% 통과 |
| `make full-check` | pre-commit·pre-push hook 모두 통과 |
| `make test-integration` | 임시 프로젝트 workflow와 실제 부분-staging hook 충돌 테스트 1개 통과 |

Python 3.13은 GitHub Actions matrix에서 검증되도록 설정되었습니다. 저장소의 최신 원격 상태는 [GitHub Actions](https://github.com/bigmooon/python-template/actions/workflows/ci.yml)에서 확인하세요.

## GitHub 저장소에서 별도로 해야 할 일

다음 항목은 코드 변경으로 적용되지 않으며, 저장소 관리자가 GitHub 설정에서 별도로 구성해야 합니다.

1. **Template repository**: Settings → General에서 Template repository를 활성화합니다.
2. **Branch ruleset**: `main`을 대상으로 PR 필수, force push/삭제 제한, CI required status check를 설정합니다.
3. **Required checks**: matrix job의 `Python 3.12`와 `Python 3.13` 모두를 성공해야 merge할 수 있도록 선택합니다. 처음에는 workflow를 한 번 실행해야 check 이름이 선택 목록에 나타날 수 있습니다.

CI workflow, read-only token permission, Dependabot 설정은 이 저장소에 파일로 포함됩니다. ruleset과 Template repository 플래그는 포함되지 않습니다.

## 구조

```text
.
├── .github/
│   ├── dependabot.yml
│   └── workflows/ci.yml
├── scripts/
│   ├── init_project.py
│   └── stage_fixes.py
├── src/your_project/
├── tests/
├── LICENSE
├── Makefile
├── pyproject.toml
└── requirements-dev.lock
```

## License

MIT. 전문은 [LICENSE](LICENSE)에 있습니다.

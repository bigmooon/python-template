# Python 3.12 Project Template

Automated commit/push quality gate template for Python 3.12 projects. The
checking system itself is the deliverable — pre-commit and pre-push hooks
plus a CI workflow ensure broken or unformatted code never lands in main.

## Features

- **Ruff** — Linting + formatting in one tool, with auto-fix and **auto-stage**
- **mypy** — Strict type checking
- **pytest + coverage** — Tests with 80%+ coverage gate (CI)
- **pre-commit + pre-push** — Two-stage hook pipeline
- **Commitizen** — Conventional Commits enforcement
- **GitHub Actions CI** — Remote safety net for `--no-verify` bypass

### Two-Stage Hook Pipeline

```
git commit -m "feat: add user auth"
  ├─ pre-commit stage (fast, file-level)
  │   ├─ End-of-file / trailing whitespace
  │   ├─ YAML / TOML / JSON syntax check
  │   ├─ Secret detection (private key, AWS credentials)
  │   ├─ Large file block (>1MB)
  │   ├─ Ruff lint (--fix)
  │   ├─ Ruff format
  │   └─ stage-fixes (auto git add the fixed files)
  └─ commit-msg stage
      └─ Commitizen message validation

git push
  └─ pre-push stage (project-wide)
      ├─ pytest -x --no-cov -q  (fast fail mode)
      └─ mypy src

GitHub Actions CI (push to main, PR)
  └─ make ci-check
      ├─ ruff check --no-fix
      ├─ ruff format --check
      ├─ mypy src
      └─ pytest --cov  (80% gate)
```

## Prerequisites

- Python 3.12+
- Git

## Getting Started

```bash
# 1. Clone
git clone https://github.com/bigmooon/python-template.git
cd python-template

# 2. Initialize with your project name
make init NAME=my_app

# 3. Install dev environment (venv + deps + git hooks for commit/push/commit-msg)
make install-dev
```

## Why might my first commit fail?

When Ruff auto-fixes code (e.g. import sort, quote style), pre-commit returns
a non-zero exit code so you can review the changes. The `stage-fixes` hook
**re-stages only the files originally staged** — protecting any partial
`git add -p` hunks you intentionally left unstaged.

```bash
git add src/foo.py
git commit -m "feat: add foo"
# ⚠️  Ruff fixed src/foo.py — first commit fails
git commit -m "feat: add foo"
# ✓ Second attempt passes (auto-fix already staged)
```

This is intentional — it gives you a chance to inspect the diff Ruff applied.

## Usage

### Daily Workflow

```bash
# Edit code → commit → push
git add src/foo.py
git commit -m "feat(foo): add bar"
git push
# pre-push runs pytest + mypy automatically
```

### Manual checks before committing

```bash
make quick-check       # commit-stage hooks (lint + format + file checks)
make full-check        # commit + push stages (adds pytest + mypy)
make ci-check          # CI mode (no auto-fix, with coverage gate)
make list-checks       # show all configured checks at a glance
```

### Commands

```bash
make help              # all commands

# Setup
make install-dev       # venv + deps + git hooks (recommended)
make install-hooks     # git hooks only (pre-commit + commit-msg + pre-push)
make init NAME=foo     # rename placeholders to 'foo'

# Code quality
make lint              # ruff check --fix
make format            # ruff format
make typecheck         # mypy src
make test              # pytest with coverage

# Combined
make check             # lint + format
make validate          # lint + format + typecheck + test
make ci-check          # CI verification (--no-fix, coverage gate)
make quick-check       # pre-commit stage only
make full-check        # pre-commit + pre-push stages

# Git
make commit            # interactive commit (Conventional Commits)
make bump-version      # auto bump version + tag

# Maintenance
make clean             # clear caches
make update-hooks      # update pre-commit hook revisions
```

## Conventional Commits

Allowed types: `feat`, `fix`, `docs`, `refactor`, `chore`, `revert`, `perf`.

```bash
feat(auth): add login endpoint
fix(parser): handle empty input
```

**MAJOR version bumps**: use the inline `!` syntax — `feat!: rewrite API`.
The `BREAKING CHANGE:` footer is **not validated** by the commit-msg hook
(commitizen schema limitation), so the inline `!` is the reliable signal.

## Troubleshooting

### A pre-push check is too slow

The `pre-push` hooks run `pytest -x --no-cov -q` and `mypy src`. If they
exceed ~30s, contributors may bypass with `--no-verify`. Mitigation:
- Mark slow tests with `@pytest.mark.slow` and skip them in pre-push
- The 80% coverage gate runs only in CI, so coverage isn't recomputed on push

### `git push --no-verify` was used

Local hooks can be bypassed. The GitHub Actions workflow
(`.github/workflows/ci.yml`) re-runs `make ci-check` on every push to `main`
and every PR — this is the authoritative gate.

### `make init` didn't rename a reference

`scripts/init_project.py` substitutes `your-project` (kebab) and `your_project`
(snake) in `pyproject.toml` and `src/<pkg>/__init__.py`. If you added new
files referencing the old name, run `grep -r your_project .` to find them.

### Ruff and pre-commit ruff versions disagree

`pyproject.toml` pins `ruff==0.8.4` exactly to match `.pre-commit-config.yaml`'s
`rev: v0.8.4`. When upgrading Ruff, **bump both in the same commit** to avoid
"local passes, CI fails" drift.

## Architecture

The check definitions live in `.pre-commit-config.yaml` (single source of
truth). The Makefile is a thin wrapper around `pre-commit run` plus a few
direct tool invocations for `make ci-check`. The CI workflow calls
`make ci-check` so local and CI behavior stay aligned.

```
.pre-commit-config.yaml  ← SSOT for all check definitions
        ↑
   Makefile (wrapper)
        ↑
   .github/workflows/ci.yml (calls make ci-check)
```

## License

MIT

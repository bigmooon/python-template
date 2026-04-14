# Python 3.12 Project Template

Automated code quality system for Python 3.12 projects.

## Features

- **Ruff** — Linting + formatting in one tool
- **mypy** — Strict type checking
- **pytest** — Testing with coverage
- **pre-commit** — Automated checks on every commit
- **Commitizen** — Conventional Commits enforcement

### Git Hook Pipeline

```bash
git commit -m "feat: add user auth"
# Runs automatically:
# 1. File checks (EOF, whitespace, YAML/TOML/JSON, private keys)
# 2. Ruff linting (with auto-fix)
# 3. Ruff formatting
# 4. Commitizen message validation
```

## Prerequisites

- Python 3.12+
- Git

## Getting Started

```bash
# Clone and setup
git clone https://github.com/bigmooon/python-template.git
cd python-template

# Install dev environment (venv + deps + git hooks)
make install-dev
```

## Usage

### Development Workflow

```bash
# 1. After writing code
make check             # lint + format (auto-fix)

# 2. Before committing — full validation
make validate          # lint + format + test + typecheck

# 3. Commit
git add .
git commit -m "feat(auth): add login endpoint"

# Or use interactive commit
make commit
```

### All Commands

```bash
make help              # Show all commands

# Setup
make install           # Production install
make install-dev       # Dev environment (recommended)
make install-hooks     # Git hooks only

# Code Quality
make lint              # Lint with auto-fix
make format            # Format code
make test              # Run tests (pytest + coverage)
make typecheck         # Type check (mypy)

# Combined
make check             # lint + format
make validate          # lint + format + test + typecheck
make ci-check          # CI mode (verify only, no auto-fix)

# Git
make commit            # Interactive commit (Conventional Commits)
make bump-version      # Auto bump version + tag

# Maintenance
make clean             # Clear caches
make update-hooks      # Update pre-commit hooks
```

## Customization

When using this template for a new project, update the following:

1. `pyproject.toml` — `name`, `description`, `authors`, `keywords`
2. `pyproject.toml` — `known-first-party` in `[tool.ruff.lint.isort]`
3. Rename `src/your_project/` to match your package name

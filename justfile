set shell := ["bash", "-euo", "pipefail", "-c"]

# List the available commands
default:
    @just --list --unsorted

# Install every dependency (Python and Node)
setup:
    cd pipeline && uv sync --locked
    cd web && pnpm install --frozen-lockfile

# Fast check, no network: lint, types and tests. Run it after every step
check: pipeline-check web-check repo-check

# Full check before a pull request: check, plus the site build
verify: check
    cd web && pnpm run build

# Python: format check, lint, types, tests, config validation
[working-directory('pipeline')]
pipeline-check:
    uv run ruff format --check .
    uv run ruff check .
    uv run mypy
    uv run pytest -q
    uv run wnr config check --metrics ../config/metrics.yaml

# Web: lint, types, tests
[working-directory('web')]
web-check:
    pnpm run lint
    pnpm run typecheck
    pnpm run test

# Repository tooling: risk-tier classifier and agent hooks
repo-check:
    node --test --test-reporter=dot ".github/scripts/*.test.mjs"
    python3 -m unittest discover -s tests/repo -t . -q

# Regenerate schemas/ from the pydantic models
[working-directory('pipeline')]
schemas:
    uv run wnr schemas export --out ../schemas

# Format code in place
fmt:
    cd pipeline && uv run ruff format . && uv run ruff check --fix .
    cd web && pnpm run format

# Start the site in development mode
[working-directory('web')]
web-dev:
    pnpm run dev

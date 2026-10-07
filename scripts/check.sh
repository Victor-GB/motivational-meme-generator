#!/usr/bin/env bash

set -euo pipefail

printf '\n==> Ruff formatting\n'
python -m ruff format --check .

printf '\n==> Ruff linting\n'
python -m ruff check .

printf '\n==> Mypy type checking\n'
python -m mypy

printf '\n==> Dependency vulnerability audit\n'
python -m pip_audit --strict -r requirements-dev.txt

printf '\n==> Pytest and coverage\n'
python -m pytest -q --tb=short

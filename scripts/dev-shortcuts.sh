#!/usr/bin/env bash

export PY_PROJECT_ROOT="/home/vicdev/workspace/python/udacity/nanodegree/intermediate-python/projects/02_motivational-meme-generator"

frma() (
    cd "$PY_PROJECT_ROOT" || return
    local project_python="$PY_PROJECT_ROOT/.venv/bin/python"

    "$project_python" -m ruff check --fix --exit-zero . || return
    "$project_python" -m ruff format . || return
    "$project_python" -m ruff check .
)

frmpya() (
    frma || return
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m mypy .
)

_latest_python_file() {
    find "$PWD" -maxdepth 1 -type f -name '*.py' -printf '%T@ %p\n' |
        sort -nr |
        sed -n '1s/^[^ ]* //p'
}

frm() (
    local target
    target="${1:-$(_latest_python_file)}"

    if [[ -z "$target" ]]; then
        printf 'No Python files in the current directory.\n'
        return 1
    fi

    local display_path="${target#"$PY_PROJECT_ROOT"/}"
    printf 'Selected: %s/%s\n' "${PY_PROJECT_ROOT##*/}" "$display_path"
    cd "$PY_PROJECT_ROOT" || return
    local project_python="$PY_PROJECT_ROOT/.venv/bin/python"

    "$project_python" -m ruff check --fix --exit-zero "$target" || return
    "$project_python" -m ruff format "$target" || return
    "$project_python" -m ruff check "$target"
)

frmpy() (
    local target
    target=$(_latest_python_file)

    frm "$target" || return
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m mypy "$target"
)


pt() (
    local target
    target=$(_latest_python_file)

    if [[ -z "$target" ]]; then
        printf 'No Python files in the current directory.\n'
        return 1
    fi

    local display_path="${target#"$PY_PROJECT_ROOT"/}"
    printf 'Selected: %s/%s\n' "${PY_PROJECT_ROOT##*/}" "$display_path"
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m pytest -q "$target"
)

pta() (
    cd "$PY_PROJECT_ROOT" || return
    "$PY_PROJECT_ROOT/.venv/bin/python" -m pytest -q
)

ptl() (
    set -o pipefail
    mkdir -p "$PY_PROJECT_ROOT/tmp" || return
    pt 2>&1 | tee "$PY_PROJECT_ROOT/tmp/pytest-latest.log"
)

ptal() (
    set -o pipefail
    mkdir -p "$PY_PROJECT_ROOT/tmp" || return
    pta 2>&1 | tee "$PY_PROJECT_ROOT/tmp/pytest-all.log"
)

al() {
    cat <<'HELP'
frm     Fix and format the newest Python file in the current directory.
frmpy   Same as frm, then run mypy on that file.
frma    Fix and format Python files recursively under PY_PROJECT_ROOT.
frmpya  Same as frma, then run mypy across the project.
pt      Run pytest on the newest Python file in the current directory.
pta     Run the complete project test suite.
ptl     Same as pt, saving output to tmp/pytest-latest.log.
ptal    Same as pta, saving output to tmp/pytest-all.log.
al      Show this shortcut reference.
HELP
}

# Development additions

- Ruff handles formatting, linting and import ordering.
- Mypy checks application type annotations.
- Pytest checks quote ingestion and image output, with branch coverage.
- pip-audit checks the recorded dependencies for known vulnerabilities.
- Pre-commit runs quick commit checks and the full quality script before pushes.
- Dependabot proposes Python dependency and GitHub Actions updates.
- `scripts/check.sh` provides one command for the full quality checks.

CLI and Flask behaviour were also verified manually.

## Terminal shortcuts

Set `PY_PROJECT_ROOT` in `scripts/dev-shortcuts.sh` to your project location.
From the project root, load the functions into your Bash terminal:

```bash
source scripts/dev-shortcuts.sh
```

Run `al` to display the shortcut reference.

`frm` and `frmpy` select the newest saved Python file directly in the current
directory. `frma` and `frmpya` work recursively across the project.

`pt` tests the newest Python file in the current directory; use it from `tests`.
`pta` runs the full suite. `ptl` and `ptal` also save output in `tmp`.

The shortcuts preserve the terminal's working directory. Loading them is
optional and applies to the current shell; no shell-profile changes are required.

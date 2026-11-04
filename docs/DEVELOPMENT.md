# Development Guide

This guide explains the tools this repository uses and why they exist. It is
written for a reader who is new to Python project infrastructure, and it
describes the repository as it exists today. Commands assume you are inside the
project directory.

## Repository, working directory, and remote

Three related things are easy to confuse:

- A **Git repository** is the `.git/` directory. It stores commits, branches,
  and configuration.
- The **working directory** is the checkout you edit: source files, docs, and
  your uncommitted changes.
- A **remote** is another copy of the repository, here on GitHub. `origin` is the
  conventional name for the primary remote.

```bash
git remote -v          # where origin points
git status             # working directory versus the last commit
git log --oneline      # commit history
```

`git status` describes local state. It knows nothing about GitHub until you
fetch or push.

## Interpreter, package, and distribution

- A **Python interpreter** is the executable that runs code (`python3.12`).
- A **package** is an importable directory containing an `__init__.py`.
- A **distribution** is what `pip` installs. It can contain one or more packages
  plus metadata and entry points.

This project's distribution is `spotify-music-clustering`; the package it
installs is `spotify_music_clustering`. Hyphens are valid in distribution names
but not in import statements.

## `pip` versus `venv`

They solve different problems:

- **`venv`** creates an isolated Python environment: its own interpreter
  symlink, its own `site-packages`, its own scripts directory. It decides *where*
  packages are installed.
- **`pip`** downloads and installs packages into whichever environment is active.
  It decides *what* is installed.

Using `pip` without a virtual environment writes into the system interpreter.
On many Linux distributions that is blocked, and even where it is allowed it can
break tools that depend on system packages.

### Why every collaborator creates their own environment

`.venv/` is machine-specific. It contains absolute paths and platform-specific
binaries, so copying it between machines or committing it does not work
reliably. Each collaborator creates an environment from `pyproject.toml`, which
is the shared, versioned description of what the project needs.

## Creating the environment

### Linux and macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -c "import sys; print(sys.executable)"
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
```

The printed path must contain `.venv`. Activation changes your shell's `PATH` so
that `python` and `pip` resolve to the environment. `deactivate` reverses it.

## `pyproject.toml`

`pyproject.toml` is the single source of project metadata. In this repository it
declares:

| Section | Purpose |
|---|---|
| `[build-system]` | Which backend builds the distribution (setuptools) |
| `[project]` | Name, description, Python range, runtime dependencies |
| `[project.optional-dependencies]` | `dev` tools: pytest, Ruff, build |
| `[project.scripts]` | The `spotify-cluster` console command |
| `[tool.setuptools]` | Where packages live and how the version is discovered |
| `[tool.pytest.ini_options]` | Test discovery and strictness |
| `[tool.ruff]` | Lint rules and formatter settings |

Because dependencies are declared here, there is no separate
`requirements.txt`. Adding a runtime dependency means editing
`[project].dependencies`; adding a development-only tool means editing the `dev`
extra.

## Editable installation

```bash
python -m pip install -e ".[dev]"
```

The `-e` flag means *editable*: `pip` records a link to this checkout instead of
copying files into `site-packages`. Changes to source files take effect on the
next import without reinstalling. The `.[dev]` part installs the project itself
plus the `dev` extra.

Use this form after changing `[project].dependencies` or `[project.scripts]`,
because those changes are packaging metadata and require `pip` to re-read them.

To confirm what is installed:

```bash
python -m pip show spotify-music-clustering
```

## How imports work with a `src` layout

When Python executes `import spotify_music_clustering`, it searches the entries
of `sys.path`. After an editable install, one of those entries points at
`src/`, so the package is found there.

The repository root is *not* automatically on `sys.path`, which means a stray
top-level directory named `spotify_music_clustering` cannot shadow the installed
package. This is the main reason the `src` layout is used.

To inspect resolution:

```bash
python -c "import spotify_music_clustering as m; print(m.__file__)"
```

The path should end in `src/spotify_music_clustering/__init__.py`. If it does
not, the project is either not installed or a different copy is being imported.

## `__init__.py` and `__main__.py`

- `__init__.py` runs when the package is imported. Here it defines the package
  docstring and `__version__`, and declares `__all__`. It has no side effects: no
  printing, no file access, no environment mutation.
- `__main__.py` runs when the package is executed with `python -m`. It calls
  `app.main()`, so running the module and running the console script share the
  same code.

`app.run()` returns an integer exit code; `app.main()` converts it into
`SystemExit`. A zero exit code means success, which is what CI checks.

## How the console script works

`[project.scripts]` maps a command name to a callable:

```toml
[project.scripts]
spotify-cluster = "spotify_music_clustering.app:main"
```

At install time, `pip` writes a small launcher into the environment's scripts
directory (`.venv/bin/` on Linux and macOS, `.venv\Scripts\` on Windows). The
launcher imports `app` and calls `main()`. The command only exists while the
environment is active or its scripts directory is on `PATH`.

## What pytest checks, and what it cannot

Run:

```bash
python -m pytest -q
```

The current suite checks that:

- the package imports from `src/` and exposes a version;
- `app.run()` prints the expected status and returns `0`;
- `python -m spotify_music_clustering` runs successfully;
- the `spotify-cluster` script exists and prints exactly the same output.

What it cannot prove:

- that the analysis is correct — there is no analysis yet;
- that every future code path works — tests cover what they assert;
- that a different operating system behaves identically;
- that the remote CI workflow passes, until that workflow has actually run.

Tests reduce risk; they do not certify correctness. A passing suite describes the
checked behavior, nothing more.

## Ruff: linting versus formatting

Both commands use Ruff but answer different questions:

```bash
python -m ruff check .            # static analysis: errors, imports, style bugs
python -m ruff format --check .   # formatting only: would the formatter rewrite files?
```

`ruff check` applies rules such as unused imports, undefined names, import
ordering, and simplification suggestions. `ruff format` is a deterministic code
formatter; `--check` reports differences without writing them.

To fix:

```bash
python -m ruff check --fix .
python -m ruff format .
```

CI runs both in check mode, so a formatted-but-linting-failing change still
fails the build.

## How GitHub Actions CI works

`.github/workflows/ci.yml` defines a job that GitHub runs on a fresh Ubuntu
machine:

1. Check out the repository.
2. Install Python 3.12 and cache `pip` downloads.
3. Install the project with the `dev` extra.
4. Run `ruff check`, `ruff format --check`, and `pytest`.
5. Build the sdist and wheel.
6. Install the wheel into a separate empty virtual environment and run the
   console command.

The workflow triggers on pushes and pull requests to `main`, uses read-only
repository permissions, and fails if any step fails. Jobs run on GitHub's
infrastructure, so local success does not guarantee CI success — the environment
differs.

## Recreating the environment elsewhere

1. Install Python 3.12.
2. Clone the repository.
3. Create and activate `.venv`.
4. Run `python -m pip install -e ".[dev]"`.
5. Verify with `python -m spotify_music_clustering` and `python -m pytest -q`.

No environment files are copied. If the setup works on one machine and not
another, compare the interpreter version first.

## Diagnosing common problems

**`ModuleNotFoundError: No module named 'spotify_music_clustering'`**

The project is not installed in the active environment, or the environment is
not active. Check `python -c "import sys; print(sys.executable)"`, then
reinstall with `python -m pip install -e ".[dev]"`.

**`bash: spotify-cluster: command not found`**

The console script is installed inside `.venv`, not globally. Activate the
environment, or reinstall if the script is genuinely missing.

**`error: externally-managed-environment`**

`pip` is pointing at a system interpreter. Create and activate a virtual
environment instead of forcing the install.

**`ERROR: Package 'spotify-music-clustering' requires a different Python: 3.13.x not in '>=3.12,<3.13'`**

The environment was created with the wrong interpreter. Remove `.venv`, recreate
it with `python3.12 -m venv .venv`, and reinstall.

**A stale command or entry point after editing metadata**

Editable installs track source code, not all packaging metadata. Reinstall with
`python -m pip install -e ".[dev]"`.

**`ruff: command not found`**

Ruff is a development dependency. Install the `dev` extra, then run it as a
module: `python -m ruff check .` — that form uses the environment's Ruff even if
its scripts directory is not on `PATH`.

**Tests fail while importing subprocess output**

Run the suite from the repository root with the environment active, and check
that the console script exists in the same scripts directory as the active
interpreter. The test error message reports the directory it searched.

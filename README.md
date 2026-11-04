# Spotify Music Clustering

A Python project for exploring acoustic similarity among Spotify tracks with
unsupervised learning. The repository currently provides the engineering
foundation — packaging, environment setup, tests, linting, and CI — for a
research pipeline that will be built in later milestones.

## Overview

Music recommendation and playlist curation often rely on metadata such as genre,
artist, or popularity. This project instead studies the audio features that
describe how a track sounds — for example energy, tempo, and spectral
characteristics — and asks whether tracks form meaningful groups in that feature
space.

The intended approach is unsupervised: tracks are described by numerical audio
features, compared in a normalized feature space, and grouped with clustering
algorithms. The project will examine whether those groups are stable,
interpretable, and consistent with human descriptions of musical style.

No analysis has been implemented yet. The current milestone only establishes the
repository, the installable package, the tooling, and the continuous integration
workflow.

## Objectives

The planned research pipeline covers:

- **Audio feature analysis** — examine the distributions and relationships of
  the numerical descriptors supplied with the dataset.
- **Data cleaning and preparation** — define how invalid, duplicated, or
  missing records are handled before any modelling.
- **Feature normalization** — place features with different units and ranges on
  a comparable scale.
- **Dimensionality reduction** — project the normalized feature space with PCA
  and t-SNE to inspect structure and support visualization.
- **K-Means clustering** — partition tracks into a chosen number of groups.
- **Gaussian Mixture Models** — model groups probabilistically and compare the
  result with hard partitioning.
- **Cluster evaluation and comparison** — use internal validation measures and
  stability checks to compare configurations rather than assuming one is best.
- **Acoustic cluster profiling** — describe each group in terms of its feature
  centroids and representative tracks.
- **Visualization and interpretation** — produce figures and written analysis
  that explain what the groups represent.

These are planned capabilities, not completed functionality. Each will be
implemented and documented with reproducible evidence in its own milestone.

## Technology Stack

| Category | Technology | Responsibility |
|---|---|---|
| Language | Python 3.12 | Supported interpreter for this milestone |
| Packaging | setuptools + `pyproject.toml` | Build metadata, dependencies, entry points |
| Environment | `venv` + `pip` | Isolated interpreter and dependency installation |
| Data processing | NumPy, Pandas | Array computation and tabular data handling |
| Machine learning | scikit-learn | Preprocessing, decomposition, clustering, validation |
| Visualization | Matplotlib | Static figures for analysis and documentation |
| Configuration | PyYAML | Future experiment configuration files |
| Testing | pytest | Automated verification of code and packaging |
| Linting and formatting | Ruff | Static checks and consistent code style |
| Continuous integration | GitHub Actions | Reproducible checks on every push and pull request |

Dependencies are declared once in `pyproject.toml`. There is no separate
`requirements.txt`, because the project metadata is the canonical source.

## Repository Structure

```text
spotify-music-clustering/
├── .github/
│   └── workflows/
│       └── ci.yml              # Lint, format, test, and packaging checks
├── .venv/                      # Local virtual environment (ignored by Git)
├── data/
│   ├── raw/
│   │   └── .gitkeep            # Original dataset, downloaded locally
│   └── processed/
│       └── .gitkeep            # Derived data produced by preprocessing
├── src/
│   └── spotify_music_clustering/
│       ├── __init__.py         # Package metadata and version
│       ├── __main__.py         # `python -m spotify_music_clustering`
│       └── app.py              # Entry points and status report
├── tests/
│   └── test_smoke.py           # Bootstrap and packaging tests
├── configs/
│   └── .gitkeep                # Future experiment configuration files
├── artifacts/
│   └── .gitkeep                # Future figures, metrics, and models
├── docs/
│   ├── ARCHITECTURE.md         # Design boundaries and layout decisions
│   └── DEVELOPMENT.md          # Beginner-oriented engineering guide
├── .editorconfig               # Editor-level whitespace and encoding rules
├── .gitignore                  # Local environments, data, and generated files
├── pyproject.toml              # Build, dependencies, pytest, and Ruff config
└── README.md
```

Directory responsibilities:

- `src/spotify_music_clustering/` holds importable application logic.
- `tests/` holds automated tests, kept separate from application code.
- `data/raw/` will hold the unmodified dataset. It is ignored by Git.
- `data/processed/` will hold derived datasets. It is ignored by Git.
- `configs/` will hold experiment configuration files.
- `artifacts/` will hold generated outputs: figures, metrics, and models.
- `docs/` holds architecture, development, and future methodology notes.

Only source code, configuration, tests, and documentation are versioned.
Datasets and generated outputs stay local and are recreated from documented
steps.

## Getting Started

### Prerequisites

- Python **3.12.x** — the only supported interpreter for this milestone.
- Git.
- A terminal (bash/zsh on Linux or macOS, PowerShell on Windows).

Confirm the interpreter before creating the environment:

```bash
python3.12 --version
```

On Windows:

```powershell
py -3.12 --version
```

If the command is unavailable, install Python 3.12 from
[python.org](https://www.python.org/downloads/) and retry. Do not continue with
a different version and assume compatibility; the project metadata declares
`requires-python = ">=3.12,<3.13"`.

### Linux and macOS

```bash
git clone https://github.com/minhqng/spotify-music-clustering.git
cd spotify-music-clustering

python3.12 -m venv .venv
source .venv/bin/activate
python -c "import sys; print(sys.executable)"

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Windows PowerShell

```powershell
git clone https://github.com/minhqng/spotify-music-clustering.git
Set-Location spotify-music-clustering

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell refuses to run the activation script, allow it for the current
session only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

The printed interpreter path must point inside `.venv`. If it points to a system
installation, the environment is not active.

### Leaving the environment

```bash
deactivate
```

## Running the Application

The application currently prints an initialization report: project name,
version, pipeline status, and the active interpreter. Both entry points call the
same function.

As a Python module:

```bash
python -m spotify_music_clustering
```

Through the installed console script:

```bash
spotify-cluster
```

Expected output has this shape (the version and path depend on your machine):

```text
Spotify Music Clustering 0.1.0
Status: repository bootstrap complete; analysis pipeline not implemented yet
Python 3.12.14 at /path/to/spotify-music-clustering/.venv/bin/python
```

## Testing and Code Quality

Run the suite with the environment active:

```bash
python -m pytest -q
```

The tests verify that the package imports from the `src` layout, that both entry
points run in the installed environment, and that they produce the same output.

Run static checks:

```bash
python -m ruff check .
python -m ruff format --check .
```

Apply formatting automatically:

```bash
python -m ruff format .
```

Build and inspect the distributable artifacts:

```bash
python -m build
```

To confirm the wheel is self-contained, install it into a throwaway
environment:

```bash
python -m venv /tmp/spotify-wheel-check
/tmp/spotify-wheel-check/bin/python -m pip install dist/*.whl
/tmp/spotify-wheel-check/bin/spotify-cluster
```

On Windows, replace `/tmp/spotify-wheel-check/bin/...` with
`.venv-check\Scripts\...`.

## Dataset

The only dataset intended for this project is the
[Kaggle Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset)
published by Maharshi Pandya.

- Obtain it through Kaggle with an account that has accepted the dataset's
  terms. Do not use scraped, mirrored, or substituted collections.
- The Kaggle download is named `dataset.csv`. Place it at
  `data/raw/dataset.csv`.
- The file is excluded by `.gitignore` and must never be committed. This
  repository does not redistribute the data and does not grant rights to it.
- Dataset licensing and the code license are separate decisions. The dataset's
  terms govern the data regardless of how this repository is licensed.
- No schema, row count, or quality claim is made here. Those properties will be
  measured and documented from the actual file in the ingestion milestone.

## Development Status

**Milestone 1 — repository bootstrap: complete.**

Delivered: `src`-layout package, packaging metadata, dual entry points, smoke
tests, Ruff configuration, GitHub Actions CI, ignore rules, and technical
documentation.

**Not implemented:** dataset ingestion, cleaning, feature engineering,
normalization, dimensionality reduction, K-Means, Gaussian Mixture Models,
evaluation metrics, experiment sweeps, trained models, dashboards, and any
research result. The application reports status only; it performs no analysis
and produces no metrics.

## Reproducibility

What exists today:

- Python 3.12 is declared as the supported interpreter, and CI runs on exactly
  that version.
- Direct dependencies are declared with explicit lower and upper bounds in
  `pyproject.toml`.
- The test suite and CI workflow run from a clean environment on every push.
- Local environments are created from documented commands rather than copied
  between machines.
- Data and generated artifacts are deliberately excluded from version control.

What does not exist yet, and must not be assumed:

- A fully pinned lockfile with hashes for transitive dependencies.
- Versioned experiment configurations, fixed random seeds, and recorded
  environment snapshots per experiment.
- A documented dataset version or checksum.
- Archived result artifacts linked to specific commits.

Those mechanisms will be added with the experiments they are meant to make
reproducible.

## License

No license has been published for this repository yet, so the source code is not
currently licensed for reuse. The Kaggle dataset is governed by its own terms
and is not covered by any license in this repository.

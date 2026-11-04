# Architecture

This document describes the boundaries and layout of the repository as it exists
today, and the pipeline it is being prepared for. It deliberately avoids
specifying modules that have not been written.

## Project boundaries

The project has one responsibility: study acoustic similarity among tracks from
the Kaggle Spotify Tracks Dataset using unsupervised learning, and document the
method and results honestly. That responsibility implies a few boundaries:

- **The repository owns code, not data.** Research data lives on the local
  machine and is never committed.
- **Analysis is reproducible from source.** Given the dataset and the documented
  environment, a result should be regenerable. The current milestone establishes
  only the environment and verification parts of that promise.
- **Reporting is evidence-based.** Documentation must not describe results
  before they have been produced.
- **Scope grows by milestone.** There are no placeholder analysis modules, no
  mock models, and no stubbed metrics. A capability appears when it is
  implemented and tested.

## Why a `src` layout

Application code lives in `src/spotify_music_clustering/` rather than a
top-level `spotify_music_clustering/` directory.

- **Imports match the installed package.** Python does not put the repository
  root on `sys.path`, so `import spotify_music_clustering` resolves to the
  installed distribution rather than to a directory that happens to sit next to
  the command you ran.
- **Packaging errors surface early.** If the build configuration is wrong, the
  import fails instead of silently working from the working directory. That
  makes the tests meaningful.
- **Tests exercise the real artifact.** The suite runs against what `pip
  install` produced, which is also what CI and future users run.

The trade-off is one extra directory level and the requirement to install the
project (editable installation is enough) before importing it.

## Distribution name and import package name

Two names exist and must not be confused:

| Purpose | Name | Where it appears |
|---|---|---|
| Distribution (what `pip` installs) | `spotify-music-clustering` | `[project].name` in `pyproject.toml`, `pip install` commands |
| Import package (what Python imports) | `spotify_music_clustering` | `import` statements, module paths |
| Console command | `spotify-cluster` | `[project.scripts]`, shell commands |

Python import names cannot contain hyphens, which is why the distribution uses
hyphens and the package uses underscores. The console command is a third name
chosen for typing convenience.

The version is declared once, as `__version__` in
`src/spotify_music_clustering/__init__.py`, and read by the build backend through
`[tool.setuptools.dynamic]`. There is no second copy to keep in sync.

## Package contents

```text
src/spotify_music_clustering/
├── __init__.py   # Package docstring and __version__
├── __main__.py   # Enables `python -m spotify_music_clustering`
└── app.py        # Status report, run(), and the console-script main()
```

- `__init__.py` marks the directory as a regular package and exposes the
  version. It contains no side effects.
- `__main__.py` makes the package executable as a module. It delegates to
  `app.main()`, so both entry points share one code path.
- `app.py` contains the only application behavior in this milestone: building a
  short status report and printing it. It has no dependency on data, models, or
  the working directory.

`app.run()` returns an exit code and `app.main()` raises `SystemExit` with it.
That separation keeps the logic testable in-process while still producing a
correct process exit status for shells and CI.

## Entry points

| Invocation | Path |
|---|---|
| `python -m spotify_music_clustering` | `__main__.py` → `app.main()` |
| `spotify-cluster` | generated launcher → `app:main` from `[project.scripts]` |

Both must remain equivalent. The test suite compares their stdout to catch
divergence.

## Intended data pipeline

The future pipeline is a sequence of stages, each producing a durable output:

```text
data/raw/dataset.csv
        │
        ▼
ingestion and validation        (schema, duplicates, missing values)
        │
        ▼
cleaning and feature selection  (analysis-ready numeric features)
        │
        ▼
normalization                   (comparable feature scales)
        │
        ├──────────────► dimensionality reduction (PCA, t-SNE)
        │
        ▼
clustering                      (K-Means, Gaussian Mixture Models)
        │
        ▼
evaluation and comparison       (internal metrics, stability)
        │
        ▼
profiling and visualization     (cluster descriptions, figures)
        │
        ▼
artifacts/                      (configs, metrics, figures, models)
```

This is a conceptual flow, not a module map. Stage boundaries will be fixed when
each stage is implemented, so that code follows demonstrated needs rather than
speculation.

## Separation of concerns

| Location | Contents | Versioned |
|---|---|---|
| `src/` | Importable logic | Yes |
| `tests/` | Automated verification | Yes |
| `configs/` | Experiment parameters | Yes, once they exist |
| `data/raw/` | Original dataset, unmodified | No |
| `data/processed/` | Derived datasets | No |
| `artifacts/` | Figures, metrics, models, reports | No |
| `docs/` | Architecture, development, methodology | Yes |

Configuration is separate from code so that an experiment can be described
without editing Python. Tests are separate from source so that the shipped
package stays free of test-only dependencies. Artifacts are separate from both
so that a result can be deleted and regenerated without touching the code that
produced it.

## Why raw research data stays out of version control

- **Size.** The dataset is large enough to bloat history and slow clones.
- **Licensing.** Kaggle terms govern the data. Committing it would redistribute
  it under terms this repository cannot grant.
- **Provenance.** A file obtained from its documented source is traceable; a copy
  inside a repository history is not.
- **Immutability.** `data/raw/` is treated as read-only input. Deriving new files
  into `data/processed/` preserves the ability to re-run from the original.

The same reasoning applies to generated artifacts: they are outputs, and outputs
should be reproducible rather than archived in Git.

## Implemented versus planned

**Implemented now**

- Installable `src`-layout package with a single version source.
- Module and console entry points sharing one function.
- Bootstrap smoke tests covering import, both entry points, and output.
- Ruff lint and format configuration.
- GitHub Actions workflow: lint, format check, tests, build, wheel smoke test.
- Ignore rules for environments, data, artifacts, secrets, and tool caches.
- This architecture note, a development guide, and the README.

**Planned**

- Dataset ingestion and validation against the real file.
- Cleaning, feature selection, and normalization.
- Dimensionality reduction and clustering experiments.
- Evaluation, stability analysis, and cluster profiling.
- Configuration-driven experiment runs and recorded artifacts.
- Methodology documentation backed by actual results.

Until a planned item appears in code, tests, and documentation, it should be
described as planned.

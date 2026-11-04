"""Application entry point for the Spotify Music Clustering project.

This module intentionally contains no analysis logic. It reports the state of
the local environment so that a fresh checkout can be verified before the
analytical pipeline exists.
"""

from __future__ import annotations

import platform
import sys

from spotify_music_clustering import __version__

PROJECT_NAME = "Spotify Music Clustering"
PIPELINE_STATUS = "analysis pipeline not implemented yet"


def build_status_report(python_executable: str | None = None) -> str:
    """Return a short, human-readable report about this installation.

    Args:
        python_executable: Interpreter path to report. Defaults to the path of
            the interpreter currently running this code.

    Returns:
        A multi-line status report suitable for terminal output.
    """
    executable = python_executable or sys.executable
    python_version = platform.python_version()
    return "\n".join(
        [
            f"{PROJECT_NAME} {__version__}",
            f"Status: repository bootstrap complete; {PIPELINE_STATUS}",
            f"Python {python_version} at {executable}",
        ]
    )


def run() -> int:
    """Print the status report and return a process exit code."""
    print(build_status_report())
    return 0


def main() -> None:
    """Console-script entry point."""
    raise SystemExit(run())

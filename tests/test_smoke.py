"""Bootstrap smoke tests for the installed project.

These tests verify packaging, entry points, and the status report. They say
nothing about analytical correctness, because no analysis code exists yet.
"""

from __future__ import annotations

import subprocess
import sys
import sysconfig
from pathlib import Path

import spotify_music_clustering
from spotify_music_clustering import app

CONSOLE_SCRIPT_NAME = "spotify-cluster"


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    """Run a command and capture its output without raising on failure."""
    return subprocess.run(command, capture_output=True, check=False, text=True)


def _console_script_path() -> Path:
    """Return the installed ``spotify-cluster`` executable for this interpreter."""
    scripts_dir = Path(sysconfig.get_path("scripts"))
    candidates = [scripts_dir / CONSOLE_SCRIPT_NAME]
    if sys.platform == "win32":
        candidates.append(scripts_dir / f"{CONSOLE_SCRIPT_NAME}.exe")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise AssertionError(
        f"console script {CONSOLE_SCRIPT_NAME!r} was not found in {scripts_dir}; "
        "install the project with: python -m pip install -e '.[dev]'"
    )


def test_package_is_importable_from_src_layout() -> None:
    package_file = Path(spotify_music_clustering.__file__).resolve()

    assert package_file.name == "__init__.py"
    assert "src" in package_file.parts
    assert spotify_music_clustering.__version__ == "0.1.0"


def test_run_prints_expected_status(capsys) -> None:
    exit_code = app.run()
    captured = capsys.readouterr()

    assert exit_code == 0
    assert app.PROJECT_NAME in captured.out
    assert spotify_music_clustering.__version__ in captured.out
    assert "repository bootstrap complete" in captured.out
    assert app.PIPELINE_STATUS in captured.out
    assert sys.executable in captured.out
    assert captured.err == ""


def test_status_report_uses_requested_interpreter() -> None:
    report = app.build_status_report(python_executable="/example/python")

    assert report.splitlines()[-1].endswith("at /example/python")


def test_module_entry_point_runs() -> None:
    result = _run([sys.executable, "-m", "spotify_music_clustering"])

    assert result.returncode == 0, result.stderr
    assert app.PROJECT_NAME in result.stdout
    assert result.stderr == ""


def test_console_script_matches_module_output() -> None:
    module_result = _run([sys.executable, "-m", "spotify_music_clustering"])
    script_result = _run([str(_console_script_path())])

    assert script_result.returncode == 0, script_result.stderr
    assert script_result.stdout == module_result.stdout
    assert script_result.stderr == ""

"""Tests for the shared shell helper functions."""

import subprocess
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "src" / "sh" / "shell_utils.sh"


def test_handle_interruption_logs_and_exits():
    """handle_interruption prints its abort message and exits 1, with no missing-command error."""
    result = subprocess.run(
        ["bash", "-c", f'source "{SCRIPT}" && handle_interruption'],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "Script execution aborted by the user." in result.stdout
    assert "command not found" not in result.stderr

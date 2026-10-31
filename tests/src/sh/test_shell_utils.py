# version: 1.1.4
# created: 2026-10-30
# updated: 2026-10-31
"""Tests for the shared shell helper functions."""

import subprocess

import pytest
from _paths import SCRIPTS_DIR

SCRIPT = SCRIPTS_DIR / "shell_utils.sh"


def run_with_utils(command):
    """Source shell_utils.sh in a fresh bash, run the command, and return the result."""
    return subprocess.run(
        ["bash", "-c", f'source "{SCRIPT}" && {command}'],
        capture_output=True,
        text=True,
        check=False,
    )


# MoSCoW: Should — every script's Ctrl+C trap calls handle_interruption
def test_handle_interruption_logs_and_exits():
    """handle_interruption prints its abort message and exits 1, with no missing-command error."""
    result = run_with_utils("handle_interruption")
    assert result.returncode == 1, "handle_interruption should exit 1"
    assert "Script execution aborted by the user." in result.stdout, f"expected the abort message: {result.stdout}"
    assert "command not found" not in result.stderr, f"a command it calls is missing: {result.stderr}"


# MoSCoW: Could — template starter helpers, unused by the scripts today
@pytest.mark.parametrize(("function", "kind"), [("dir_exists", "dir"), ("file_exists", "file")])
def test_exists_helpers(tmp_path, function, kind):
    """dir_exists and file_exists succeed only for a path of the right kind."""
    folder = tmp_path / "folder"
    folder.mkdir()
    file = tmp_path / "file.txt"
    file.write_text("x\n")
    right, wrong = (folder, file) if kind == "dir" else (file, folder)
    assert run_with_utils(f'{function} "{right}"').returncode == 0, f"{function} should succeed for a {kind}"
    assert run_with_utils(f'{function} "{wrong}"').returncode == 1, f"{function} should fail for the wrong kind of path"
    assert run_with_utils(f'{function} "{tmp_path / "missing"}"').returncode == 1, (
        f"{function} should fail for a missing path"
    )


# MoSCoW: Could — guards against running the library by mistake
def test_running_directly_is_refused():
    """Running shell_utils.sh directly, rather than sourcing it, exits 1 with an explanation."""
    result = subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 1, "running shell_utils.sh directly should exit 1"
    assert "meant to be sourced" in result.stderr, f"expected the 'meant to be sourced' explanation: {result.stderr}"


# MoSCoW: Must — shared number parsing used by three scripts
@pytest.mark.parametrize(("value", "expected"), [("7", "7"), ("010", "10"), ("08", "8"), ("123456789", "123456789")])
def test_to_whole_number_reads_base_ten(value, expected):
    """to_whole_number prints the base-10 value, so a leading zero isn't read as octal."""
    result = run_with_utils(f'to_whole_number "{value}"')
    assert result.returncode == 0, f"to_whole_number should accept {value!r}: {result.stderr}"
    assert result.stdout.strip() == expected, f"{value!r} should read as {expected}"


# MoSCoW: Must — shared input validation used by three scripts
@pytest.mark.parametrize("value", ["", "abc", "-5", "1.5", "1234567890"])
def test_to_whole_number_rejects_non_numbers(value):
    """to_whole_number fails on anything that isn't 1 to 9 digits, which keeps it clear of 64-bit overflow."""
    assert run_with_utils(f'to_whole_number "{value}"').returncode == 1, f"to_whole_number should reject {value!r}"

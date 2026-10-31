# version: 1.1.2
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


def test_handle_interruption_logs_and_exits():
    """handle_interruption prints its abort message and exits 1, with no missing-command error."""
    result = run_with_utils("handle_interruption")
    assert result.returncode == 1
    assert "Script execution aborted by the user." in result.stdout
    assert "command not found" not in result.stderr


def test_log_message_adds_a_leading_blank_line_by_default():
    """log_message prints a blank line, then the message."""
    result = run_with_utils('log_message "${INFO}" "hello"')
    assert result.stdout.startswith("\n")
    assert "hello" in result.stdout


def test_log_message_can_skip_the_blank_line():
    """Passing false as the third argument drops the leading blank line."""
    result = run_with_utils('log_message "${INFO}" "hello" false')
    assert not result.stdout.startswith("\n")
    assert "hello" in result.stdout


def test_print_section_header_wraps_the_message():
    """print_section_header prints the message between two rule lines."""
    result = run_with_utils('print_section_header "${INFO}" "Section"')
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    assert len(lines) == 3
    assert "# Section" in lines[1]
    assert "#----" in lines[0] and "#----" in lines[2]


@pytest.mark.parametrize(("function", "kind"), [("dir_exists", "dir"), ("file_exists", "file")])
def test_exists_helpers(tmp_path, function, kind):
    """dir_exists and file_exists succeed only for a path of the right kind."""
    folder = tmp_path / "folder"
    folder.mkdir()
    file = tmp_path / "file.txt"
    file.write_text("x\n")
    right, wrong = (folder, file) if kind == "dir" else (file, folder)
    assert run_with_utils(f'{function} "{right}"').returncode == 0
    assert run_with_utils(f'{function} "{wrong}"').returncode == 1
    assert run_with_utils(f'{function} "{tmp_path / "missing"}"').returncode == 1


def test_running_directly_is_refused():
    """Running shell_utils.sh directly, rather than sourcing it, exits 1 with an explanation."""
    result = subprocess.run(["bash", str(SCRIPT)], capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert "meant to be sourced" in result.stderr


@pytest.mark.parametrize(("value", "expected"), [("7", "7"), ("010", "10"), ("08", "8"), ("123456789", "123456789")])
def test_to_whole_number_reads_base_ten(value, expected):
    """to_whole_number prints the base-10 value, so a leading zero isn't read as octal."""
    result = run_with_utils(f'to_whole_number "{value}"')
    assert result.returncode == 0
    assert result.stdout.strip() == expected


@pytest.mark.parametrize("value", ["", "abc", "-5", "1.5", "1234567890"])
def test_to_whole_number_rejects_non_numbers(value):
    """to_whole_number fails on anything that isn't 1 to 9 digits, which keeps it clear of 64-bit overflow."""
    assert run_with_utils(f'to_whole_number "{value}"').returncode == 1

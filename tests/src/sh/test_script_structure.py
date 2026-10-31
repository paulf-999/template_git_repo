# version: 1.0.1
# created: 2026-10-31
# updated: 2026-10-31
"""Checks every script in src/sh/, and the bash script template itself, follows the template's structure."""

import re

import pytest
from _paths import REPO_ROOT, SH_DIR

TEMPLATE = REPO_ROOT / "src" / "templates" / "bash_script_template.sh"
# shell_utils.sh is a library that other scripts source, not a script that runs on its own
LIBRARIES = {"shell_utils.sh"}
SCRIPTS = sorted(path for path in SH_DIR.glob("*.sh") if path.name not in LIBRARIES)

# the parts of src/templates/bash_script_template.sh every script must keep, in this order
REQUIRED_PARTS = [
    ("shebang", r"#!/bin/bash"),
    ("version header", r"# version: \S+"),
    ("strict mode", r"set -euo pipefail\b.*"),
    ("description line", r"# Description: .+"),
    ("usage line", r"# Usage: .+"),
    ("shell_utils.sh source", r"source src/sh/shell_utils\.sh"),
    ("Ctrl+C trap", r"trap handle_interruption SIGINT"),
    ("Variables section", r"# Variables"),
    ("Functions section", r"# Functions"),
    ("Main script logic section", r"# Main script logic"),
    ("start message", r'print_section_header "\$\{DEBUG\}" "Script execution started\."'),
    ("completed message", r'print_section_header "\$\{DEBUG\}" "Script execution completed\."( && echo)?'),
]


def problems_with(path):
    """Return each required part that's missing or out of order in the script, as readable messages."""
    lines = path.read_text().splitlines()
    problems, last_found = [], -1
    for name, pattern in REQUIRED_PARTS:
        found = next((n for n, line in enumerate(lines) if re.fullmatch(pattern, line)), None)
        if found is None:
            problems.append(f"missing the {name}")
        elif found < last_found:
            problems.append(f"the {name} (line {found + 1}) is out of order")
        else:
            last_found = found
    return problems


def test_scripts_are_found():
    """The scan finds the scripts, so an empty glob can't make every other test pass by default."""
    assert len(SCRIPTS) >= 5, f"expected at least 5 scripts in src/sh/, found {[p.name for p in SCRIPTS]}"


@pytest.mark.parametrize("path", [TEMPLATE, *SCRIPTS], ids=lambda path: path.name)
def test_script_follows_the_template(path):
    """Each script keeps every part of the bash script template, in the template's order."""
    problems = problems_with(path)
    assert not problems, f"{path.relative_to(REPO_ROOT)} doesn't follow {TEMPLATE.relative_to(REPO_ROOT)}: {problems}"


def test_a_missing_part_is_reported(tmp_path):
    """A script with no completed message is caught, so the check can't silently pass everything."""
    script = tmp_path / "broken.sh"
    script.write_text(TEMPLATE.read_text().replace('"Script execution completed."', '"Done."'))
    assert problems_with(script) == ["missing the completed message"]


def test_an_out_of_order_part_is_reported(tmp_path):
    """A section moved above an earlier one is reported as out of order."""
    script = tmp_path / "reordered.sh"
    text = TEMPLATE.read_text().replace("# Functions\n", "# Placeholder\n")
    script.write_text("# Functions\n" + text)
    assert any("Functions section" in problem and "out of order" in problem for problem in problems_with(script))

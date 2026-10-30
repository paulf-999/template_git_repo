# version: 1.0.0
# created: 2026-10-30
# updated: 2026-10-30
"""Checks every tracked file opens with a version/created/updated metadata header (see CONTRIBUTING.md)."""

import re
import subprocess
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
HEADER_FIELDS = ("version", "created", "updated")

# copied into every new PR or issue body, or kept empty, so they carry no header
EXEMPT = {
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    "src/templates/jinja/.gitkeep",
}


def tracked_files():
    """Return every file git tracks in the repo, minus the exempt ones."""
    output = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    return [path for path in output.splitlines() if path not in EXEMPT]


def header_lines(path):
    """Return the three lines where the header belongs: line 1, or after a shebang or YAML '---'."""
    lines = (REPO_ROOT / path).read_text().splitlines()
    start = 1 if lines and (lines[0].startswith("#!") or lines[0] == "---") else 0
    return lines[start : start + 3]


def header_pattern(path, field):
    """Return the regex for one header line, using HTML comments in markdown and '#' comments elsewhere."""
    value = r"\d+\.\d+\.\d+" if field == "version" else r"\d{4}-\d{2}-\d{2}"
    if path.endswith(".md"):
        return rf"<!-- {field}: ({value}) -->"
    return rf"# {field}: ({value})"


@pytest.mark.parametrize("path", tracked_files())
def test_file_has_metadata_header(path):
    """Each file has version, created and updated lines in order, with real dates and created <= updated."""
    values = {}
    for line, field in zip(header_lines(path), HEADER_FIELDS):
        match = re.fullmatch(header_pattern(path, field), line)
        assert match, f"{path}: expected the '{field}' header line here, got {line!r}"
        values[field] = match.group(1)
    assert len(values) == len(HEADER_FIELDS), f"{path}: the header needs version, created and updated lines"
    created = date.fromisoformat(values["created"])
    updated = date.fromisoformat(values["updated"])
    assert created <= updated, f"{path}: updated ({updated}) is earlier than created ({created})"

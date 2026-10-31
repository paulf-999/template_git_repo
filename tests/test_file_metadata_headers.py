# version: 1.2.0
# created: 2026-10-30
# updated: 2026-10-31
"""Checks every tracked file opens with a version/created/updated header (see docs/maintenance/file_headers.md)."""

import re
import subprocess
from datetime import date

import pytest
from _paths import REPO_ROOT

HEADER_FIELDS = ("version", "created", "updated")

# no header: copied into every new PR or issue body, kept empty, or kept verbatim so GitHub detects the licence
EXEMPT = {
    "LICENSE",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    "src/templates/jinja/.gitkeep",
}


def tracked_files():
    """Return every file git tracks in the repo, minus the exempt ones."""
    output = subprocess.run(["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True).stdout
    return [path for path in output.splitlines() if path not in EXEMPT]


def header_lines(path, root):
    """Return the three lines where the header belongs: line 1, or after a shebang or YAML '---'."""
    lines = (root / path).read_text().splitlines()
    start = 1 if lines and (lines[0].startswith("#!") or lines[0] == "---") else 0
    return lines[start : start + 3]


def header_pattern(path, field):
    """Return the regex for one header line, using HTML comments in markdown and '#' comments elsewhere."""
    value = r"\d+\.\d+\.\d+" if field == "version" else r"\d{4}-\d{2}-\d{2}"
    if path.endswith(".md"):
        return rf"<!-- {field}: ({value}) -->"
    return rf"# {field}: ({value})"


def header_problem(path, root=REPO_ROOT):
    """Return what's wrong with a file's header, or None if it has version, created and updated lines in order."""
    values = {}
    for line, field in zip(header_lines(path, root), HEADER_FIELDS):
        match = re.fullmatch(header_pattern(path, field), line)
        if not match:
            return f"{path}: expected the '{field}' header line here, got {line!r}"
        values[field] = match.group(1)
    if len(values) < len(HEADER_FIELDS):
        return f"{path}: the header needs version, created and updated lines"
    try:
        created, updated = date.fromisoformat(values["created"]), date.fromisoformat(values["updated"])
    except ValueError as error:  # the regex allows impossible dates like 2026-13-45
        return f"{path}: {error}"
    if created > updated:
        return f"{path}: updated ({updated}) is earlier than created ({created})"
    return None


# one case for the whole repo, so adding a file doesn't change the test count
# MoSCoW: Must — every tracked file needs a valid header
def test_every_tracked_file_has_a_metadata_header():
    """Every tracked file has version, created and updated lines in order, with real dates and created <= updated."""
    problems = [problem for path in tracked_files() if (problem := header_problem(path))]
    assert not problems, "fix these file headers:\n" + "\n".join(problems)


# MoSCoW: Must — a check that never reports a problem would pass every file
@pytest.mark.parametrize(
    "header",
    [
        "# no header at all",
        "# version: 1.0.0\n# created: 2026-13-45\n# updated: 2026-10-31",  # month 13
        "# version: 1.0.0\n# created: 2026-10-31\n# updated: 2026-10-30",  # updated before created
    ],
)
def test_a_bad_header_is_reported(tmp_path, header):
    """A missing header, an impossible date, and an updated date before created are each reported."""
    (tmp_path / "script.sh").write_text(f"#!/bin/bash\n{header}\n")
    assert header_problem("script.sh", tmp_path), f"this header should be reported:\n{header}"

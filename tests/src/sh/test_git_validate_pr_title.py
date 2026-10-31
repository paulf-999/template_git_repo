# version: 1.0.3
# created: 2026-10-31
# updated: 2026-10-31
"""Tests for the PR title check, which keeps squash-merge commit messages on main valid."""

import os
import subprocess

import pytest
from _paths import REPO_ROOT, SCRIPTS_DIR

SCRIPT = SCRIPTS_DIR / "git_validate_pr_title.sh"


def run_check(title):
    """Run the PR title check from the repo root and return the full result."""
    return subprocess.run([str(SCRIPT), title], cwd=REPO_ROOT, capture_output=True, text=True, check=False)


# MoSCoW: Must — good PR titles must not be blocked
@pytest.mark.parametrize(
    "title",
    [
        "ci(repo): make pull request checks finish in under 10 seconds",
        "docs(readme): return to the simpler layout",
        "feat: add a thing",
        "feat(api)!: drop the old endpoint",
        "fix(src/sh): handle README updates",
    ],
)
def test_valid_titles_pass(title):
    """Conventional Commits titles with a lowercase scope and description exit 0."""
    result = run_check(title)
    assert result.returncode == 0, result.stdout


# MoSCoW: Must — bad PR titles must be blocked with a reason
@pytest.mark.parametrize(
    ("title", "expected_error"),
    [
        ("Update the README", "type(scope): description"),
        ("feature(ci): add a check", "type(scope): description"),
        ("feat(CI): add a check", "type(scope): description"),
        ("feat:add a check", "type(scope): description"),
        ("feat(ci): Add a check", "lowercase letter"),
        ("feat(ci): add a check.", "full stop"),
        ("feat(ci): " + "x" * 91, "Keep the title to 100 characters"),
    ],
)
def test_invalid_titles_fail_with_a_reason(title, expected_error):
    """A title commitlint would reject exits 1 and says what to fix."""
    result = run_check(title)
    assert result.returncode == 1, f"{title!r} should be blocked"
    assert expected_error in result.stdout, f"expected '{expected_error}' in the reason: {result.stdout}"


# MoSCoW: Must — security: a PR title must never run as code
def test_title_with_shell_characters_is_not_executed(tmp_path):
    """The title is treated as text, so shell syntax in it is never run."""
    # the path is passed in a variable, so the title stays under the 100-character limit
    marker = tmp_path / "should_not_exist"
    title = "feat(ci): add $(touch $MARKER) check"
    env = {**os.environ, "MARKER": str(marker)}
    result = subprocess.run([str(SCRIPT), title], cwd=REPO_ROOT, env=env, capture_output=True, text=True, check=False)
    assert result.returncode == 0, f"the title is valid once its shell syntax is read as text: {result.stdout}"
    assert not marker.exists(), "the $(...) in the title was run as a command"

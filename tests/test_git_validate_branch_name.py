"""Tests for the git branch name validation pre-commit hook."""

import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "src" / "sh" / "git_validate_branch_name.sh"


def run_hook(branch_name):
    """Run the hook script from the repo root with the given branch name and return its exit code."""
    return subprocess.run([str(SCRIPT), branch_name], cwd=REPO_ROOT, capture_output=True, check=False).returncode


@pytest.mark.parametrize("branch_name", ["feature/x_1", "hotfix/a", "release/b_2"])
def test_valid_branch_names_pass(branch_name):
    """Valid branch names exit 0."""
    assert run_hook(branch_name) == 0


@pytest.mark.parametrize("branch_name", ["main", "feature/My-Change", "feat/x", "feature/"])
def test_invalid_branch_names_fail(branch_name):
    """Invalid branch names exit 1."""
    assert run_hook(branch_name) == 1

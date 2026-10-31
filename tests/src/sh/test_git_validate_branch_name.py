# version: 1.0.1
# created: 2026-10-30
# updated: 2026-10-31
"""Tests for the git branch name validation pre-commit hook."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "src" / "sh" / "git_validate_branch_name.sh"


def run_hook(branch_name):
    """Run the hook script from the repo root with the given branch name and return its exit code."""
    return subprocess.run([str(SCRIPT), branch_name], cwd=REPO_ROOT, capture_output=True, check=False).returncode


# MoSCoW: Must — good branch names must not be blocked
@pytest.mark.parametrize("branch_name", ["feature/x_1", "hotfix/a", "release/b_2"])
def test_valid_branch_names_pass(branch_name):
    """Valid branch names exit 0."""
    assert run_hook(branch_name) == 0


# MoSCoW: Must — bad branch names must be blocked
@pytest.mark.parametrize("branch_name", ["main", "feature/My-Change", "feat/x", "feature/"])
def test_invalid_branch_names_fail(branch_name):
    """Invalid branch names exit 1."""
    assert run_hook(branch_name) == 1


# MoSCoW: Could — wording of the error message
def test_error_explains_the_naming_rule():
    """An invalid name prints the regex and the allowed prefixes, so the fix is clear."""
    result = subprocess.run([str(SCRIPT), "bad-name"], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    assert "^(feature|hotfix|release)/[a-z0-9_]+$" in result.stdout
    assert "'feature/', 'hotfix/' or 'release/'" in result.stdout


# MoSCoW: Must — this is how the pre-commit hook calls the script
@pytest.mark.parametrize(("current_branch", "expected_code"), [("feature/from_git", 0), ("Bad-Branch", 1)])
def test_defaults_to_the_current_branch(tmp_path, current_branch, expected_code):
    """With no argument, the script checks the current git branch."""
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    subprocess.run(["git", "init", "-q", "-b", current_branch], cwd=tmp_path, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "x"], cwd=tmp_path, env=env, check=True)
    # the script sources src/sh/shell_utils.sh from the repo root, as in the real repo
    (tmp_path / "src" / "sh").mkdir(parents=True)
    shutil.copy(REPO_ROOT / "src" / "sh" / "shell_utils.sh", tmp_path / "src" / "sh" / "shell_utils.sh")
    result = subprocess.run([str(SCRIPT)], cwd=tmp_path, env=env, capture_output=True, check=False)
    assert result.returncode == expected_code

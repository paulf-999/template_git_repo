# version: 1.0.3
# created: 2026-10-30
# updated: 2026-10-31
"""Tests for the git branch name validation pre-commit hook."""

import os
import shutil
import subprocess

import pytest
from _paths import REPO_ROOT, SCRIPTS_DIR

SCRIPT = SCRIPTS_DIR / "git_validate_branch_name.sh"


def run_hook(branch_name):
    """Run the hook script from the repo root with the given branch name and return its exit code."""
    return subprocess.run([str(SCRIPT), branch_name], cwd=REPO_ROOT, capture_output=True, check=False).returncode


def repo_on_branch(repo, branch):
    """Make the folder a git repo with one commit on the branch, and return an env that skips the user's git config."""
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    subprocess.run(["git", "init", "-q", "-b", branch], cwd=repo, env=env, check=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "x"], cwd=repo, env=env, check=True)
    # the script sources scripts/shell_utils.sh from the repo root, as in the real repo
    (repo / "scripts").mkdir(parents=True)
    shutil.copy(SCRIPTS_DIR / "shell_utils.sh", repo / "scripts" / "shell_utils.sh")
    return env


# MoSCoW: Must — good branch names must not be blocked
@pytest.mark.parametrize("branch_name", ["feature/x_1", "hotfix/a", "release/b_2"])
def test_valid_branch_names_pass(branch_name):
    """Valid branch names exit 0."""
    assert run_hook(branch_name) == 0, f"{branch_name} should pass"


# MoSCoW: Must — bad branch names must be blocked
@pytest.mark.parametrize("branch_name", ["main", "feature/My-Change", "feat/x", "feature/"])
def test_invalid_branch_names_fail(branch_name):
    """Invalid branch names exit 1."""
    assert run_hook(branch_name) == 1, f"{branch_name} should be blocked"


# MoSCoW: Could — wording of the error message
def test_error_explains_the_naming_rule():
    """An invalid name prints the regex and the allowed prefixes, so the fix is clear."""
    result = subprocess.run([str(SCRIPT), "bad-name"], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    assert "^(feature|hotfix|release)/[a-z0-9_]+$" in result.stdout, f"expected the naming rule: {result.stdout}"
    assert "'feature/', 'hotfix/' or 'release/'" in result.stdout, f"expected the allowed prefixes: {result.stdout}"


# MoSCoW: Must — this is how the pre-commit hook calls the script
@pytest.mark.parametrize(("current_branch", "expected_code"), [("feature/from_git", 0), ("Bad-Branch", 1)])
def test_defaults_to_the_current_branch(tmp_path, current_branch, expected_code):
    """With no argument, the script checks the current git branch."""
    env = repo_on_branch(tmp_path, current_branch)
    result = subprocess.run([str(SCRIPT)], cwd=tmp_path, env=env, capture_output=True, text=True, check=False)
    assert result.returncode == expected_code, f"{current_branch} should exit {expected_code}: {result.stdout}"

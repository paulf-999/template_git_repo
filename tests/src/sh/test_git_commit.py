# version: 1.2.2
# created: 2026-10-30
# updated: 2026-10-31
"""Tests for the interactive git commit helper."""

import os
import re
import shutil
import subprocess

import pytest
from _paths import SCRIPTS_DIR

SCRIPT = SCRIPTS_DIR / "git_commit.sh"


def read_script_types():
    """Return the commit types listed in git_commit.sh's TYPES array, in menu order."""
    match = re.search(r"^TYPES=\(([^)]*)\)", SCRIPT.read_text(), re.MULTILINE)
    return re.findall(r'"([^"]+)"', match.group(1))


# type-enum from @commitlint/config-conventional, at the version pinned in .pre-commit-config.yaml
COMMITLINT_TYPES = ["build", "chore", "ci", "docs", "feat", "fix", "perf", "refactor", "revert", "style", "test"]


@pytest.fixture
def git_repo(tmp_path):
    """Create an isolated git repo with one staged file, plus an env that ignores the user's git config."""
    env = {
        **os.environ,
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_AUTHOR_NAME": "Test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "Test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, env=env, check=True)
    # the helper sources src/sh/shell_utils.sh from the repo root, as in the real repo
    (tmp_path / "src" / "sh").mkdir(parents=True)
    shutil.copy(SCRIPTS_DIR / "shell_utils.sh", tmp_path / "src" / "sh" / "shell_utils.sh")
    (tmp_path / "app.py").write_text("print('hi')\n")
    subprocess.run(["git", "add", "app.py"], cwd=tmp_path, env=env, check=True)
    return tmp_path, env


def run_commit_helper(repo, env, answers, *args):
    """Run git_commit.sh in the repo, feeding the menu answers through stdin."""
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=repo,
        env=env,
        input="\n".join(answers) + "\n",
        capture_output=True,
        text=True,
        check=False,
    )


def last_commit_subject(repo, env):
    """Return the subject line of the repo's latest commit."""
    return subprocess.run(
        ["git", "log", "-1", "--format=%s"], cwd=repo, env=env, capture_output=True, text=True, check=True
    ).stdout.strip()


def test_types_match_commitlint():
    """Every type commitlint allows is offered by the helper, and no others."""
    assert sorted(read_script_types()) == sorted(COMMITLINT_TYPES)


@pytest.mark.parametrize("commit_type", ["test", "perf"])
def test_commit_with_new_type(git_repo, commit_type):
    """The newly added types produce a '<type>(<scope>): <message>' commit."""
    repo, env = git_repo
    menu_number = str(read_script_types().index(commit_type) + 1)
    result = run_commit_helper(repo, env, [menu_number, "1", "add a check", "y"])
    assert result.returncode == 0, result.stderr
    assert last_commit_subject(repo, env) == f"{commit_type}(app): add a check"


def test_files_in_one_folder_share_a_scope(git_repo):
    """Staged files are grouped by top-level folder, so each repo area is offered once."""
    repo, env = git_repo
    (repo / ".github").mkdir()
    for path in ("api/a.py", "api/b.py", ".github/ci.yml"):
        (repo / path).parent.mkdir(exist_ok=True)
        (repo / path).write_text("x\n")
        subprocess.run(["git", "add", path], cwd=repo, env=env, check=True)
    result = run_commit_helper(repo, env, ["1", "3", "tidy up", "y"])
    assert result.returncode == 0, result.stderr
    # git lists staged paths alphabetically: .github/, api/, then app.py
    assert result.stdout.count(") api") == 1, result.stdout
    assert ") github" in result.stdout
    assert last_commit_subject(repo, env) == "chore(app): tidy up"


def test_custom_scope(git_repo):
    """Option 0 takes a typed scope, with spaces turned into hyphens."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "0", "my scope", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert last_commit_subject(repo, env) == "chore(my-scope): add notes"


def test_declining_the_confirm_prompt_makes_no_commit(git_repo):
    """Answering 'n' at the confirm prompt exits cleanly without committing."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", "add notes", "n"])
    assert result.returncode == 0, result.stderr
    head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=repo, env=env, capture_output=True, check=False)
    assert head.returncode != 0, "a commit was made despite answering 'n'"


def test_flags_are_passed_to_git_commit(git_repo):
    """Script arguments reach git commit, e.g. --author overrides the commit author."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", "add notes", "y"], "--author=Other <other@example.com>")
    assert result.returncode == 0, result.stderr
    author = subprocess.run(
        ["git", "log", "-1", "--format=%an"], cwd=repo, env=env, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert author == "Other"


def test_empty_message_is_rejected(git_repo):
    """An empty message exits 1 instead of committing a bare '<type>(<scope>)' subject."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", ""])
    assert result.returncode == 1
    assert "Commit message cannot be empty." in result.stdout


def test_leading_zero_menu_choice_is_read_as_decimal(git_repo):
    """'010' picks menu item 10, not item 8 (which bash would read from octal 010)."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["010", "1", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert last_commit_subject(repo, env) == f"{read_script_types()[9]}(app): add notes"


def test_menu_choice_bash_cannot_read_as_octal_still_works(git_repo):
    """'08' picks item 8, where bash on its own would stop with a 'value too great for base' error."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["08", "1", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert "value too great" not in result.stderr
    assert last_commit_subject(repo, env) == f"{read_script_types()[7]}(app): add notes"


def test_custom_scope_is_lowercased(git_repo):
    """A typed scope is lowercased, since commitlint's scope-case rule rejects 'CI'."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "0", "CI", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert last_commit_subject(repo, env) == "chore(ci): add notes"


@pytest.mark.parametrize(
    ("bad_message", "expected_error"),
    [
        ("Add notes", "lowercase letter"),
        ("add notes.", "full stop"),
        ("x" * 100, "characters"),
    ],
)
def test_messages_commitlint_would_reject_are_asked_again(git_repo, bad_message, expected_error):
    """A message commitlint would refuse is explained and asked for again, instead of failing at the hook."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", bad_message, "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert expected_error in result.stdout
    assert last_commit_subject(repo, env) == "chore(app): add notes"


def test_non_ascii_file_name_gives_a_clean_scope(git_repo):
    """A staged file like résumé.md gives the scope 'résumé', not a quoted, escaped path."""
    repo, env = git_repo
    (repo / "résumé.md").write_text("x\n")
    subprocess.run(["git", "add", "résumé.md"], cwd=repo, env=env, check=True)
    result = run_commit_helper(repo, env, ["1", "2", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert last_commit_subject(repo, env) == "chore(résumé): add notes"


def test_surrounding_spaces_are_trimmed(git_repo):
    """Spaces around the message are dropped, and an all-spaces message counts as empty and is asked again."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", "   ", "  add notes  ", "y"])
    assert result.returncode == 0, result.stderr
    assert "Commit message cannot be empty." in result.stdout
    assert last_commit_subject(repo, env) == "chore(app): add notes"


@pytest.mark.parametrize(
    ("bad_scope", "expected_error"),
    [("a)b", "Use only letters"), ("x" * 31, "Keep the scope to 30 characters")],
)
def test_unusable_custom_scope_is_asked_again(git_repo, bad_scope, expected_error):
    """A scope that would break the header, or crowd out the message, is explained and asked for again."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "0", bad_scope, "0", "ci", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert expected_error in result.stdout
    assert last_commit_subject(repo, env) == "chore(ci): add notes"


def test_huge_menu_number_is_rejected_not_wrapped(git_repo):
    """A 20-digit answer is invalid, rather than wrapping past 64 bits to a real menu item."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["18446744073709551617", "1", "1", "add notes", "y"])
    assert result.returncode == 0, result.stderr
    assert "Invalid selection" in result.stdout
    assert last_commit_subject(repo, env) == "chore(app): add notes"

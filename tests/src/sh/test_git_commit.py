# version: 1.2.11
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


# the type that menu item 1 picks, so reordering TYPES doesn't break the tests that pick it
FIRST_TYPE = read_script_types()[0]

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
    """Run git_commit.sh in the repo, feeding the menu answers through stdin.

    The script asks, in order: the type's menu number, the scope's menu number (0 = type your own scope next),
    the commit message, then 'y' or 'n' to confirm. A rejected answer is asked again, so it takes an extra entry.
    For example, ["1", "1", "add notes", "y"] picks type 1, scope 1 and the message 'add notes', then confirms.
    """
    return subprocess.run(
        ["bash", str(SCRIPT), *args],
        cwd=repo,
        env=env,
        input="\n".join(answers) + "\n",
        capture_output=True,
        text=True,
        check=False,
    )


def stage_files(repo, env, *paths):
    """Create each file with placeholder content and stage it."""
    for path in paths:
        (repo / path).parent.mkdir(parents=True, exist_ok=True)
        (repo / path).write_text("x\n")
        subprocess.run(["git", "add", path], cwd=repo, env=env, check=True)


def last_commit_subject(repo, env):
    """Return the subject line of the repo's latest commit."""
    return subprocess.run(
        ["git", "log", "-1", "--format=%s"], cwd=repo, env=env, capture_output=True, text=True, check=True
    ).stdout.strip()


# MoSCoW: Must — offered types must match what commitlint accepts
def test_types_match_commitlint():
    """Every type commitlint allows is offered by the helper, and no others."""
    assert sorted(read_script_types()) == sorted(COMMITLINT_TYPES), "git_commit.sh's TYPES should match commitlint's"


# MoSCoW: Should — the main way scopes are offered
def test_files_in_one_folder_share_a_scope(git_repo):
    """Staged files are grouped by top-level folder, so each repo area is offered once."""
    repo, env = git_repo
    stage_files(repo, env, "api/a.py", "api/b.py", ".github/ci.yml")
    # scope 3 is app, the area of the file the fixture already staged
    result = run_commit_helper(repo, env, ["1", "3", "tidy up", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    # git lists staged paths alphabetically: .github/, api/, then app.py
    assert result.stdout.count(") api") == 1, f"api should be offered once: {result.stdout}"
    assert ") github" in result.stdout, f"expected a github scope in the menu: {result.stdout}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(app): tidy up", "scope 3 should be app"


# MoSCoW: Should — option 0 is the main fallback for scopes
def test_custom_scope(git_repo):
    """Option 0 takes a typed scope, with spaces turned into hyphens."""
    repo, env = git_repo
    # scope 0, then the custom scope to type
    result = run_commit_helper(repo, env, ["1", "0", "my scope", "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(my-scope): add notes", (
        "a typed scope's spaces should become hyphens"
    )


# MoSCoW: Must — 'n' at the confirm prompt must never commit
def test_declining_the_confirm_prompt_makes_no_commit(git_repo):
    """Answering 'n' at the confirm prompt exits cleanly without committing."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", "add notes", "n"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    head = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], cwd=repo, env=env, capture_output=True, check=False)
    assert head.returncode != 0, "a commit was made despite answering 'n'"


# MoSCoW: Should — flags like --no-verify reach git commit instead of being dropped
def test_flags_are_passed_to_git_commit(git_repo):
    """Script arguments reach git commit, e.g. --author overrides the commit author."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "1", "add notes", "y"], "--author=Other <other@example.com>")
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    author = subprocess.run(
        ["git", "log", "-1", "--format=%an"], cwd=repo, env=env, capture_output=True, text=True, check=True
    ).stdout.strip()
    assert author == "Other", "--author should reach git commit"


# MoSCoW: Should — an empty message is caught before commitlint rejects the bare '<type>(<scope>)' subject
@pytest.mark.parametrize("empty_message", ["", "   "])
def test_empty_message_is_asked_again(git_repo, empty_message):
    """An empty or all-spaces message is explained and asked for again, so no bare '<type>(<scope>)' is committed."""
    repo, env = git_repo
    # the empty message is rejected, so the message is asked again
    result = run_commit_helper(repo, env, ["1", "1", empty_message, "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert "Commit message cannot be empty." in result.stdout, f"expected the empty-message error: {result.stdout}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(app): add notes", "the next message should be used"


# MoSCoW: Could — wiring check that menu input uses to_whole_number
def test_leading_zero_menu_choice_is_read_as_decimal(git_repo):
    """'010' picks menu item 10, not item 8 (which bash would read from octal 010)."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["010", "1", "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert last_commit_subject(repo, env) == f"{read_script_types()[9]}(app): add notes", "'010' should pick item 10"


# MoSCoW: Should — a mistyped menu number is explained and asked again
def test_invalid_type_number_is_asked_again(git_repo):
    """A number that isn't on the type menu is rejected, and the next valid answer is used."""
    repo, env = git_repo
    # type 99 is rejected, so type is asked again and 1 is used
    result = run_commit_helper(repo, env, ["99", "1", "1", "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert "Invalid selection" in result.stdout, f"expected the rejected number to be explained: {result.stdout}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(app): add notes", "the next valid answer should be used"


# MoSCoW: Should — commitlint rejects uppercase scopes
def test_custom_scope_is_lowercased(git_repo):
    """A typed scope is lowercased, since commitlint's scope-case rule rejects 'CI'."""
    repo, env = git_repo
    result = run_commit_helper(repo, env, ["1", "0", "CI", "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(ci): add notes", "a typed scope should be lowercased"


# MoSCoW: Should — catches commitlint errors before the hook does
@pytest.mark.parametrize(
    ("bad_message", "expected_error"),
    [
        ("Add notes", "lowercase letter"),
        ("add notes.", "full stop"),
    ],
)
def test_messages_commitlint_would_reject_are_asked_again(git_repo, bad_message, expected_error):
    """A message commitlint would refuse is explained and asked for again, instead of failing at the hook."""
    repo, env = git_repo
    # the bad message is rejected, so the message is asked again
    result = run_commit_helper(repo, env, ["1", "1", bad_message, "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert expected_error in result.stdout, f"expected '{expected_error}' in the explanation: {result.stdout}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(app): add notes", (
        "the message given after the rejected one should be used"
    )


# MoSCoW: Should — catches scopes commitlint would refuse before the hook does
@pytest.mark.parametrize(
    ("bad_scope", "expected_error"),
    [
        ("", "Scope cannot be empty"),
        ("bad!scope", "Use only letters"),
        ("x" * 31, "30 characters"),
    ],
)
def test_invalid_custom_scope_is_asked_again(git_repo, bad_scope, expected_error):
    """An empty, badly spelt or over-long typed scope is explained, then option 0 can be picked again."""
    repo, env = git_repo
    # scope 0 and the bad scope are rejected, so the scope menu is asked again: 0, then a good scope
    result = run_commit_helper(repo, env, ["1", "0", bad_scope, "0", "docs", "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert expected_error in result.stdout, f"expected '{expected_error}' in the explanation: {result.stdout}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(docs): add notes", "the next valid scope should be used"


# MoSCoW: Must — the header limit is commitlint's header-max-length, so test both sides of it
def test_header_at_the_limit_is_accepted_and_one_over_is_not(git_repo):
    """A message that makes the header one character too long is rejected, and one that exactly fills it is used."""
    repo, env = git_repo
    # read MAX_HEADER_LENGTH from the script, then fill the header after "<type>(app): " exactly to it
    max_header_length = int(re.search(r"^MAX_HEADER_LENGTH=(\d+)", SCRIPT.read_text(), re.MULTILINE).group(1))
    longest_message = "x" * (max_header_length - len(f"{FIRST_TYPE}(app): "))
    # the message one character over is rejected, so the message is asked again
    result = run_commit_helper(repo, env, ["1", "1", f"{longest_message}x", longest_message, "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert "Keep the message to" in result.stdout, f"expected the over-long message to be explained: {result.stdout}"
    assert len(last_commit_subject(repo, env)) == max_header_length, "a header exactly at the limit should be committed"


# MoSCoW: Could — rare non-ASCII file names
def test_non_ascii_file_name_gives_a_clean_scope(git_repo):
    """A staged file like résumé.md gives the scope 'résumé', not a quoted, escaped path."""
    repo, env = git_repo
    (repo / "résumé.md").write_text("x\n")
    subprocess.run(["git", "add", "résumé.md"], cwd=repo, env=env, check=True)
    # git lists app.py before résumé.md, so scope 2 is résumé
    result = run_commit_helper(repo, env, ["1", "2", "add notes", "y"])
    assert result.returncode == 0, f"the helper should finish cleanly: {result.stdout}{result.stderr}"
    assert last_commit_subject(repo, env) == f"{FIRST_TYPE}(résumé): add notes", (
        "the scope should be the plain file name"
    )

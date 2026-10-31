<!-- version: 1.0.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# CLAUDE.md — template_git_repo

This file provides repo-specific instructions for Claude Code when working in this repo. Repos created from the template should rename the heading and adapt each section to their own project.

---

## 🔍 Codebase exploration — Graphify

[Graphify](https://github.com/lucasrosati/claude-code-memory-setup) generates a local AST-based knowledge graph so structural questions (where a function is defined, which scripts source a helper, which tests cover a script) can be answered from a single file rather than reading the tree.

### ✅ When Graphify is set up

The knowledge graph is at: `graphify-out/graph.json`

Use the `/graphify` skill to query it — ask structural questions (e.g. "Which scripts source `shell_utils.sh`?", "Which tests cover `git_commit.sh`?") and the skill will query the graph directly rather than reading files.

**Before exploring the codebase manually**, check the graph first. Only open individual files when you need the content itself — not for structural orientation.

Rebuild after significant changes (run from repo root):

```bash
graphify update .
```

### ⚠️ When Graphify is not set up

Use targeted Grep and Glob rather than reading files broadly:

| Goal | Tool |
|---|---|
| Find a shell script | `Glob src/sh/<script_name>.sh` |
| Find a script's tests | `Glob tests/src/sh/test_<script_name>.py` |
| Find scripts using a helper | `Grep "<function_name>" src/sh/` |
| Find a pre-commit hook | `Grep "id: <hook_id>" .pre-commit-config.yaml` |

---

## 🛠️ Repo maintenance

Whenever a new artefact is added, the files listed below **must be updated in the same PR**. Do not consider an addition complete without these updates.

| Artefact | Required updates |
|---|---|
| **Any new file** | Open it with the `version` / `created` / `updated` header described in `CONTRIBUTING.md`, or add it to `EXEMPT` in `tests/test_file_metadata_headers.py` if it can't carry one |
| **Any edited file** | Set `updated` to today and bump `version` (MAJOR, MINOR or PATCH), but never change `created` |
| **Shell script** (`src/sh/`) | A matching pytest file in `tests/src/sh/`, mirroring the script's path; start new scripts from `src/templates/bash_script_template.sh` |
| **Shared shell helper** (`src/sh/shell_utils.sh`) | A test in `tests/src/sh/test_shell_utils.py` |
| **Make target** (`Makefile`) | The usage comment block at the top, which `make help` prints, and `.PHONY` |
| **Pre-commit hook** (`.pre-commit-config.yaml`) | A pinned `rev`, and a name in the `<Area> checks — <question>` style the other hooks use |
| **CI job** (`.github/workflows/ci.yml`) | Actions pinned to a commit SHA, a `timeout-minutes`, and any PR input passed through `env:`, never `${{ }}` inside `run:` |

After updating the required files above, check `README.md`, `CONTRIBUTING.md` and `docs/` for pages that describe the area being changed.

---

## 🧪 Running tests

Install the requirements and git hooks once, then run the tests from the repo root:

```bash
make deps
make test
```

- **Same as CI:** `make test` runs plain `pytest`, which is what the CI `Test (pytest)` job runs.
- **Scripts run from the repo root:** every script in `src/sh/` sources `src/sh/shell_utils.sh` by a relative path, so the tests copy it into each temporary repo they create.
- **Hooks:** run `pre-commit run --all-files` before raising a PR; CI re-runs every hook, so `--no-verify` doesn't skip them.

---

## Priority reads

Files that set the conventions in this repo. Consult these before scanning broadly:

| File | Domain |
|---|---|
| `CONTRIBUTING.md` | Branching, commit messages, file headers and PR rules |
| `docs/git_branching_strategy.md` | Branch types, naming regex and the `release/` exception for 20+ file PRs |
| `.pre-commit-config.yaml` | Every local check, and the order they run in |
| `.github/workflows/ci.yml` | What CI checks on every PR |
| `src/sh/shell_utils.sh` | Shared logging and parsing helpers every script sources |
| `ruff.toml` | Python lint rules |

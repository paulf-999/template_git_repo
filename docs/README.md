# 📚 Documentation

This folder contains supporting documentation and references for working with this repository.

## 🔀 Branching & Git Workflow

- [Branching strategy](git_branching_strategy.md)
  Explains the use of `main`, feature branches, and supporting branches.

## ✅ Contribution Standards

- [Contributing guidelines](../CONTRIBUTING.md) — branching, commit conventions, PR process, and expectations.
- [Pull request template](../.github/pull_request_template.md) — structure to follow when raising a PR.

## 🧪 Testing

- Tests for the template's own scripts live in `tests/src/sh/`, mirroring `src/sh/`, and run with `pytest`, both locally and in CI.
- Projects based on this template should add tests for their own code alongside these.
- Use the PR template to document **how changes were tested**.

## ℹ️ Additional References

- [Commitlint rules](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional) (the `@commitlint/config-conventional` defaults)
- [Makefile](../Makefile) for automation tasks (`make deps`, `make install`, `make run`, `make test`, `make clean`)

<!-- version: 1.0.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# CLAUDE.md — <project_name>

> 🧩 **Starting point** — fill in the TODOs, then keep this file lean.
>
> - **Why:** Claude Code reads all of it every session, so every line costs context.
> - **Add a line:** only when Claude repeatedly gets something wrong, or can't work it out from the code.
> - **Point, don't copy:** link to `CONTRIBUTING.md` and `docs/` rather than repeating them.

## Core Principles

*Adapted from [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/)*

1. **Don't assume. Don't hide confusion. Surface tradeoffs.**
2. **Minimum code that solves the problem. Nothing speculative.**
3. **Touch only what you must. Clean up only your own mess.**
4. **Define success criteria. Loop until verified.**

- **Rule:** if any detail, requirement or architecture choice is unclear, ask one clarifying question before writing code or making changes.

## Project

<!-- TODO: what this repo does, who uses it, and anything Claude keeps getting wrong here -->

| Task | Command |
|---|---|
| Install requirements and git hooks | `make deps` |
| Run the tests | `make test` |
| Run every check | `pre-commit run --all-files` |

- **Done means:** `make test` and `pre-commit run --all-files` both pass.
- **Conventions:** follow `CONTRIBUTING.md` for branching, commits, file headers and PRs.

## Imports

<!-- Optional: @-import files Claude needs every session; each import loads in full at startup, so add sparingly -->

---

## References

- [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/) — source of the Core Principles above

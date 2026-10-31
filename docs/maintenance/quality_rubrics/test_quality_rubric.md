<!-- version: 1.0.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 🧪 Test Quality Rubric

For maintainers of this template: how to score the tests for each script out of 10, with a 10 meaning enough testing that stays easy to read, not the most tests.

---

## 🏷️ Themes

| Theme (Rubric) | Description/Purpose |
|---|---|
| 🎯 **Core coverage** | Every Must-level behaviour has a test |
| ⚖️ **Leanness** | No duplicate or cosmetic tests, and no more Could tests than Must tests |
| 📖 **Clarity** | A newcomer can tell what each test checks |
| 🧩 **Simplicity** | Short, plain pytest, and a harmless change breaks at most one test |
| 🧊 **Reliability** | Isolated, repeatable, and a failure says what broke |

## 🔢 Points

Each Theme (Rubric) scores 0, 1 or 2 points, and the five add up to the script's quality score out of 10.

| Points | Meaning | Example |
|---|---|---|
| **2** | Fully met | Every Must-level behaviour has a test |
| **1** | Partly met | One common path has no test |
| **0** | Not met | Several core behaviours have no test |

## 📏 How to score

- **Score the script, not each test:** look at all of a script's tests together.
- **Rare paths don't cost points:** an untested error that almost never happens isn't a Core coverage gap.
- **Simplicity:** a test body over about 12 lines costs a point, and so does mocking the script's internals.
- **Reliability:** a test should run in a temporary folder or repo, ignore the user's git config, and use assertion messages that say what broke.
- **Say why:** every score under 10 names its gaps in the audit's **Why not 10** column.

## 🛑 Avoiding over-testing

- **Lower scores don't mean add tests:** if a new test would cost Leanness or Simplicity points, don't add it, even if it covers a real path.
- **Removing tests can raise the score:** deleting a duplicate or cosmetic test improves Leanness.

## 📊 Where scores live

- **Audit:** `tests/test_coverage_audit.md` holds each script's points and quality score.
- **Checked by:** `tests/test_coverage_audit.py`, which fails if a point isn't 0–2 or a quality score isn't the sum of its points.

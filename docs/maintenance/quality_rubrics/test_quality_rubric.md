<!-- version: 2.0.1 -->
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
| 📖 **Clarity** | A newcomer can tell what each test checks, and non-obvious logic has a short comment |
| 🧩 **Simplicity** | Short tests in plain pytest, with no mocking of the script's internals |
| 🔧 **Maintainability** | A harmless change breaks at most one test, and names and docstrings describe current behaviour |
| 🧊 **Reliability** | Isolated, repeatable, and a failure says what broke |

## 🔢 Scores

Each Theme (Rubric) gets a symbol and a score out of 10, in fixed steps so different people score the same way.

| Symbol | Score | Meaning | Example |
|---|---|---|---|
| ✅ | **10** | Fully met | Every Must-level behaviour has a test |
| 🟡 | **5** | Partly met | One common path has no test |
| ❌ | **0** | Not met | Several core behaviours have no test |

- **Overall score:** the average of the six theme scores, to one decimal place, so it's also out of 10.
- **Grade:** A for 9 or more, B for 8 or more, C for 7 or more, D for 6 or more, and F below 6.
- **Example:** five ✅ and one 🟡 average 9.2, which is shown as **A · 9.2/10**.

## 📏 How to score

- **Score the script, not each test:** look at all of a script's tests together.
- **Rare paths don't cost points:** an untested error that almost never happens isn't a Core coverage gap.
- **Clarity:** parsing, regexes, ordering checks and unexplained inputs (such as answers fed to a prompt) need a one-line comment, while plain setup doesn't.
- **Simplicity:** a test body over about 12 lines costs points, and so does mocking the script's internals.
- **Maintainability:** the same message text asserted in two or more tests costs points, because rewording it breaks them all.
- **Reliability:** a test should run in a temporary folder or repo, ignore the user's git config, and use assertion messages that say what broke.
- **Gaps:** every theme below ✅ is named in the audit's **Gaps** column, starting with the theme's name.

## 🛑 Avoiding over-testing

- **Lower scores don't mean add tests:** if a new test would cost Leanness or Simplicity points, don't add it, even if it covers a real path.
- **Removing tests can raise the score:** deleting a duplicate or cosmetic test improves Leanness.

## 📊 Where scores live

- **Audit:** `tests/test_coverage_audit.md` holds each script's theme scores, overall score and gaps.
- **Checked by:** `tests/test_coverage_audit.py`, which fails if a symbol doesn't match its score, or an overall score or grade doesn't match the theme scores.

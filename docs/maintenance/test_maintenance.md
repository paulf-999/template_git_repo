<!-- version: 1.0.7 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 🧪 Test Maintenance

For maintainers of this template: how many tests to write, how to score them and when to delete them.

---

## 📋 Executive summary

- **Count functions, not cases:** one parametrised function can produce dozens of pytest cases, so size the suite by its test functions.
- **Score every test:** each test function carries a `# MoSCoW:` comment that says how much it matters.
- **Delete `Won't` tests:** a test that adds nothing new is removed rather than kept with a low score.
- **Review with the code:** a PR that changes a script also reviews that script's test scores.

## 🏷️ MoSCoW scores

| Score | Meaning | What happens if it breaks |
|---|---|---|
| **Must** | Guards a core contract of a hook or CI check | A bad commit, PR or file gets through, or a good one is blocked |
| **Should** | Main options, common edge cases and clear error messages | A common path misbehaves, but the core gate still works |
| **Could** | Rare edge cases and template helpers | Something unusual misbehaves |
| **Won't** | A duplicate of a lower-level test, or a cosmetic check | Nothing new, so the test is deleted |

- **Format:** put `# MoSCoW: <score> — <reason>` on the line above the test's decorators, or above `def` when it has none.
- **Reason:** keep it to about 12 words, and say what the test protects, not how it works.
- **Tests only:** score `test_` functions, not helpers or fixtures, which take their importance from the tests that use them.
- **Example:**

```python
# MoSCoW: Must — security: a PR title must never run as code
def test_title_with_shell_characters_is_not_executed():
```

## 📏 How many tests

- **Musts:** write one per contract of a script, covering the happy path, each failure that blocks and the limit boundary.
- **Lowest level once:** test a shared helper in `test_shell_utils.py`, and give each script that uses it one wiring test, not a copy of every edge case.
- **Parametrise:** cover input variants with parametrised cases instead of near-duplicate functions.
- **Bug fixes:** each fix adds one regression test, scored by the impact of the bug.
- **No new `Won't` tests:** if a test would score `Won't`, don't add it.

## 🍂 Keeping tests from going stale

A stale test checks or describes behaviour the code no longer has, so it still passes but protects nothing.

- **Same PR:** a change to a script updates that script's tests in the same PR, and deletes tests for behaviour it removes.
- **Rescore:** the same PR rechecks those tests' scores, since a change can turn a `Could` into a `Must`, or a test into a duplicate.
- **Names and docstrings:** describe what the code does now, never what is "new", "added" or "old", since that wording goes stale on the next change.

## 🔍 Periodic review

At each template release, count the tests by score:

```bash
grep -rh --include='*.py' '^# MoSCoW:' tests | awk '{print $3}' | sort | uniq -c
```

- **By script:** `docs/maintenance/quality_maintenance/quality_audit_tests.md` shows the same counts for each script, and `tests/test_quality_audit_tests.py` fails if it falls out of date.
- **Quality:** rescore each script out of 10 in the same audit, using `docs/maintenance/quality_maintenance/rubrics/test_quality_rubric.md`.
- **Cut:** delete `Could` tests that no longer earn their run time, and any test that now duplicates another.
- **Check:** every test function still has exactly one `# MoSCoW:` comment.

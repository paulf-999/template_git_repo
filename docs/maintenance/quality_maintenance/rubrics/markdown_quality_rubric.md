<!-- version: 1.0.2 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 📄 Markdown Quality Rubric

For maintainers of this template: how to score each markdown doc out of 10, with a 10 meaning a doc that's short, correct and easy to follow, not the longest one.

---

## 🏷️ Themes

| Theme (Rubric) | Description/Purpose |
|---|---|
| 🎯 **Core coverage** | Covers every task the reader comes for, and opens by saying who it's for |
| ⚖️ **Leanness** | Links to other docs instead of repeating them, and stays under about 100 lines |
| 📖 **Clarity** | A newcomer can follow it without outside context and get the gist from a skim, with jargon explained and any non-obvious step or rule saying why |
| 🔧 **Maintainability** | No lists that drift, points to the source instead, keeps no history, and covers one topic per file |
| ✅ **Accuracy** | Every command, path and link works and matches the repo today |

## 🔢 Scores

Scores work exactly as in [the test rubric's Scores section](test_quality_rubric.md#-scores): each Theme (Rubric) gets ✅ 2, 🟡 1 or ❌ 0 points, and the five add up to a graded score out of 10.

## 📏 How to score

- **Score each file on its own:** judge it against what its reader needs, not against other docs.
- **Clarity:** headings, bullets and tables should put the key point first, and a rule or step a newcomer might question, such as a naming limit or a required order, needs a short reason.
- **Leanness:** a doc over about 100 lines costs points unless it's split, and so does a section copied from another doc.
- **Maintainability:** a full file tree, a full list of options or a hard-coded count costs points, because each drifts as the repo changes.
- **Accuracy:** every path, command and link is checked against the repo as it is now.
- **Not scored:** the PR and issue templates, which are forms to fill in rather than docs to read.

## 🛑 Avoiding over-writing

- **Lower scores don't mean add text:** if a new section would cost Leanness or Clarity points, link to where the detail lives instead.
- **Cutting can raise the score:** removing a repeated or out-of-date section improves Leanness and Accuracy.

## 📊 Where scores live

- **Audit:** `docs/maintenance/quality_maintenance/audits/quality_audit_markdown_files.md` holds each doc's theme scores, overall score and gaps.
- **Checked by:** `tests/test_docs_quality_audit.py`, which fails if a tracked doc has no row, or a score or grade doesn't match its themes.

<!-- version: 1.0.0 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 🏷️ File Headers

For maintainers of this template: how the version header at the top of each file works.

---

Every file opens with a three-line header, as HTML comments in markdown and `#` comments elsewhere, placed after any shebang or YAML `---` line:

```markdown
<!-- version: 1.0.0 -->
<!-- created: 2026-10-30 -->
<!-- updated: 2026-10-30 -->
```

- **New file:** start at `version: 1.0.0`, with `created` and `updated` both set to today.
- **Every edit:** set `updated` to today and bump `version`, but never change `created`.
  - **MAJOR:** behaviour or guidance reversed or removed.
  - **MINOR:** behaviour or guidance added.
  - **PATCH:** wording, typo or formatting fix only.
- **Exempt:** the PR and issue templates, which are copied into every new PR or issue, and empty `.gitkeep` files.
- **Checked by:** `tests/test_file_metadata_headers.py`, which fails on a missing or malformed header.

<!-- version: 1.1.1 -->
<!-- created: 2026-10-31 -->
<!-- updated: 2026-10-31 -->
# 🏷️ File Headers

For maintainers of this repo: how the version header at the top of each file works, and how it's kept up to date automatically.

---

## 📄 Format

Every file opens with a three-line header, as HTML comments in markdown and `#` comments elsewhere, placed after any shebang or YAML `---` line:

```markdown
<!-- version: 1.0.0 -->
<!-- created: 2026-10-30 -->
<!-- updated: 2026-10-30 -->
```

## 📏 Rules

- **New file:** start at `version: 1.0.0`, with `created` and `updated` both set to today.
- **Every edit:** set `updated` to today and bump `version`, but never change `created`.
  - **MAJOR:** behaviour or guidance reversed or removed.
  - **MINOR:** behaviour or guidance added.
  - **PATCH:** wording, typo or formatting fix only.
- **Exempt:** the PR and issue templates, which are copied into every new PR or issue, and empty `.gitkeep` files.
- **Checked by:** `tests/test_file_metadata_headers.py`, which fails on a missing or malformed header.

## ⚙️ Automation

A check that runs on every commit keeps headers up to date, so most bumps happen without you doing anything.

| When you commit a file that… | The check… |
|---|---|
| Has changed since the last commit | Sets `updated` to today and raises PATCH by 1 |
| Has a version you already raised by hand | Keeps your version and only updates the date |
| Is new, has no header, or hasn't changed | Leaves it alone |
| Has no `updated` line, or a version like `1.0` | Stops the commit and says what to fix |

- **After a bump:** the commit stops so you can check the change, then re-add the file and commit again.
- **Where it lives:** `src/sh/bump_file_headers.sh`, run by the `bump_file_headers` hook in `.pre-commit-config.yaml`.

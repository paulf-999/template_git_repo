<!-- version: 1.0.4 -->
<!-- created: 2025-09-18 -->
<!-- updated: 2026-10-31 -->
# 🐍 Virtual Environment Setup

For anyone setting up this repo locally for the first time: how to create the Python virtualenv it needs.

Using a virtualenv keeps dependencies isolated and avoids conflicts with system Python packages.

---

## 1. Create a Virtual Environment

Run the following in the project root:

```bash
python3 -m venv .venv
```

Use the Python version CI uses, set by `python-version` in [`ci.yml`](../.github/workflows/ci.yml), so local results match CI.

This will create a hidden `.venv/` directory containing the environment.

---

## 2. Activate the Virtual Environment

* **Linux / macOS**

  ```bash
  source .venv/bin/activate
  ```

* **Windows (PowerShell)**

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

* **Windows (Command Prompt)**

  ```bat
  .venv\Scripts\activate.bat
  ```

Once activated, your shell prompt will typically show `(.venv)`.

---

## 3. Install Requirements

With the environment active, install the dependencies and the development tools (linters and tests):

```bash
pip install -r requirements.txt
```

Or run `make deps`, which also installs the pre-commit git hooks.

---

## 4. Deactivate the Environment

When finished, deactivate with:

```bash
deactivate
```

---

## 5. Clean Up

To remove the environment completely:

```bash
rm -rf .venv
```

---

## 🔍 Notes

* The `.venv/` folder is ignored via `.gitignore` and should not be committed.
* If you use multiple projects, each should have its own virtual environment.

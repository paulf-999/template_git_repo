<!-- version: 1.0.0 -->
<!-- created: 2025-09-18 -->
<!-- updated: 2026-10-30 -->
# 🐍 Virtual Environment Setup

Using a virtualenv keeps dependencies isolated and avoids conflicts with system Python packages.

---

## 1. Create a Virtual Environment

Run the following in the project root:

```bash
python3 -m venv .venv
```

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

With the environment active, install the dependencies and the development tools (linters, tests, git hooks):

```bash
pip install -r requirements-dev.txt
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

# 🛠 Development Guide

This guide outlines how to set up, build, and manage the project using `just`, `uv`, and Git. This project uses PowerShell for cross-platform support.

---

## 📦 Requirements

Ensure the following tools are installed:

- [Python](https://www.python.org/downloads/)
- [Uv](github.com/astral-sh/uv)
- [Just](https://github.com/casey/just)
- [Git](https://git-scm.com/downloads)

---

## 🚀 Getting Started

```bash
git clone https://github.com/Tempo-Organization/tempo-gui
cd tempo-gui
just setup
```

---

## ⚙️ Available Commands

### 🔧 Setup and Build

- `just setup`
  Setup virtual environment and install pre-commit hooks.

- `just build`
  Build the project for Windows using Flet.

- `just run`
  Run the app in Python form (development mode).

- `just run_exe`
  Run the Windows executable app.

- `just build_run_exe`
  Build and run the Windows executable.

- `just rebuild`
  Full clean and rebuild.

- `just rebuild_run_exe`
  Full clean, rebuild, and run the Windows executable.

- `just cleanup` or `just clean`
  Remove virtual environment and clean untracked files.

- `just refresh_deps`
  Refresh and upgrade project dependencies.

---

### 📋 Git Commands

- `just git_pull`
  Pull latest changes from remote.

- `just git_push`
  Push local changes to remote.

- `just switch_to_main_branch`
  Switch to `main` branch.

- `just switch_to_dev_branch`
  Switch to `dev` branch.

- `just merge_dev_into_main`
  Merge `dev` into `main` and push.

- `just git_add_files`
  Interactively add files by path.

- `just git_add_all`
  Add all changes to staging.

- `just git_reset`
  Reset Git staging area.

---

### 💾 Git Stash Management

- `just git_create_stash`
  Interactively create a stash with a path and comment.

- `just git_pop_stash`
  Interactively pop stash(es) by index.

---

### 🧪 Pre-commit

- `just pre_commit_auto_update`
  Update pre-commit hooks.

- `just pre_commit_check_all`
  Run pre-commit checks on all files.

---

### 📝 Commitizen

- `just cz_commit`
  Create a commit using Commitizen.

- `just cz_commit_retry`
  Retry previous Commitizen commit.

---

### 📘 MkDocs

- `just mkdocs_build`
  Build MkDocs site.

- `just mkdocs_serve`
  Serve MkDocs site locally.

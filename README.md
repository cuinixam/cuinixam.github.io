# My personal website

<p align="center">
  <a href="https://github.com/cuinixam/cuinixam.github.io/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/cuinixam/cuinixam.github.io/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/cuinixam/pypeline">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cuinixam/pypeline/refs/heads/main/assets/badge/v0.json" alt="pypeline">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>

---

This is my personal website at [maxiniuc.com](https://maxiniuc.com).

## How it's built

Two builders, one output directory:

- **Sphinx + ABlog** renders the blog (`build/docs/blogs/**`). That's all Sphinx does.
- **`jarvis landing`** (a small typer CLI in `src/jarvis/`) renders the landing page from JSON data files and copies the presentation / notebook directories into the build root.

The principle is "Sphinx for blogs only." Everything else is hand-crafted HTML/CSS/JS, generated from data files so there is exactly one source of truth per piece of content.

See [AGENTS.md](AGENTS.md) for the architecture in detail and the "where do I add X" table.

## Build

The project uses [pypeline](https://github.com/cuinixam/pypeline) to orchestrate the build. Install it once:

```shell
pipx install pypeline-runner
```

Then build everything (Sphinx blog + jarvis landing, into `build/docs/`):

```shell
pypeline run
```

VS Code tasks for the common commands live in `.vscode/tasks.json`.

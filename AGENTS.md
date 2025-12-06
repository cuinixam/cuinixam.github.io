# Copilot Instructions for cuinixam.github.io

This is a personal website/blog project built with Sphinx, hosted on GitHub Pages at [maxiniuc.com](https://maxiniuc.com).

## Architecture Overview

**Core Components:**
- `jarvis`: Python CLI tool for content generation (blogs, timelines)
- `docs/`: Sphinx documentation source (Markdown with MyST parser)
- `docs/presentations/`: Reveal.js slide decks built from Markdown (`slides.md` → `presentation.html`)
- `src/jarvis/notebooks/`: Marimo interactive notebooks exported as HTML to `docs/notebooks/`
- `build/docs/`: Generated static site (deployed to GitHub Pages)

**Build System:** Uses [pypeline](https://github.com/cuinixam/pypeline) orchestrator with UV package manager. The `pypeline.yaml` defines all build steps.

## Development Workflows

### Quick Start
```powershell
# Bootstrap project (creates venv with UV, runs all steps)
pypeline run

# Use the jarvis CLI via PowerShell wrapper
.\jarvis.ps1 --help

# Alternative: Use VS Code tasks for common operations
# - "run tests" (pytest)
# - "generate docs" (sphinx-build)
# - "autobuild docs" (sphinx-autobuild with live reload)
```

### Running Individual Steps
```powershell
pypeline run --step CreateVEnv --step PyTest  # Run specific steps
pypeline run --step BuildDocs --single        # Skip dependencies
```

### Documentation Development
- **Edit:** Modify `.md` files in `docs/`
- **Build:** `pypeline run --step BuildDocs --single` or use "generate docs" task
- **Preview:** Run "autobuild docs" task, opens live-reloading server at http://127.0.0.1:8000
- **View:** Open `build/docs/index.html` or use "open docs index.html" task

## Key Conventions

### Blog Posts
- Created via `jarvis blog --title "Post Title" --category tech --tags python,sphinx`
- Auto-generates file at `docs/blogs/<YEAR>/<title_snake_case>.md` with frontmatter
- Uses [ABlog](https://ablog.readthedocs.io/) Sphinx extension for blog functionality
- Post pattern: `blog_post_pattern = "blogs/*/*"` in `docs/conf.py`

### Timeline Feature
- Defined as JSON in `docs/timeline.json` with `TimelineEntry` objects (year, title, description)
- Converted to Sphinx grid-based Markdown via `jarvis timeline` command
- Uses custom CSS classes (`.timeline`, `.entry.left`, `.entry.right`) in `docs/_static/lessons.css`
- Outputs to `docs/timeline.md` with alternating left/right grid layout

### Presentations
- Source: `docs/presentations/<name>/slides.md` (Reveal.js Markdown)
- Output: `docs/presentations/<name>/presentation.html` (built externally, copied to `docs/`)
- Excluded from Sphinx processing via `exclude_patterns` but included in final output via `html_extra_path`
- Linked from `docs/presentations.md` using Sphinx Design grid cards

### Notebooks
- Source: `src/jarvis/notebooks/<name>.py` (Marimo Python apps)
- Export as HTML via: `marimo export html <name>.py -o docs/notebooks/<name>/index.html`
- Marimo notebooks are reactive Python notebooks with `marimo.App()` structure
- Excluded from mypy checking: `[[tool.mypy.overrides]]` for `jarvis.notebooks.*`

### Sphinx Configuration Patterns
- **Theme:** pydata-sphinx-theme with custom sidebar configs per page type
- **Extensions:** MyST Parser (Markdown), ABlog (blog), sphinx-design (grids/cards), sphinxcontrib-mermaid
- **Static paths:** Custom CSS in `docs/_static/` auto-added via `setup(app)` function
- **MyST features:** Colon fences, definition lists, HTML admonitions, inline attributes

## Testing & Quality

```powershell
pytest                              # Run tests
pre-commit run --all-files          # Linters, formatters (ruff, codespell, etc.)
```

## Python Environment

- **Package manager:** UV (not pip/poetry)
- **Python version:** >=3.10, <4.0
- **Dev dependencies:** All in `[dependency-groups.dev]` section
- **Editable install:** Via `setup.py` shim (required for GitHub package detection)
- **Entry point:** `jarvis.main:main()` via Typer CLI

## Common Pitfalls

1. **Don't run `pip install` directly** - use UV or `pypeline run --step CreateVEnv`
2. **Presentations/notebooks are pre-built** - HTML files are committed, not generated during Sphinx build
3. **PowerShell commands use `;` not `&&`** - e.g., `cd docs ; sphinx-build ...`
4. **Jarvis CLI from repo root** - use `.\jarvis.ps1` not `python -m jarvis` (requires special `_run.py` path setup)
5. **Timeline JSON must match dataclass** - Fields: year (int), title (str), description (str)

## File/Directory Purposes

- `jarvis.ps1`: PowerShell wrapper to run jarvis CLI with correct venv/paths
- `src/jarvis/_run.py`: Bootstrap script for running jarvis module from repo (adds `src/` to path)
- `setup.py`: Minimal shim for GitHub package detection (actual build uses UV)
- `pypeline.yaml`: Build orchestration config (steps: CreateVEnv, PreCommit, PyTest, BuildDocs)
- `docs/conf.py`: Sphinx configuration with ABlog, MyST, and custom sidebar layouts
- `build/CreateVEnv.deps.json`: Pypeline dependency tracking (auto-generated)

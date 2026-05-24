# Agent instructions for cuinixam.github.io

This is the personal website at [maxiniuc.com](https://maxiniuc.com), hosted on GitHub Pages.

## Architecture: one principle

**Sphinx is for BLOGS ONLY.** Every other page is hand-crafted HTML rendered by `jarvis`, a small typer CLI in `src/jarvis/`, from JSON data files. Static asset directories (presentations, notebooks) are copied into the build root by `jarvis` — not by Sphinx via `html_extra_path`.

The end state:

| URL | Written by |
|---|---|
| `index.html` (landing) | `jarvis landing` |
| `about.html`, future non-blog pages | `jarvis landing` (planned) |
| `blogs/**` (blog index + all posts) | Sphinx + ABlog |
| `<presentation_or_notebook>/**` (static HTML) | `jarvis landing` copies the dirs |

If something is going to be new, do not reach for a `.md` file. The only `.md` source files in this project belong inside `docs/blogs/`.

## Build pipeline

`pypeline run` walks the steps in `pypeline.yaml`:

1. **CreateVEnv** — uv-bootstrapped Python 3.13 venv
2. **PreCommit** — ruff, ruff-format, mypy, codespell, hooks
3. **PyTest** — tests
4. **BuildDocs** — `sphinx-build docs build/docs` (writes blog pages and a stub `index.html`)
5. **BuildLanding** — `jarvis landing …` (overwrites `index.html` with the real landing, copies static dirs)

Steps 4 and 5 both write into `build/docs/`; step 5 deliberately overwrites Sphinx's stub `index.html`.

## Where to add what

| Want to | Edit |
|---|---|
| New blog post | `jarvis blog --title "…" --category … --tags …` — creates `docs/blogs/<year>/<slug>.md` |
| New timeline entry | `docs/timeline.json` |
| New talk (slide deck) | `docs/presentations.json` `talks` array + drop the static dir under `docs/presentations/` |
| New demo (interactive HTML) | `docs/presentations.json` `demos` array + drop the static dir under `docs/presentations/` |
| New featured project (carousel) | `PROJECTS` list at the top of `src/jarvis/landing.py` |
| New notebook *(once teaching is migrated)* | `docs/teaching.json` + drop HTML under `docs/notebooks/` |
| Landing page styles | `src/jarvis/templates/landing/assets/landing.css` |
| Landing page layout / new sections | `src/jarvis/templates/landing/index.html.j2` |
| Blog page styles (palette overrides) | `docs/_static/filament.css` |

If a presentation/notebook directory exists under `docs/presentations/` or `docs/notebooks/` but is **not** listed in the corresponding JSON, it is still copied into the build (URL works) but is not surfaced on the landing. This is how internal/private content (e.g. `docs/presentations/objectives_2024/`, `docs/presentations/alex/`) is handled.

## Theme

One palette: **Filament**, a warm-yellow-on-dark theme adapted from monkeytype's serika_dark. Two stylesheets, one per surface:

- `src/jarvis/templates/landing/assets/landing.css` — full standalone styles for jarvis-rendered pages
- `docs/_static/filament.css` — pydata-sphinx-theme variable overrides for blog pages

## Migration status

The project is mid-migration toward the Sphinx-for-blogs-only model.

| Old (Sphinx) | New | Status |
|---|---|---|
| `docs/presentations.md` + `html_extra_path = ["presentations"]` | `docs/presentations.json` + jarvis-copied dirs + landing sections | ✅ Done |
| `docs/teaching.md` + `html_extra_path = ["notebooks"]` | `docs/teaching.json` + jarvis-copied dirs + landing section | ⏳ Pending |
| `docs/about.md` | jarvis-rendered `about.html` | ⏳ Pending |
| `docs/timeline.md` (generated from JSON) | merged into the about page | ⏳ Pending |
| `docs/index.md` (Sphinx tries to render an index doc) | minimal stub; `jarvis landing` overwrites the output | ⏳ Pending |

## Common commands

```bash
pypeline run                                          # full build
jarvis landing --help                                 # see flags
jarvis blog --title "Hello" --category tech           # scaffold a new post
pre-commit run --all-files                            # lint/format manually
sphinx-autobuild docs build/docs                      # blog-only live reload
```

## Conventions to NOT break

- **No new `.md` files outside `docs/blogs/`.** Anything new is a JSON data file consumed by `jarvis landing`.
- **No Sphinx extensions to solve landing-page problems.** The landing is plain HTML/CSS/JS rendered from a Jinja template; nothing fancier should creep in.
- **No content duplication.** If something appears on the landing AND on a Sphinx page, the JSON is the single source of truth — never edit two files.
- **No reaching into `docs/_templates/hello.html` or `docs/about.md` text without the user's per-line permission.** That copy is the user's voice; visuals can change, words cannot. See [the personal-voice rule](https://github.com/cuinixam/cuinixam.github.io/blob/main/AGENTS.md#personal-voice-rule) below.

## Personal-voice rule

Treat as sacred (do not edit without explicit per-line approval):

- The homepage tagline `I'm not just another engineer.`
- The `focusareas` and `whatido` blocks in `docs/_templates/hello.html`
- All About-page prose
- Section labels with personality (including emojis in titles like `🛠 Working Experience`, `💡 SPL Mindmap`, `🔎 Objects Dependencies Graph`)

A redesign request is about visuals (CSS, layout, theme) — never a license to rewrite the user's words.

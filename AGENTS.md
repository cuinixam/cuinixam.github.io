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
| `about.html` | `jarvis about` (prose from `docs/about.md`, timeline from `docs/timeline.json`) |
| `<presentation_or_notebook>/**` (static HTML) | `jarvis landing` copies the dirs |

If something is going to be new, do not reach for a `.md` file. The only `.md` source files in this project belong inside `docs/blogs/`, plus `docs/about.md` as the prose source for the about page.

## Build pipeline

`pypeline run` walks the steps in `pypeline.yaml`:

1. **CreateVEnv** — uv-bootstrapped Python 3.13 venv
2. **PreCommit** — ruff, ruff-format, mypy, codespell, hooks
3. **PyTest** — tests
4. **BuildDocs** — `sphinx-build docs build/docs` (writes blog pages and a stub `index.html`)
5. **BuildLanding** — `jarvis landing …` (overwrites `index.html` with the real landing, copies presentation + notebook dirs)
6. **BuildAbout** — `jarvis about …` (writes `about.html` from `docs/about.md` + `docs/timeline.json`)

Steps 4–6 all write into `build/docs/`; step 5 deliberately overwrites Sphinx's stub `index.html`.

## Where to add what

| Want to | Edit |
|---|---|
| New blog post | `jarvis blog --title "…" --category … --tags …` — creates `docs/blogs/<year>/<slug>.md`. Appears on the landing's writing section automatically if it's in the 4 most recent. |
| New timeline entry | `docs/timeline.json` |
| New talk (slide deck) | `docs/presentations.json` `talks` array + drop the static dir under `docs/presentations/` |
| New demo (interactive HTML) | `docs/presentations.json` `demos` array + drop the static dir under `docs/presentations/` |
| New featured project (carousel) | `PROJECTS` list at the top of `src/jarvis/landing.py` |
| New notebook | `docs/teaching.json` + drop HTML under `docs/notebooks/` |
| Landing page styles | `src/jarvis/templates/landing/assets/landing.css` (shared by landing + about) |
| Landing page layout / new sections | `src/jarvis/templates/landing/index.html.j2` |
| About-page bio prose | `docs/about.md` (everything up to the first H2 — first H2 onward is ignored) |
| About-page layout | `src/jarvis/templates/about/index.html.j2` |
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
| `docs/teaching.md` + `html_extra_path = ["notebooks"]` | `docs/teaching.json` + jarvis-copied dirs + landing section | ✅ Done |
| `docs/about.md` (Sphinx renders) | jarvis-rendered `about.html` (about.md is now prose source only; `exclude_patterns` keeps Sphinx out) | ✅ Done |
| `docs/timeline.md` (generated from JSON) | deleted; timeline content lives only in `about.html`, rendered by jarvis from `timeline.json` | ✅ Done |
| `docs/index.md` (Sphinx tries to render an index doc) | reduced to minimal master_doc stub; `jarvis landing` overwrites the output | ✅ Done |

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
- **No reaching into `docs/about.md` text without the user's per-line permission.** That copy is the user's voice; visuals can change, words cannot. See [the personal-voice rule](https://github.com/cuinixam/cuinixam.github.io/blob/main/AGENTS.md#personal-voice-rule) below.

## Personal-voice rule

Treat as sacred (do not edit without explicit per-line approval):

- The homepage tagline `I'm not just another engineer.` (in the landing template)
- All About-page prose (`docs/about.md` and the inlined landing `#about` paragraphs)
- Section/sub-section H2s like `Selected talks.`, `Interactive demos.`, `Notebooks for learning.`, `Recent writing.`, `Some things I am working on.`
- Section labels with personality (including emojis in titles like `🛠 Working Experience`, `💡 SPL Mindmap`, `🔎 Objects Dependencies Graph`)

A redesign request is about visuals (CSS, layout, theme) — never a license to rewrite the user's words.

# Website redesign — in-flight notes

Working doc to pick up the redesign later. Architecture lives in [AGENTS.md](AGENTS.md); this file captures the *in-progress* state and parked decisions.

Last touched: 2026-05-24.

## The vision (one paragraph)

The site is migrating from "Sphinx renders everything" to "Sphinx renders blogs only; jarvis renders everything else from JSON data files." The landing page is a hand-crafted single-page experience (hero → projects carousel → talks → demos → writing → about, all as in-page anchors). The Filament theme — warm yellow on dark, adapted from monkeytype's serika_dark — unifies both surfaces.

## What's done

- **Filament theme** applied to both surfaces (blog pages + landing):
  - `docs/_static/filament.css` (pydata-sphinx-theme variable overrides for blog pages)
  - `src/jarvis/templates/landing/assets/landing.css` (full standalone styles for landing)
  - Pygments dark style: `gruvbox-dark`
  - Single palette, theme switcher hidden, dark forced

- **Blog page sidebar cleanup** (in `docs/conf.py`):
  - Blogs index left sidebar: `categories` only (was: categories + tagcloud + archives)
  - Blog post left sidebar: `recentposts` only (was: postcard + recentposts + archives)
  - Right page-TOC sidebar: hidden everywhere except `blogs/**`

- **Jarvis landing pipeline**
  - `src/jarvis/landing.py` (`LandingWriter`, `PROJECTS` list, `render_md_inline` filter)
  - `src/jarvis/templates/landing/index.html.j2` (Jinja template)
  - `src/jarvis/templates/landing/assets/landing.css`
  - `jarvis landing` typer command in `src/jarvis/main.py`
  - `BuildLanding` step in `pypeline.yaml` after `BuildDocs`
  - `pyproject.toml`: added `[build-system]` (hatchling), `jinja2`, `markdown` deps; `types-Markdown` dev dep + in mypy pre-commit additional_dependencies

- **Presentations migration (full)** — the pattern for everything else
  - `docs/presentations.md` deleted
  - `docs/presentations.json` (structure: `{ "talks": [...], "demos": [...] }`)
  - `src/jarvis/presentations.py` (Presentation + Presentations dataclasses, mashumaro/JSON)
  - `jarvis landing` now also copies every subdir of `docs/presentations/` into the build root (took over Sphinx `html_extra_path` for these)
  - Landing renders **3 talks** + **3 demos** in two grids
  - "Not on landing but URL works": `objectives_2024/`, `alex/erdkunde_8e/`, `objects_deps_hello_world_zephyr/` (still copied, just not in JSON)
  - `conf.py`: presentations removed from `html_sidebars`, `secondary_sidebar_items`, `html_extra_path`
  - `docs/index.md` toctree: removed `presentations` entry

- **AGENTS.md + README.md rewrite** — current architecture + where-to-add-what table + personal-voice rule

## In flight (current design discussion, not yet implemented)

Agreed in chat but not yet coded — the new landing layout:

- **Menu items are in-page anchors only.** No external links in the nav.
- **Menu structure**: `projects · talks · demos · writing · about` (drop `github` and `timeline`)
- **Writing section (new on landing)**: 3-5 most recent blog posts (date · title · category), with "all posts ↗" top-right linking to `blogs.html`
- **About section on landing**: 1-2 sentence overview, "more about me ↗" top-right linking to the about page
- **Timeline moves OFF the landing INTO the about page** (no longer a landing section)
- **General principle**: landing = overview for every section; separate page if depth is needed
- **Teaching**: confirmed name = "Teaching" (not "Learning")

## What's next (ordered)

1. **Teaching migration** (mirror of presentations)
   - Delete `docs/teaching.md`
   - `docs/teaching.json` (single list of notebooks)
   - jarvis copies `docs/notebooks/<dir>/` into the build root
   - Remove `notebooks` from `html_extra_path`
   - Landing "Teaching" section + menu item
   - Add menu item between `demos` and `writing` (or wherever fits visually)

2. **Landing layout changes** (from the design discussion above)
   - Update nav: drop `github`, `timeline`; add `writing`, `about`
   - Add writing section to template (needs blog-frontmatter scanner — see open decision)
   - Move timeline section out of landing template
   - Update about section: short overview + "more about me ↗"

3. **About page migration**
   - First step: add timeline content to about.md (either via `{include} timeline.md` directive or by inlining)
   - Eventually: migrate `about.md` itself to a jarvis-rendered `about.html`

4. **Final cleanup toward "Sphinx for blogs only"**
   - `docs/index.md` → minimal stub (Sphinx needs a master_doc; jarvis overwrites the rendered output anyway)
   - Eliminate `docs/_templates/hello.html` if no longer referenced
   - Eliminate `docs/timeline.md` and `jarvis timeline` (timeline data goes straight from JSON into the about page)
   - `html_sidebars` in conf.py: only `blogs` / `blogs/**` keys

## Open decisions (need user input before action)

- **Timeline placement on the about page**: include directive vs inline into about.md
- **Writing data source**: scan `docs/blogs/**/*.md` frontmatter at landing build time *(recommended)* vs maintain a `docs/writing.json`
- **`objects_deps_hello_world_zephyr/`**: surface as a 4th demo? Need a one-line description in user's voice — not invented
- **`alex/` and `objectives_2024/`**: confirmed copy-but-don't-list. Keep as-is.

## Key files reference

| Purpose | File |
|---|---|
| Architecture & conventions | `AGENTS.md` |
| Build orchestration | `pypeline.yaml` |
| Sphinx config (blogs only direction) | `docs/conf.py` |
| Landing entry point | `src/jarvis/landing.py` |
| Landing template | `src/jarvis/templates/landing/index.html.j2` |
| Landing styles | `src/jarvis/templates/landing/assets/landing.css` |
| Blog-page palette overrides | `docs/_static/filament.css` |
| Timeline data | `docs/timeline.json` |
| Presentations data (talks + demos) | `docs/presentations.json` |
| Featured projects (carousel) | `PROJECTS` list at top of `src/jarvis/landing.py` |
| Personal-voice rule (DO NOT touch) | `AGENTS.md` § Personal-voice rule |

## Known issues (pre-existing, not redesign-induced)

- Two files named literally `*.md.md` (`spl_bootstrap.md.md`, `what_you_did_not_want_to_know_about_your_code.md.md`) — heading-level warnings
- `docs/blogs/2026/smarty_p1.md:85` uses Pygments lexer `txt` (should be `text` or `plain`)
- `docs/timeline.json` YANGA entry (year 2023) description ends with `[here](#presentations)` — the `presentations` doc was deleted, so this xref fails on build (2 warnings). User's voice; awaiting decision on repoint vs drop.

## Resume signal

When picking this up, the most likely next step is **teaching migration** (#1 above) — it's the same shape as presentations, just one more JSON file + one more landing section + a few `html_extra_path` / sidebar removals. Should take 10 minutes of edits + one pypeline run.

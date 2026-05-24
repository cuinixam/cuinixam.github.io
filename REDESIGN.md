# Website redesign — in-flight notes

Working doc to pick up the redesign later. Architecture lives in [AGENTS.md](AGENTS.md); this file captures the *in-progress* state and parked decisions.

Last touched: 2026-05-24 (about-page migration complete).

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

- **Teaching migration (full)** — same shape as presentations
  - `docs/teaching.md` deleted
  - `docs/teaching.json` (structure: `{ "notebooks": [...] }`)
  - `src/jarvis/teaching.py` (Notebook + Teaching dataclasses)
  - `jarvis landing` copies every subdir of `docs/notebooks/` into the build root via a generalised `_copy_subdirs` helper (same call now used for both `presentations/` and `notebooks/`)
  - Landing renders the 3 notebooks in a single grid (section id `#teaching`, between `#demos` and `#about`)
  - `conf.py`: teaching removed from `html_sidebars` + `secondary_sidebar_items`; `html_extra_path` is now `[]`
  - `docs/index.md`: removed `teaching.html` card + toctree entry

- **About-page migration (full)** — last big content surface off Sphinx
  - `docs/about.md` kept as **prose source only** (not deleted — user's bio lives here, untouched). Trailing `## A rough timeline` + `{include} timeline.md` section removed (now redundant: jarvis pulls timeline straight from JSON).
  - `src/jarvis/about.py` — `parse_about_md` (extracts H1 + paragraphs, stops at first H2), `AboutWriter`
  - `src/jarvis/templates/about/index.html.j2` — story-flow layout: slim nav → `// about` eyebrow + hero title → narrow bio prose column (max-width 720px) → timeline grid (same component the landing used to have) → footer
  - `src/jarvis/_md.py` extracted from landing.py so `render_md_inline` is shared by both writers (no circular-import risk)
  - `jarvis about --about-md-file docs/about.md --timeline-file docs/timeline.json --output-dir build/docs` — new typer command
  - `pypeline.yaml`: added `BuildAbout` step after `BuildLanding`
  - `conf.py`: `about.md` added to `exclude_patterns`; `about` dropped from `html_sidebars` and `secondary_sidebar_items`
  - `docs/index.md`: `about` removed from toctree (the dead-UI card stays, since `about.html` exists)
  - Timeline section **removed from the landing** (`#timeline` section, nav item, IntersectionObserver JS, and `timeline_file` argument to `LandingWriter` all gone)
  - Landing `#about` block restyled: `section-head` + `<h2>About me.</h2>` + two right-aligned `↗` links (`full about` → `about.html`, `timeline` → `about.html#timeline`); user's two summary paragraphs preserved verbatim
  - Landing nav: dropped `timeline`, added `about` (`#about` anchor → summary block); final order: `projects · writing · talks · demos · teaching · about · github`
  - New CSS in shared `landing.css`: `.about-hero`, `.bio`, `.bio-prose`, `.section-head .see-all-group`, `.about-page nav .brand` hover

- **AGENTS.md + README.md rewrite** — current architecture + where-to-add-what table + personal-voice rule

## In flight (current design discussion, not yet implemented)

Remaining from the design discussion:

- **Menu items are in-page anchors only.** No external links in the nav. *(Still pending: `github` is still in the nav as an external link.)*
- **Menu structure**: `projects · talks · demos · writing · about` (drop `github`; order writing after demos)  *(Current order is `projects · writing · talks · demos · teaching · about · github` — close, but `writing` is still before talks and `github` still present.)*
- **Writing section (new on landing)**: 3-5 most recent blog posts (date · title · category), with "all posts ↗" top-right linking to `blogs.html` *(Not yet implemented — needs the writing data-source decision below.)*
- **General principle**: landing = overview for every section; separate page if depth is needed
- **Teaching**: confirmed name = "Teaching" (not "Learning") ✅

Resolved by the about-page migration:

- ✅ **About section on landing**: short overview + `↗` link(s) to the about page (we shipped two: `full about` + `timeline`)
- ✅ **Timeline moves OFF the landing INTO the about page**

## What's next (ordered)

1. **Writing section on the landing** (the last big design-discussion item)
   - Add `writing` section between `#demos` and `#teaching` (or wherever fits final nav order)
   - 3–5 most recent blog posts, `date · title · category`, with `all posts ↗` linking to `blogs.html`
   - Needs the writing-data-source decision (frontmatter scan vs `writing.json`)

2. **Nav cleanup**
   - Drop `github` from the nav (still reachable via footer + brand)
   - Reorder to the agreed final: `projects · talks · demos · writing · about`
   - `teaching` doesn't appear in the doc's target list — confirm with user whether to keep it in nav or fold into a different section

3. **Final cleanup toward "Sphinx for blogs only"**
   - `docs/index.md` → minimal stub (Sphinx needs a master_doc; jarvis overwrites the rendered output anyway)
   - Eliminate `docs/timeline.md` and `jarvis timeline` (timeline now goes JSON → about page directly; standalone `timeline.html` is orphaned)
   - Eliminate `docs/_templates/hello.html` if no longer referenced
   - `html_sidebars` in conf.py: only `blogs` / `blogs/**` keys

## Open decisions (need user input before action)

- ✅ **Timeline placement on the about page**: resolved — jarvis pulls timeline straight from `timeline.json` into the about template; no markdown include.
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
| Teaching data (notebooks) | `docs/teaching.json` |
| Featured projects (carousel) | `PROJECTS` list at top of `src/jarvis/landing.py` |
| About-page bio prose | `docs/about.md` (everything before the first H2) |
| About-page layout | `src/jarvis/templates/about/index.html.j2` |
| Shared markdown helper | `src/jarvis/_md.py` (used by landing + about) |
| Personal-voice rule (DO NOT touch) | `AGENTS.md` § Personal-voice rule |

## Known issues (pre-existing, not redesign-induced)

- Two files named literally `*.md.md` (`spl_bootstrap.md.md`, `what_you_did_not_want_to_know_about_your_code.md.md`) — heading-level warnings
- `docs/blogs/2026/smarty_p1.md:85` uses Pygments lexer `txt` (should be `text` or `plain`)
- `docs/timeline.json` YANGA entry (year 2023) description ends with `[here](#presentations)` — the `presentations` doc was deleted, so this xref fails on build (2 warnings). User's voice; awaiting decision on repoint vs drop.

## Resume signal

About-page migration shipped and verified locally (build is green, both surfaces render). The next concrete content move is the **writing section on the landing** (#1 above) — but it's blocked on the writing-data-source decision (frontmatter scan vs `writing.json`). Either resolve that and code the section, or do the smaller nav cleanup (#2: drop `github`, reorder) which has no blockers.

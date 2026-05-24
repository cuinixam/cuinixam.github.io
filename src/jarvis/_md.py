"""Small markdown helpers shared by the jarvis page writers."""

import re

import markdown as md
from markupsafe import Markup

_WRAPPING_P = re.compile(r"^<p>(.*)</p>$", re.DOTALL)


def render_md_inline(text: str) -> Markup:
    """Render inline markdown, stripping the wrapping <p> tag for single-paragraph input."""
    html = md.markdown(text).strip()
    m = _WRAPPING_P.match(html)
    if m:
        html = m.group(1)
    # Inputs come from project-owned JSON files (timeline, presentations, teaching) — no XSS risk.
    return Markup(html)  # noqa: S704

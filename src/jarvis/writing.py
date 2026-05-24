"""Scan blog post frontmatter to surface recent writing on the landing page."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass
class WritingEntry:
    title: str
    date: date
    category: str
    url: str  # relative to the landing (e.g. blogs/2026/smarty_p2.html)

    @property
    def date_label(self) -> str:
        return self.date.isoformat()


def _parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def scan_blogs(blogs_dir: Path, limit: int = 4) -> list[WritingEntry]:
    """Return the most recent ``limit`` blog posts, newest first.

    Skips files whose frontmatter is missing the required ``date``, ``title``, or ``category`` keys.
    """
    entries: list[WritingEntry] = []
    for md_path in blogs_dir.rglob("*.md"):
        # Skip stray `.md.md` files and any non-post files at the blog index level.
        if md_path.name.endswith(".md.md"):
            continue
        fm = _parse_frontmatter(md_path.read_text())
        if not all(k in fm for k in ("date", "title", "category")):
            continue
        try:
            post_date = date.fromisoformat(fm["date"])
        except ValueError:
            continue
        # blogs_dir is docs/blogs; relative URL on the landing is "blogs/<year>/<slug>.html".
        rel = md_path.relative_to(blogs_dir.parent).with_suffix(".html")
        entries.append(
            WritingEntry(
                title=fm["title"],
                date=post_date,
                category=fm["category"],
                url=rel.as_posix(),
            )
        )
    entries.sort(key=lambda e: e.date, reverse=True)
    return entries[:limit]

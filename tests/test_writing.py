from datetime import date
from pathlib import Path

from jarvis.writing import _parse_frontmatter, scan_blogs


def test_parse_frontmatter_extracts_keys() -> None:
    text = "---\ntitle: Hello\ndate: 2026-01-01\ncategory: learning\n---\n\nBody.\n"
    assert _parse_frontmatter(text) == {
        "title": "Hello",
        "date": "2026-01-01",
        "category": "learning",
    }


def test_parse_frontmatter_returns_empty_when_no_block() -> None:
    assert _parse_frontmatter("no frontmatter here\n") == {}


def test_scan_blogs_sorts_newest_first_and_builds_url(tmp_path: Path) -> None:
    blogs = tmp_path / "blogs"
    (blogs / "2024").mkdir(parents=True)
    (blogs / "2024" / "old.md").write_text("---\ntitle: Old\ndate: 2024-01-01\ncategory: learning\n---\n")
    (blogs / "2024" / "new.md").write_text("---\ntitle: New\ndate: 2024-12-31\ncategory: review\n---\n")

    entries = scan_blogs(blogs)

    assert [e.title for e in entries] == ["New", "Old"]
    assert entries[0].date == date(2024, 12, 31)
    assert entries[0].url == "blogs/2024/new.html"
    assert entries[0].category == "review"


def test_scan_blogs_skips_posts_with_invalid_or_missing_fields(tmp_path: Path) -> None:
    blogs = tmp_path / "blogs"
    (blogs / "2024").mkdir(parents=True)
    (blogs / "2024" / "ok.md").write_text("---\ntitle: OK\ndate: 2024-06-01\ncategory: learning\n---\n")
    (blogs / "2024" / "no_date.md").write_text("---\ntitle: NoDate\ncategory: learning\n---\n")
    (blogs / "2024" / "bad_date.md").write_text("---\ntitle: Bad\ndate: not-a-date\ncategory: learning\n---\n")

    assert [e.title for e in scan_blogs(blogs)] == ["OK"]


def test_scan_blogs_respects_limit(tmp_path: Path) -> None:
    blogs = tmp_path / "blogs"
    (blogs / "2024").mkdir(parents=True)
    for i in range(6):
        (blogs / "2024" / f"post{i}.md").write_text(f"---\ntitle: Post {i}\ndate: 2024-0{i + 1}-01\ncategory: learning\n---\n")

    assert len(scan_blogs(blogs, limit=3)) == 3

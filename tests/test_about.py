from jarvis.about import parse_about_md


def test_extracts_h1_title() -> None:
    assert parse_about_md("# About me\n\nFirst.\n").title == "About me"


def test_renders_paragraphs_as_html() -> None:
    text = "# About me\n\nFirst paragraph.\n\nSecond paragraph.\n"
    body = parse_about_md(text).body_html
    assert "<p>First paragraph.</p>" in body
    assert "<p>Second paragraph.</p>" in body


def test_stops_at_first_h2() -> None:
    text = "# About me\n\nKept.\n\n## A rough timeline\n\nDropped.\n"
    body = parse_about_md(text).body_html
    assert "Kept." in body
    assert "Dropped." not in body
    assert "rough timeline" not in body

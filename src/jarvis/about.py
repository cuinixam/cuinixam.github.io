"""Generate the standalone HTML about page from docs/about.md + timeline.json."""

from dataclasses import dataclass
from pathlib import Path

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from jarvis._md import render_md_inline
from jarvis.timeline import Timeline


@dataclass
class About:
    title: str
    body_html: Markup


def parse_about_md(text: str) -> About:
    """
    Extract the H1 title and bio paragraphs, dropping anything from the first H2 onward.

    The first H2 in about.md is "A rough timeline" — its content is now rendered from
    timeline.json by the template, so the markdown source's timeline-include block is ignored.
    """
    lines = text.splitlines()
    title = ""
    body_lines: list[str] = []
    in_body = False
    for line in lines:
        stripped = line.strip()
        if not in_body:
            if stripped.startswith("# "):
                title = stripped[2:].strip()
                in_body = True
            continue
        if stripped.startswith("## "):
            break
        body_lines.append(line)
    body_md = "\n".join(body_lines).strip()
    # about.md is project-owned content — no XSS risk.
    body_html = Markup(md.markdown(body_md))  # noqa: S704
    return About(title=title, body_html=body_html)


class AboutWriter:
    def __init__(
        self,
        about_md_file: Path,
        timeline_file: Path,
        output_dir: Path,
        templates_dir: Path | None = None,
    ) -> None:
        self.about_md_file = about_md_file
        self.timeline_file = timeline_file
        self.output_dir = output_dir
        self.templates_dir = templates_dir or Path(__file__).parent / "templates" / "about"

    def write(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        about = parse_about_md(self.about_md_file.read_text())
        timeline = Timeline.from_json_file(self.timeline_file)

        env = Environment(
            loader=FileSystemLoader([str(self.templates_dir), str(self.templates_dir.parent)]),
            autoescape=select_autoescape(["html"]),
        )
        env.filters["md"] = render_md_inline

        tmpl = env.get_template("index.html.j2")
        html = tmpl.render(
            title=about.title,
            body_html=about.body_html,
            timeline_entries=timeline.entries,
        )
        (self.output_dir / "about.html").write_text(html)

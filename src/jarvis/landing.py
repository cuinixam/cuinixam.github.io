"""Generate the standalone HTML landing page that overrides Sphinx's index."""

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import markdown as md
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

from jarvis.presentations import Presentations
from jarvis.teaching import Teaching
from jarvis.timeline import Timeline


@dataclass
class Project:
    name: str
    year_range: str
    subtitle: str
    description: str
    github_url: str
    code_title: str
    code_html: str  # pre-rendered HTML; spans use kw|str|com|ac|ok classes

    @property
    def github_label(self) -> str:
        return self.github_url.replace("https://", "")


PROJECTS: list[Project] = [
    Project(
        name="yanga",
        year_range="2023 — present",
        subtitle="Yet Another Ninja Generator",
        description="Teaming up with AI to develop a Python application for software product line engineering.",
        github_url="https://github.com/cuinixam/yanga",
        code_title="~/spl-build $",
        code_html=(
            '<span class="ac">$ yanga build --variant chassis-premium</span>\n\n'
            '<span class="com"># resolving features…</span>\n'
            '  <span class="ok">✓</span> brake_ctrl\n'
            '  <span class="ok">✓</span> power_mgr\n'
            '  <span class="ok">✓</span> telemetry\n'
            '  <span class="ok">✓</span> diagnostics\n\n'
            '<span class="com"># compiling components…</span>\n'
            '  <span class="ok">✓</span> 47 source files\n'
            '  <span class="ok">✓</span> 12 component tests\n'
            '  <span class="ok">✓</span> integration suite\n\n'
            '<span class="ac">Build succeeded in 12.4s</span>\n'
            "artifacts: build/chassis_premium/"
        ),
    ),
    Project(
        name="pypeline",
        year_range="2024 — present",
        subtitle="Define once, run anywhere",
        description="Define your pipeline once in YAML and run it consistently across local environments and any CI/CD platform.",
        github_url="https://github.com/cuinixam/pypeline",
        code_title="pypeline.yaml",
        code_html=(
            '<span class="kw">pipeline</span>:\n'
            '  - <span class="kw">step</span>: CreateVEnv\n'
            '    <span class="kw">module</span>: pypeline.steps.venv\n\n'
            '  - <span class="kw">step</span>: PreCommit\n'
            '    <span class="kw">module</span>: pypeline.steps.precommit\n\n'
            '  - <span class="kw">step</span>: PyTest\n'
            '    <span class="kw">module</span>: pypeline.steps.pytest\n\n'
            '  - <span class="kw">step</span>: BuildDocs\n'
            '    <span class="kw">module</span>: pypeline.steps.sphinx\n'
            '    <span class="kw">config</span>:\n'
            '      source: <span class="str">"docs"</span>\n'
            '      output: <span class="str">"build/docs"</span>\n\n'
            '<span class="com"># $ pypeline run</span>\n'
            '<span class="com"># → identical results, every machine.</span>'
        ),
    ),
    Project(
        name="spl-core",
        year_range="2022 — present",
        subtitle="CMake for software product lines",
        description="My first CMake project to support engineering Software Product Lines. The shared foundation underneath every variant a team ships.",
        github_url="https://github.com/avengineers/spl-core",
        code_title="CMakeLists.txt",
        code_html=(
            '<span class="ac">include</span>(spl)\n\n'
            '<span class="ac">spl_add_component</span>(brake_ctrl\n'
            '  <span class="kw">SOURCES</span>\n'
            "    src/brake_ctrl.c\n"
            "    src/brake_state.c\n"
            '  <span class="kw">TESTS</span>\n'
            "    test/brake_ctrl_test.cc)\n\n"
            '<span class="ac">spl_add_component</span>(power_mgr\n'
            '  <span class="kw">SOURCES</span> src/power_mgr.c\n'
            '  <span class="kw">DEPENDS</span> brake_ctrl)\n\n'
            '<span class="com"># Variants pick which components to include.</span>\n'
            '<span class="com"># Core handles toolchain, tests, reports.</span>'
        ),
    ),
    Project(
        name="SPLed",
        year_range="training",
        subtitle="An SPL you can hold in your head",
        description=(
            "A simple software product line for controlling an LED with different variants — Disco, Sleep, Spa. "
            "The training repo we use to teach SPLE without anyone drowning in real-product complexity."
        ),
        github_url="https://github.com/avengineers/SPLed",
        code_title="variants/",
        code_html=(
            '<span class="com"># Three variants. One source tree.</span>\n\n'
            '<span class="ac">disco/</span>      LED blinks · adjustable frequency\n'
            '<span class="ac">sleep/</span>      Constant color · adjustable brightness\n'
            '<span class="ac">spa/</span>        Brightness pulsates · color cycles\n\n'
            '<span class="com"># Same components, different feature sets.</span>\n'
            '<span class="com"># Build any variant standalone:</span>\n\n'
            '<span class="ac">$ yanga build --variant disco</span>\n'
            '<span class="ac">$ yanga build --variant sleep</span>\n'
            '<span class="ac">$ yanga build --variant spa</span>\n\n'
            '<span class="ok">→</span> three products. one codebase.\n'
            '<span class="ok">→</span> the smallest SPL that\'s still real.'
        ),
    ),
]


_WRAPPING_P = re.compile(r"^<p>(.*)</p>$", re.DOTALL)


def render_md_inline(text: str) -> Markup:
    """Render inline markdown, stripping the wrapping <p> tag for single-paragraph input."""
    html = md.markdown(text).strip()
    m = _WRAPPING_P.match(html)
    if m:
        html = m.group(1)
    # Input comes from timeline.json (project-owned), not from any external source — no XSS risk.
    return Markup(html)  # noqa: S704


class LandingWriter:
    def __init__(
        self,
        timeline_file: Path,
        presentations_file: Path,
        presentations_dir: Path,
        teaching_file: Path,
        notebooks_dir: Path,
        output_dir: Path,
        templates_dir: Path | None = None,
    ) -> None:
        self.timeline_file = timeline_file
        self.presentations_file = presentations_file
        self.presentations_dir = presentations_dir
        self.teaching_file = teaching_file
        self.notebooks_dir = notebooks_dir
        self.output_dir = output_dir
        self.templates_dir = templates_dir or Path(__file__).parent / "templates" / "landing"

    def write(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        timeline = Timeline.from_json_file(self.timeline_file)
        presentations = Presentations.from_json_file(self.presentations_file)
        teaching = Teaching.from_json_file(self.teaching_file)
        env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html"]),
        )
        env.filters["md"] = render_md_inline

        tmpl = env.get_template("index.html.j2")
        html = tmpl.render(
            projects=PROJECTS,
            timeline_entries=timeline.entries,
            talks=presentations.talks,
            demos=presentations.demos,
            notebooks=teaching.notebooks,
        )
        (self.output_dir / "index.html").write_text(html)

        assets_src = self.templates_dir / "assets"
        if assets_src.exists():
            assets_dst = self.output_dir / "_landing"
            if assets_dst.exists():
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)

        self._copy_subdirs(self.presentations_dir)
        self._copy_subdirs(self.notebooks_dir)

    def _copy_subdirs(self, src_dir: Path) -> None:
        """Copy each subdirectory of src_dir into output_dir (mirrors Sphinx html_extra_path behavior)."""
        if not src_dir.exists():
            return
        for item in src_dir.iterdir():
            dst = self.output_dir / item.name
            if item.is_dir():
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(item, dst)
            else:
                shutil.copy2(item, dst)

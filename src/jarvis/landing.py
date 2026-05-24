"""Generate the standalone HTML landing page that overrides Sphinx's index."""

import shutil
from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from jarvis.presentations import Presentations
from jarvis.teaching import Teaching
from jarvis.writing import scan_blogs


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
        name="yanga",
        year_range="2023 — present",
        subtitle="Yet Another Ninja Generator",
        description="A Python CMake/Ninja build-system generator for C/C++ software product lines.",
        github_url="https://github.com/cuinixam/yanga",
        code_title="~/SPLed $",
        code_html=(
            '<span class="ac">$ yanga run --variant Disco</span>\n\n'
            '<span class="com"># resolving variant: Disco</span>\n'
            '  <span class="ok">✓</span> light_controller\n'
            '  <span class="ok">✓</span> brightness_controller\n'
            '  <span class="ok">✓</span> main_control_knob\n'
            '  <span class="ok">✓</span> power_button\n'
            '  <span class="ok">✓</span> auto_off\n\n'
            '<span class="com"># generating CMake/Ninja…</span>\n'
            '  <span class="ok">✓</span> CMakeLists.txt\n'
            '  <span class="ok">✓</span> variant.cmake\n'
            '  <span class="ok">✓</span> component libraries\n\n'
            '<span class="com"># building…</span>\n'
            '  <span class="ok">✓</span> sources compiled\n'
            '  <span class="ok">✓</span> unit tests passed\n'
            '  <span class="ok">✓</span> Disco.elf\n\n'
            '<span class="ac">Build succeeded</span>\n'
            "artifacts: build/Disco/"
        ),
    ),
    Project(
        name="clanguru",
        year_range="2024 — present",
        subtitle="C language utils & tools",
        description="C language utils and tools based on the `clang` and `binutils` modules.",
        github_url="https://github.com/cuinixam/clanguru",
        code_title="~/clanguru $",
        code_html=(
            '<span class="ac">$ clanguru --help</span>\n\n'
            '<span class="kw">Usage</span>: clanguru [OPTIONS] COMMAND [ARGS]...\n\n'
            '<span class="com">C language utils and tools based on</span>\n'
            '<span class="com">the libclang module.</span>\n\n'
            '<span class="kw">Commands</span>:\n'
            '  parse     <span class="com">Parse C source and print TU</span>\n'
            '  docs      <span class="com">Generate docs for C/C++ sources</span>\n'
            '  mock      <span class="com">Generate mocks for functions</span>\n'
            '  analyze   <span class="com">Analyze object files dependencies</span>'
        ),
    ),
]


class LandingWriter:
    def __init__(
        self,
        presentations_file: Path,
        presentations_dir: Path,
        teaching_file: Path,
        notebooks_dir: Path,
        blogs_dir: Path,
        output_dir: Path,
        templates_dir: Path | None = None,
    ) -> None:
        self.presentations_file = presentations_file
        self.presentations_dir = presentations_dir
        self.teaching_file = teaching_file
        self.notebooks_dir = notebooks_dir
        self.blogs_dir = blogs_dir
        self.output_dir = output_dir
        self.templates_dir = templates_dir or Path(__file__).parent / "templates" / "landing"

    def write(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        presentations = Presentations.from_json_file(self.presentations_file)
        teaching = Teaching.from_json_file(self.teaching_file)
        writing = scan_blogs(self.blogs_dir)
        env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            autoescape=select_autoescape(["html"]),
        )

        tmpl = env.get_template("index.html.j2")
        html = tmpl.render(
            projects=PROJECTS,
            talks=presentations.talks,
            demos=presentations.demos,
            notebooks=teaching.notebooks,
            writing=writing,
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

import sys
from pathlib import Path
from typing import Annotated

import typer
from py_app_dev.core.exceptions import UserNotificationException
from py_app_dev.core.logging import logger, setup_logger, time_it

from jarvis import __version__
from jarvis.about import AboutWriter
from jarvis.blog import BlogWritter
from jarvis.landing import LandingWriter

package_name = "jarvis"

app = typer.Typer(name=package_name, help="a", no_args_is_help=True, add_completion=False)


@app.callback(invoke_without_command=True)
def version(
    version: bool = typer.Option(None, "--version", "-v", is_eager=True, help="Show version and exit."),
) -> None:
    if version:
        typer.echo(f"{package_name} {__version__}")
        raise typer.Exit()


@app.command()
@time_it("blog")
def blog(
    title: str = typer.Option(help="Title of the blog post."),
    output_dir: Path = typer.Option(Path(__file__).parent.parent.parent.joinpath("docs/blogs"), help="Input timeline json file."),  # noqa: B008
    category: str = "uncategorized",
    tags: Annotated[list[str] | None, typer.Option()] = None,
) -> None:
    BlogWritter(output_dir, title, category, tags).write()


@app.command()
@time_it("landing")
def landing(
    presentations_file: Path = typer.Option(help="Input presentations JSON file."),  # noqa: B008
    presentations_dir: Path = typer.Option(help="Directory of presentation HTML subdirs to copy into the output."),  # noqa: B008
    teaching_file: Path = typer.Option(help="Input teaching JSON file."),  # noqa: B008
    notebooks_dir: Path = typer.Option(help="Directory of notebook HTML subdirs to copy into the output."),  # noqa: B008
    blogs_dir: Path = typer.Option(help="Directory of blog post markdown files (scanned for the writing section)."),  # noqa: B008
    output_dir: Path = typer.Option(help="Output directory (typically the Sphinx build root)."),  # noqa: B008
) -> None:
    LandingWriter(presentations_file, presentations_dir, teaching_file, notebooks_dir, blogs_dir, output_dir).write()


@app.command()
@time_it("about")
def about(
    about_md_file: Path = typer.Option(help="Source markdown file (docs/about.md)."),  # noqa: B008
    timeline_file: Path = typer.Option(help="Input timeline JSON file."),  # noqa: B008
    output_dir: Path = typer.Option(help="Output directory (typically the Sphinx build root)."),  # noqa: B008
) -> None:
    AboutWriter(about_md_file, timeline_file, output_dir).write()


def main() -> int:
    try:
        setup_logger()
        app()
        return 0
    except UserNotificationException as e:
        logger.error(f"{e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

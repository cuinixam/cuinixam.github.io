import sys
from pathlib import Path

import typer
from py_app_dev.core.exceptions import UserNotificationException
from py_app_dev.core.logging import logger, setup_logger, time_it

from jarvis import __version__
from jarvis.timeline import TimelineWriter

package_name = "jarvis"

app = typer.Typer(name=package_name, help="a", no_args_is_help=True)


@app.callback(invoke_without_command=True)
def version(
    version: bool = typer.Option(None, "--version", "-v", is_eager=True, help="Show version and exit."),
) -> None:
    if version:
        typer.echo(f"{package_name} {__version__}")
        raise typer.Exit()


@app.command()
@time_it("timeline")
def timeline(
    input_file: Path = typer.Option(help="Input timeline json file."),  # noqa: B008
    output_file: Path = typer.Option(help="Output timeline markdown file."),  # noqa: B008
    reverse_order: bool = False,
) -> None:
    TimelineWriter(input_file, output_file).write(reverse_order)


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

import sys
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from pathlib import Path
from sys import argv

from mashumaro import DataClassDictMixin
from py_app_dev.core.cmd_line import (
    Command,
    CommandLineHandlerBuilder,
    register_arguments_for_config_dataclass,
)
from py_app_dev.core.exceptions import UserNotificationException
from py_app_dev.core.logging import logger, setup_logger, time_it

from jarvis import __version__
from jarvis.my_app import MyApp


@dataclass
class RunCommandConfig(DataClassDictMixin):
    project_dir: Path = field(
        default=Path(".").absolute(),
        metadata={
            "help": "Project root directory. "
            "Defaults to the current directory if not specified."
        },
    )

    @classmethod
    def from_namespace(cls, namespace: Namespace) -> "RunCommandConfig":
        return cls.from_dict(vars(namespace))


class RunCommand(Command):
    def __init__(self) -> None:
        super().__init__("run", "Start the GUI to build an SPL project.")
        self.logger = logger.bind()

    @time_it()
    def run(self, args: Namespace) -> int:
        self.logger.info(f"Running command '{self.name}' with {args}")
        config = RunCommandConfig.from_namespace(args)
        MyApp(config.project_dir).run()
        return 0

    def _register_arguments(self, parser: ArgumentParser) -> None:
        register_arguments_for_config_dataclass(parser, RunCommandConfig)


def do_run() -> None:
    parser = ArgumentParser(
        prog="jarvis", description="My personal page.", exit_on_error=False
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    builder = CommandLineHandlerBuilder(parser)
    builder.add_commands(
        [
            RunCommand(),
            # TODO: add here more commands
        ]
    )
    handler = builder.create()
    handler.run(argv[1:])


def main() -> int:
    try:
        setup_logger()
        do_run()
    except UserNotificationException as e:
        logger.error(f"{e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

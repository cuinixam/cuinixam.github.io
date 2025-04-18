import io
import json
import textwrap
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from mashumaro.config import TO_DICT_ADD_OMIT_NONE_FLAG, BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from py_app_dev.core.exceptions import UserNotificationException


@dataclass
class TimelineEntry(DataClassJSONMixin):
    year: int
    title: str
    description: str


@dataclass
class Timeline(DataClassJSONMixin):
    entries: list[TimelineEntry]

    class Config(BaseConfig):
        """Base configuration for JSON serialization with omitted None values."""

        code_generation_options: ClassVar[list[str]] = [TO_DICT_ADD_OMIT_NONE_FLAG]

    @classmethod
    def from_json_file(cls, file_path: Path) -> "Timeline":
        try:
            result = cls.from_dict(json.loads(file_path.read_text()))
        except Exception as e:
            output = io.StringIO()
            traceback.print_exc(file=output)
            raise UserNotificationException(output.getvalue()) from e
        return result

    def to_json_string(self) -> str:
        return json.dumps(self.to_dict(omit_none=True), indent=2)

    def to_json_file(self, file_path: Path) -> None:
        file_path.write_text(self.to_json_string())


class TimelineWriter:
    def __init__(self, input_json_file: Path, output_md_file: Path) -> None:
        self.input_json_file = input_json_file
        self.output_md_file = output_md_file

    def write(self, reverse_order: bool = False) -> None:
        timeline = Timeline.from_json_file(self.input_json_file)
        self.output_md_file.write_text(self.timeline_to_md(timeline, reverse_order))

    @staticmethod
    def timeline_to_md(timeline: Timeline, reverse_order: bool) -> str:
        result = ["`````{grid} 2", ":class-container: timeline", "", ""]
        arrange_left = True
        # Parse the timeline entries in reverse order if needed without changing the original list.
        for entry in reversed(timeline.entries) if reverse_order else timeline.entries:
            result.append(TimelineWriter.timeline_entry_to_md(entry, arrange_left))
            arrange_left = not arrange_left
        result.extend(["", "", "`````"])
        return "\n".join(result)

    @staticmethod
    def timeline_entry_to_md(entry: TimelineEntry, arrange_left: bool) -> str:
        return textwrap.dedent(f"""\
            ````{{grid-item-card}}
            :class-item: entry {"left" if arrange_left else "right"}
            <!-- ------------------------------------------------------------------------- -->

            **{entry.year}** {entry.title}
            ^^^

            {entry.description}

            ````


            ````{{grid-item}}
            :class: {"right" if arrange_left else "left"}
            ````
            ````{{grid-item}}
            :class: {"left" if arrange_left else "right"}
            ````""")

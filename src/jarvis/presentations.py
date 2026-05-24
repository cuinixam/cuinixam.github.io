import io
import json
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from mashumaro.config import TO_DICT_ADD_OMIT_NONE_FLAG, BaseConfig
from mashumaro.mixins.json import DataClassJSONMixin
from py_app_dev.core.exceptions import UserNotificationException


@dataclass
class Presentation(DataClassJSONMixin):
    title: str
    description: str
    link: str
    image: str | None = None


@dataclass
class Presentations(DataClassJSONMixin):
    talks: list[Presentation]
    demos: list[Presentation]

    class Config(BaseConfig):
        """Base configuration for JSON serialization with omitted None values."""

        code_generation_options: ClassVar[list[str]] = [TO_DICT_ADD_OMIT_NONE_FLAG]

    @classmethod
    def from_json_file(cls, file_path: Path) -> "Presentations":
        try:
            result = cls.from_dict(json.loads(file_path.read_text()))
        except Exception as e:
            output = io.StringIO()
            traceback.print_exc(file=output)
            raise UserNotificationException(output.getvalue()) from e
        return result

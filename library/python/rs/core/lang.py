import enum
import locale
from pathlib import Path

import dataclasses
from strenum import StrEnum

from rs.core import config

CONFIG_FILE: Path = config.CONFIG_DIR.joinpath('lang.json')


class Code(StrEnum):
    ja = enum.auto()
    en = enum.auto()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_str(cls, s: str) -> 'Code':
        if s not in list(cls):
            return None
        return cls[s]

    @classmethod
    def from_locale(cls) -> 'Code':
        return cls.from_str(locale.getdefaultlocale()[0][:2])


@dataclasses.dataclass
class ConfigData(config.Data):
    lang_code: str = str(Code.ja)


def save(lang_code: Code):
    config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    c = ConfigData()
    c.lang_code = str(lang_code)
    c.save(CONFIG_FILE)


def load() -> Code:
    c = ConfigData()
    if CONFIG_FILE.is_file():
        c.load(CONFIG_FILE)
    return Code.from_str(c.lang_code)


if __name__ == '__main__':
    print(list(Code))
    print(Code.from_str('ja'))
    print(Code.from_str('en'))
    print(Code.from_str('bbb'))
    print(Code.from_locale())

    pass

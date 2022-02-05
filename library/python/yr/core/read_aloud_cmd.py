import dataclasses
from pathlib import Path

from yr.core import config


@dataclasses.dataclass
class Data(config.DataInterface):
    exe_path: str = ''

    text: str = ''

    def export(self, path: Path) -> None:
        pass


if __name__ == '__main__':
    pass

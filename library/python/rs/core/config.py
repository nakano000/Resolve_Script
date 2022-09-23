import json
import os

import dataclasses
from pathlib import Path

from rs.core import util

ROOT_PATH: Path = Path(__file__).joinpath('..', '..', '..', '..', '..').resolve()
LAUNCHER_CONFIG_FILE: Path = ROOT_PATH.joinpath('data', 'app', 'launcher.json')
PYTHONW_EXE_PATH: Path = ROOT_PATH.joinpath(
    json.loads(LAUNCHER_CONFIG_FILE.read_text(encoding='utf-8'))['program']
)
CONFIG_DIR: Path = ROOT_PATH.joinpath('config')
DATA_PATH = ROOT_PATH.joinpath('data')
BIN_PATH = ROOT_PATH.joinpath('bin')

APP_SET_PATH = ROOT_PATH.joinpath('app')
FUSION_SET_PATH = APP_SET_PATH.joinpath('fusion')
RESOLVE_SET_PATH = APP_SET_PATH.joinpath('resolve')

PYTHON_INSTALL_PATH: Path = PYTHONW_EXE_PATH.parent
PYTHON_EXE_PATH = PYTHON_INSTALL_PATH.joinpath('python.exe')

APPDATA_PATH = Path(os.path.expandvars('$APPDATA'))
RESOLVE_USER_PATH = APPDATA_PATH.joinpath('Blackmagic Design', 'DaVinci Resolve', 'Support', 'Fusion')
FUSION_USER_PATH = APPDATA_PATH.joinpath('Blackmagic Design', 'Fusion')


def get_user_path(is_resolve: bool):
    return RESOLVE_USER_PATH if is_resolve else FUSION_USER_PATH


class DataList(list):
    def __init__(self, cls):
        super().__init__()
        self._data_cls = cls

    def new_data(self):
        return self._data_cls()

    def set(self, lst: list):
        self.clear()
        for i in lst:
            data = self._data_cls()
            data.set(i)
            self.append(data)

    def set_list(self, lst: list):
        self.clear()
        for i in lst:
            self.append(i)

    def to_list(self) -> list:
        lst = []
        for i in self:
            lst.append(i)
        return lst

    def to_list_of_dict(self) -> list:
        lst = []
        for i in self:
            lst.append(dataclasses.asdict(i))
        return lst


@dataclasses.dataclass
class DataInterface:
    def set(self, dct):
        base = dataclasses.asdict(self)
        for k in base.keys():
            if k in dct:
                if isinstance(getattr(self, k), DataInterface):
                    getattr(self, k).set(dct[k])
                elif isinstance(getattr(self, k), DataList):
                    getattr(self, k).set(dct[k])
                else:
                    setattr(self, k, dct[k])

    def as_dict(self) -> dict:
        dct = dataclasses.asdict(self)
        for k in dct.keys():
            if isinstance(getattr(self, k), DataList):
                dct[k] = getattr(self, k).to_list_of_dict()
        return dct


@dataclasses.dataclass
class Data(DataInterface):
    def load(self, path: Path) -> None:
        dct = json.loads(path.read_text(encoding='utf-8'))
        self.set(dct)

    def save(self, path: Path) -> None:
        util.write_text(
            path,
            json.dumps(self.as_dict(), indent=2, ensure_ascii=False),
        )


if __name__ == '__main__':
    print(ROOT_PATH)
    print(LAUNCHER_CONFIG_FILE)
    print(LAUNCHER_CONFIG_FILE.read_text(encoding='utf-8'))
    print(PYTHONW_EXE_PATH)
    print(CONFIG_DIR)


    @dataclasses.dataclass
    class D(DataInterface):
        a: int = 10


    dl = DataList(D)
    print(dl)
    dl.set(
        [
            {'a': 10},
            {'a': 20},
            {'a': 30},
        ]
    )
    print(dl)

import json
import os

import dataclasses
from pathlib import Path

from rs.core import util

ROOT_PATH: Path = Path(__file__).joinpath('..', '..', '..', '..', '..').resolve()
LAUNCHER_CONFIG_FILE: Path = ROOT_PATH.joinpath('data', 'app', 'launcher.json')

PYTHONW_EXE_PATH: Path = ROOT_PATH.joinpath(
    json.loads(LAUNCHER_CONFIG_FILE.read_text(encoding='utf-8'))['program'].replace('\\', os.sep)
)

CONFIG_DIR: Path = ROOT_PATH.joinpath('config')
DATA_PATH = ROOT_PATH.joinpath('data')
BIN_PATH = ROOT_PATH.joinpath('bin')

APP_SET_PATH = ROOT_PATH.joinpath('app')
FUSION_SET_PATH = APP_SET_PATH.joinpath('fusion')
RESOLVE_SET_PATH = APP_SET_PATH.joinpath('resolve')

if util.IS_WIN:
    PYTHON_INSTALL_PATH: Path = PYTHONW_EXE_PATH.parent
else:
    PYTHON_INSTALL_PATH: Path = ROOT_PATH.joinpath('bin', 'python-3')

PYTHON_EXE_PATH = PYTHON_INSTALL_PATH.joinpath('python.exe')
PYTHON_SCRIPTS_PATH = PYTHON_INSTALL_PATH.joinpath('Scripts')
if util.IS_WIN:
    APPDATA_PATH = Path(os.path.expandvars('$APPDATA'))
    RESOLVE_USER_PATH = APPDATA_PATH.joinpath('Blackmagic Design', 'DaVinci Resolve', 'Support', 'Fusion')
    FUSION_USER_PATH = APPDATA_PATH.joinpath('Blackmagic Design', 'Fusion')
elif util.IS_MAC:
    APPDATA_PATH = Path(os.path.expandvars('$HOME')).joinpath('Library', 'Application Support')
    RESOLVE_USER_PATH = APPDATA_PATH.joinpath('Blackmagic Design', 'DaVinci Resolve', 'Fusion')
    FUSION_USER_PATH = APPDATA_PATH.joinpath('Blackmagic Design', 'Fusion')
else:
    APPDATA_PATH = Path(os.path.expandvars('$HOME')).joinpath('.local', 'share')
    RESOLVE_USER_PATH = APPDATA_PATH.joinpath('DaVinciResolve', 'Fusion')
    FUSION_USER_PATH = APPDATA_PATH.joinpath('Fusion')

ENCODING_LIST = [
    'utf-8',
    'utf-8-sig',
    'utf-16',
    'utf-16be',
    'utf-16le',
    'utf-32',
    'utf-32be',
    'utf-32le',
    'cp932',
    'shift_jis',
]

MARKER_COLOR_LIST = [
    'Blue',
    'Cyan',
    'Green',
    'Yellow',
    'Red',
    'Pink',
    'Purple',
    'Fuchsia',
    'Rose',
    'Lavender',
    'Sky',
    'Mint',
    'Lemon',
    'Sand',
    'Cocoa',
    'Cream',
]

COLOR_LIST = [
    'Orange',
    'Apricot',
    'Yellow',
    'Lime',
    'Olive',
    'Green',
    'Teal',
    'Navy',
    'Blue',
    'Purple',
    'Violet',
    'Pink',
    'Tan',
    'Beige',
    'Brown',
    'Chocolate',
]


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
            lst.append(i.as_dict())
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

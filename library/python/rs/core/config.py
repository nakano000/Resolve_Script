import json
import dataclasses
from pathlib import Path

ROOT_PATH: Path = Path(__file__).joinpath('..', '..', '..', '..', '..').resolve()
LAUNCHER_CONFIG_FILE: Path = ROOT_PATH.joinpath('data', 'app', 'launcher.json')
PYTHONW_EXE_PATH: Path = ROOT_PATH.joinpath(
    json.loads(LAUNCHER_CONFIG_FILE.read_text())['program']
)
CONFIG_DIR: Path = ROOT_PATH.joinpath('config')


@dataclasses.dataclass
class DataInterface:
    def set(self, dct):
        base = dataclasses.asdict(self)
        for k in base.keys():
            if k in dct:
                if isinstance(getattr(self, k), DataInterface):
                    getattr(self, k).set(dct[k])
                else:
                    setattr(self, k, dct[k])


@dataclasses.dataclass
class Data(DataInterface):
    def load(self, path: Path) -> None:
        dct = json.loads(path.read_text())
        self.set(dct)

    def save(self, path: Path) -> None:
        path.write_text(
            json.dumps(dataclasses.asdict(self), indent=2),
            encoding='utf-8',
        )


if __name__ == '__main__':
    print(ROOT_PATH)
    print(LAUNCHER_CONFIG_FILE)
    print(LAUNCHER_CONFIG_FILE.read_text())
    print(PYTHONW_EXE_PATH)
    print(CONFIG_DIR)

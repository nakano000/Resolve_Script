from pathlib import Path

import dataclasses
from typing import List

from rs.core import config
from rs.gui import basic_table


@dataclasses.dataclass
class CharaData(basic_table.RowData):
    # reg_exp: str = r'^\d+_ずんだもん.+'
    track_name: str = ''
    reg_exp: str = r'.+'
    color: str = 'None'
    _setting: str = r'Preset\TextPlus\字幕_白.setting'

    @property
    def setting_file(self) -> Path:
        path = Path(self._setting)
        if not path.is_absolute():
            return config.ROOT_PATH.joinpath(str(path))
        return path

    @setting_file.setter
    def setting_file(self, path: Path):
        if str(path).lower().startswith(str(config.ROOT_PATH).lower()):
            self._setting = str(path.relative_to(config.ROOT_PATH))
        else:
            self._setting = str(path)

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ['トラック名', '正規表現', '色', 'settingファイル']


if __name__ == '__main__':
    c = CharaData()
    print(c._setting)
    print(c.setting_file)


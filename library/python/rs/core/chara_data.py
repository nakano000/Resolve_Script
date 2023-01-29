from pathlib import Path

import dataclasses
from typing import List

from rs.core import (
    config,
    pipe as p,
    anim,
)
from rs.gui import table

CONFIG_DIR: Path = config.CONFIG_DIR.joinpath('VoiceBin')
CONFIG_FILE: Path = CONFIG_DIR.joinpath('chara.json')
TEMPLATE_FILE: Path = config.DATA_PATH.joinpath('app', 'VoiceBin', 'chara.json')


@dataclasses.dataclass
class CharaData(table.RowData):
    # reg_exp: str = r'^\d+_ずんだもん.+'
    track_name: str = ''
    reg_exp: str = r'.+'
    color: str = 'None'
    c_code: str = 'auto'
    str_width: int = 0
    anim_type: str = anim.Type.aiueo.value
    anim_parameter: str = 'Anim'
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
        return [
            ' トラック名 ',
            ' 正規表現 ',
            ' クリップカラー ',
            ' 文字コード ',
            ' 字幕幅 ',
            ' 口パク タイプ ',
            ' 口パク パラメータ名 ',
            ' settingファイル ',
        ]


@dataclasses.dataclass
class CharaSetData(config.Data):
    chara_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(CharaData))


def get_chara_list():
    f = CONFIG_FILE
    if not f.is_file():
        f = TEMPLATE_FILE
    a = CharaSetData()
    a.load(f)
    return a.chara_list


if __name__ == '__main__':
    c = CharaData()
    print(c._setting)
    print(c.setting_file)

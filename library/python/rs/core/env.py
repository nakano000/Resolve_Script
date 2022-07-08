import os
import enum
from pathlib import Path

from typing import Dict, List, Optional

from rs.core import pipe as p, util


class EnvKey(util.StrEnum):
    #
    RS_FUSION_USER_PATH = enum.auto()
    # python
    PYTHONDONTWRITEBYTECODE = enum.auto()
    PYTHONPATH = enum.auto()
    PYTHONHOME = enum.auto()
    # maya
    MAYA_SCRIPT_PATH = enum.auto()
    MAYA_SHELF_PATH = enum.auto()
    XBMLANGPATH = enum.auto()
    MAYA_PLUG_IN_PATH = enum.auto()
    MAYA_MODULE_PATH = enum.auto()
    MAYA_ENABLE_LEGACY_RENDER_LAYERS = enum.auto()
    MAYA_RENDER_DESC_PATH = enum.auto()
    # houdini
    HOUDINI_PATH = enum.auto()
    # resolve fusion
    PYTHON3HOME = enum.auto()
    FUSION_Python3_Home = enum.auto()
    FUSION_Python36_Home = enum.auto()  # 9ではFUSION9とかになる？
    FUSION_MasterPrefs = enum.auto()
    FUSION_MasterPrefs8 = enum.auto()
    FUSION9_MasterPrefs = enum.auto()
    FUSION16_MasterPrefs = enum.auto()
    # OCIO
    OCIO = enum.auto()
    OCIO_ACTIVE_DISPLAYS = enum.auto()
    OCIO_ACTIVE_VIEWS = enum.auto()
    #
    ARNOLD_PLUGIN_PATH = enum.auto()
    PXR_PLUGINPATH_NAME = enum.auto()
    #
    PATH = enum.auto()


class Env:
    def __init__(self, e: Optional[Dict[str, str]] = None) -> None:
        self._env = e
        if self._env is None:
            self._env = os.environ.copy()

    def get(self, key: EnvKey) -> str:
        env_key = key.name
        if env_key not in self._env:
            return ''
        return self._env[env_key]

    def set(self, key: EnvKey, s: str):
        env_key = key.name
        self._env[env_key] = s

    def set_by_text(self, s: str) -> None:
        for n, v in p.pipe(
                s,
                p.call.split('\n'),
                p.map(lambda x: x.split('=')),
                p.filter(lambda x: len(x) == 2),
                p.map(lambda x: (x[0].strip(), x[1].strip())),
                list,
        ):
            ss = v.split('%')
            for i in range(len(ss)):
                if i % 2 == 1:
                    val = ''
                    if ss[i] in self._env:
                        val = self._env[ss[i]]
                    v = v.replace('%' + ss[i] + '%', val, 1)
            self._env[n] = v

    def add(self, key: EnvKey, prefix: str, suffix: str) -> None:
        env_key = key.name
        if env_key not in self._env:
            self._env[env_key] = ''
        self._env[env_key] = prefix + self._env[env_key] + suffix

    def add_path(self, key: EnvKey, pre: Optional[List[Path]] = None, suf: Optional[List[Path]] = None) -> None:
        if pre is None:
            pre = []
        if suf is None:
            suf = []
        env_key = key.name
        ss = [] if env_key not in self._env else [self._env[env_key]]
        lst = list(map(str, pre)) + ss + list(map(str, suf))
        self.set(key, os.pathsep.join(lst))

    def to_dict(self) -> Dict[str, str]:
        return self._env.copy()


if __name__ == '__main__':
    env = Env()
    print(p.pipe(
        [Path('aaa'), Path('bbb')],
        p.map(str),
        os.pathsep.join,
    ))

    print(os.pathsep.join(['aaa', 'bbb']))
    print(list(EnvKey))
    pass

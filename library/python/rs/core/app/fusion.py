# -*- coding: utf-8 -*-

import os
import string
import dataclasses
from pathlib import Path
from typing import Dict

from rs.core import config
from rs.core import pipe as p
from rs.core.app import App
from rs.core.env import Env, EnvKey


@dataclasses.dataclass
class Fusion(App):
    exe: str = r'C:\Program Files\Blackmagic Design\Fusion 18\Fusion.exe'

    def get_path(self) -> Path:
        return Path(self.exe)

    def get_env(self) -> Env:
        env = super().get_env()
        env.set(
            EnvKey.RS_FUSION_USER_PATH,
            str(config.FUSION_SET_PATH.joinpath('UserPath')) + str('\\')
        )

        # FUSION_MasterPrefs
        master_prefs = config.FUSION_SET_PATH.joinpath('rs.prefs')
        env.set(EnvKey.FUSION_MasterPrefs, str(master_prefs))
        env.set(EnvKey.FUSION_MasterPrefs8, str(master_prefs))
        env.set(EnvKey.FUSION9_MasterPrefs, str(master_prefs))
        env.set(EnvKey.FUSION16_MasterPrefs, str(master_prefs))

        # PYTHONPATH
        env.add_path(EnvKey.PYTHONPATH, pre=[
            config.APP_SET_PATH.joinpath('fusion', 'python'),
        ])

        # PYTHONHOME
        env.set(EnvKey.PYTHON3HOME, str(config.PYTHON_INSTALL_PATH))
        env.set(EnvKey.FUSION_Python3_Home, str(config.PYTHON_INSTALL_PATH))
        env.set(EnvKey.FUSION_Python36_Home, str(config.PYTHON_INSTALL_PATH))
        # PATH
        env.add_path(EnvKey.PATH, pre=[
            config.PYTHON_INSTALL_PATH,
        ])

        return env


if __name__ == '__main__':
    print(config.PYTHON_INSTALL_PATH)
    app = Fusion()
    app.execute([])

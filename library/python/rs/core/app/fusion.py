# -*- coding: utf-8 -*-

import os
import dataclasses
from pathlib import Path

from rs.core import config, util
from rs.core import pipe as p
from rs.core.app import App
from rs.core.env import Env, EnvKey


def _get_def():
    if util.IS_WIN:
        return r'C:\Program Files\Blackmagic Design\Fusion 18\Fusion.exe'
    elif util.IS_MAC:
        return '/Applications/Blackmagic Fusion 18/Fusion.app'
    else:
        return '/opt/BlackmagicDesign/Fusion9/Fusion'


@dataclasses.dataclass
class Fusion(App):
    exe: str = _get_def()

    def get_path(self) -> Path:
        return Path(self.exe)

    def get_env(self) -> Env:
        env = super().get_env()
        env.set(
            EnvKey.RS_FUSION_USER_PATH,
            str(config.FUSION_SET_PATH.joinpath('UserPath')) + os.sep
        )

        # FUSION_MasterPrefs
        # master_prefs = config.FUSION_SET_PATH.joinpath('rs.prefs')
        # env.set(EnvKey.FUSION_MasterPrefs, str(master_prefs))
        # env.set(EnvKey.FUSION_MasterPrefs8, str(master_prefs))
        # env.set(EnvKey.FUSION9_MasterPrefs, str(master_prefs))
        # env.set(EnvKey.FUSION16_MasterPrefs, str(master_prefs))

        # PYTHONPATH
        env.add_path(EnvKey.PYTHONPATH, pre=[
            config.APP_SET_PATH.joinpath('fusion', 'python'),
        ])
        if util.IS_WIN or util.IS_MAC:
            # PYTHONHOME
            env.set(EnvKey.PYTHON3HOME, str(config.PYTHON_INSTALL_PATH))
            env.set(EnvKey.FUSION_Python3_Home, str(config.PYTHON_INSTALL_PATH))
            env.set(EnvKey.FUSION_Python36_Home, str(config.PYTHON_INSTALL_PATH))
            # PATH
            python_bin_path = config.PYTHON_INSTALL_PATH
            if util.IS_MAC:
                python_bin_path = config.PYTHON_INSTALL_PATH.joinpath('bin')
            env.add_path(EnvKey.PATH, pre=[
                python_bin_path,
            ])

        return env


if __name__ == '__main__':
    print(config.PYTHON_INSTALL_PATH)
    app = Fusion()
    app.execute([])

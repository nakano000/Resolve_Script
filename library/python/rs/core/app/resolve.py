# -*- coding: utf-8 -*-

import os
import string
import dataclasses
import winreg
from pathlib import Path

from rs.core import config
from rs.core import pipe as p
from rs.core.app import Fusion
from rs.core.env import Env, EnvKey


@dataclasses.dataclass
class Resolve(Fusion):
    exe: str = r'C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'

    def get_env(self) -> Env:
        env = super().get_env()
        # PYTHONPATH
        env.add_path(EnvKey.PYTHONPATH, pre=[
            config.APP_SET_PATH.joinpath('resolve', 'python'),
        ])
        return env


if __name__ == '__main__':
    print(config.PYTHON_INSTALL_PATH)
    app = Resolve()
    app.execute([])

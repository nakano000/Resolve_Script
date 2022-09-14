# -*- coding: utf-8 -*-

import os
import string
import dataclasses
from pathlib import Path

from rs.core import config, util
from rs.core import pipe as p
from rs.core.app import Fusion
from rs.core.env import Env, EnvKey


@dataclasses.dataclass
class Resolve(Fusion):
    exe: str = (
        r'C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'
        if util.IS_WIN else
        '/opt/resolve/bin/resolve'
    )

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

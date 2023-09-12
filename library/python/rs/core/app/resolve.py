# -*- coding: utf-8 -*-

import dataclasses

from rs.core import config, util
from rs.core import pipe as p
from rs.core.app import Fusion
from rs.core.env import Env, EnvKey


def _get_def():
    if util.IS_WIN:
        return r'C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe'
    elif util.IS_MAC:
        return '/Applications/DaVinci Resolve/DaVinci Resolve.app'
    else:
        return '/opt/resolve/bin/resolve'


@dataclasses.dataclass
class Resolve(Fusion):
    exe: str = _get_def()

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

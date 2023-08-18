import dataclasses
import subprocess
from pathlib import Path

from rs.core import config
from rs.core.env import Env, EnvKey


@dataclasses.dataclass
class App(config.DataInterface):
    def get_path(self) -> Path:
        return Path()

    def get_env(self) -> Env:
        env = Env()
        # PYTHONDONTWRITEBYTECODE
        # env.set(EnvKey.PYTHONDONTWRITEBYTECODE, '1')
        # PYTHONPATH
        env.add_path(EnvKey.PYTHONPATH, suf=[
            config.ROOT_PATH.joinpath('library', 'python'),
        ])
        return env

    def execute(self, args) -> None:
        path = self.get_path()
        cmd = [
                  str(path),
              ] + args
        env = self.get_env().to_dict()
        subprocess.Popen(
            cmd,
            env=env,
        )


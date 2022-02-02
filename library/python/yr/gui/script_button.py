import os
import subprocess
from pathlib import Path
from typing import Optional

from PySide2.QtWidgets import (
    QPushButton,
)

from yr.core import config


def run_python(path, args, env=None):
    cmd = [
              str(config.PYTHONW_EXE_PATH),
              str(path),
          ] + list(args)
    if env is None:
        env = os.environ.copy()
    subprocess.Popen(
        cmd,
        # shell=True,
        env=env,
    )


class ScriptButton(QPushButton):
    def __init__(self, *args, script_path=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.script_file: Optional[Path] = script_path

        self.clicked.connect(self.run)

    def run(self) -> None:
        if self.script_file is None:
            return
        run_python(self.script_file, [])

import sys
import os
from pathlib import Path

lib_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../library/python')
)
sys.path.append(lib_path)

from rs.core import (
    config,
    pipe as p,
)

if __name__ == "__main__":
    import shutil

    # C:\ProgramData\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
    # %APPDATA%\Blackmagic Design\DaVinci Resolve\Fusion\Scripts
    # C:\ProgramData\Blackmagic Design\Fusion\Scripts
    # %APPDATA%\Blackmagic Design\Fusion\Scripts
    for f in p.pipe(
            config.ROOT_PATH.joinpath('Scripts', 'Comp').iterdir(),
            p.filter(p.call.is_file()),
            p.filter(lambda x: x.suffix.lower() in ['.py', '.py2', '.py3']),
    ):
        shutil.copyfile(
            f,
            Path(os.path.expandvars('%APPDATA%')).joinpath(
                'Blackmagic Design', 'Fusion', 'Scripts', 'Comp', f.name
            ),
        )

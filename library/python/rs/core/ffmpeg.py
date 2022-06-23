import os
import subprocess
from pathlib import Path

from rs.core import config

EMPTY_IMAGE = config.ROOT_PATH.joinpath('data', 'image', 'empty.png')
EXE_PATH = config.ROOT_PATH.joinpath('bin', 'ffmpeg-5.0.1-essentials_build', 'bin', 'ffmpeg.exe')


def execute(args) -> None:
    cmd = [
              str(EXE_PATH),
          ] + args
    env = os.environ.copy()
    proc = subprocess.Popen(
        cmd,
        env=env,
    )
    proc.wait()


def make_args(wav_path: Path, out_path: Path) -> list:
    return [
        '-y',
        '-loop',
        '1',
        '-i',
        str(EMPTY_IMAGE),
        '-i',
        str(wav_path),
        '-r',
        '30',
        '-shortest',
        '-c:v',
        'prores_ks',
        '-profile:v',
        '4',
        str(out_path),
    ]


if __name__ == '__main__':
    wave_file = Path(r'\\qnap\pj\youtube\test\out05\003_四国めたん（ノーマル）_こんばんは.wav')
    out_file = Path('D:/tmp/c.mov')
    execute(make_args(wave_file, out_file))

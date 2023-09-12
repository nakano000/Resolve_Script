import functools
import platform
import subprocess
import unicodedata

from pathlib import Path

import budoux

from rs.core import (
    pipe as p,
)


class Singleton:
    _unique_instance = None

    @classmethod
    def get_instance(cls):
        if not cls._unique_instance:
            cls._unique_instance = cls()

        return cls._unique_instance


def memoize(f):
    cache = f.cache = {}

    def del_cache(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key in cache:
            del cache[key]

    f.del_cache = del_cache

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if key not in cache:
            cache[key] = f(*args, **kwargs)
        return cache[key]

    return wrapper


IS_WIN = platform.system() == 'Windows'
IS_MAC = platform.system() == 'Darwin'


def write_text(path: Path, s: str) -> None:
    with path.open('w', encoding='utf-8', newline='\n') as f:
        f.write(s)


def open_url(url):
    import webbrowser
    webbrowser.get('windows-default').open(url)


def open_directory(path: Path):
    subprocess.Popen(['explorer', str(path)])


def get_char_width(c):
    data = unicodedata.east_asian_width(c)
    return 1 if data in ['Na', 'H'] else 2


def get_str_width(s):
    return p.pipe(
        s,
        p.map(get_char_width),
        sum,
    )


def str2lines(s: str, width: int):
    if width <= 0:
        return s
    parser = budoux.load_default_japanese_parser()
    ss = parser.parse(s)
    lines = ['']
    for _s in ss:
        if get_str_width(lines[-1] + _s) > width:
            lines.append(_s)
        else:
            lines[-1] += _s
    return '\n'.join(lines)


if __name__ == '__main__':
    print(get_str_width('abcあいう'))
    print(str2lines('今日は晴れています。', 10))

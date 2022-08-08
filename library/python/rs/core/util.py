import enum
import functools
import subprocess
from pathlib import Path


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


def open_url(url):
    import webbrowser
    webbrowser.get('windows-default').open(url)


def open_directory(path: Path):
    subprocess.Popen(['explorer', str(path)])


if __name__ == '__main__':
    pass

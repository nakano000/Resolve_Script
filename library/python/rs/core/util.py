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


class StrEnum(str, enum.Enum):
    """
    Enum where members are also (and must be) strings
    """

    def __new__(cls, *values):
        if len(values) > 3:
            raise TypeError('too many arguments for str(): %r' % (values,))
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError('%r is not a string' % (values[0],))
        if len(values) >= 2:
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError('encoding must be a string, not %r' % (values[1],))
        if len(values) == 3:
            # check that errors argument is a string
            if not isinstance(values[2], str):
                raise TypeError('errors must be a string, not %r' % (values[2]))
        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    __str__ = str.__str__

    __format__ = str.__format__

    def _generate_next_value_(name, start, count, last_values):
        """
        """
        return name


if __name__ == '__main__':
    class TesEnum(StrEnum):
        AAA = enum.auto()


    print(TesEnum.AAA.name)
    print(TesEnum.AAA.value)
    pass

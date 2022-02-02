# -*- coding: utf-8 -*-

import traceback
import builtins

from operator import attrgetter
from operator import methodcaller

from functools import (
    partial,
    reduce,
)


class MethodCaller:
    def __getattribute__(self, name):
        return partial(methodcaller, name)

    def __getattr__(self, name):
        return partial(methodcaller, name)


call = MethodCaller()


class AttrGetter:
    def __getattribute__(self, name):
        return attrgetter(name)

    def __getattr__(self, name):
        return attrgetter(name)


get = AttrGetter()


def map(f):
    return partial(builtins.map, f)


def iter(f):
    def _f(x):
        list(builtins.map(f, x))  # 要素を計算させる目的でlistにしている。
        return []

    return _f


def filter(f):
    def _f(*args, **kwargs) -> bool:
        r = f(*args, **kwargs)
        if type(r) is not bool:
            try:
                raise TypeError
            except TypeError as e:
                traceback.print_exc()
                raise
        return r

    return partial(builtins.filter, _f)


def do(*fs):
    def _do(x):
        pipe(x, *fs)
        return x

    return _do


def pipe(x, *fs):
    return reduce(lambda a, b: b(a), fs, x)


if __name__ == '__main__':
    print('test')
    pipe(
        "aaa",
        print,
    )

    print('end')

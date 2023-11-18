import re
from pathlib import Path

from rs.core import (
    pipe as p,
)


def read(path: Path):
    dct = {
        'notes': []
    }
    for lst in p.pipe(
            path.read_text(encoding='cp932'),
            lambda x: re.split(r'\n(?=\[#)', x),
            p.map(p.call.split('\n')),
            p.filter(lambda x: len(x) > 1),
            p.map(lambda x: [
                re.sub(r'\[#(.+)]', r'\1', x[0]),
                p.pipe(
                    x[1:],
                    p.map(p.call.split('=')),
                    p.filter(lambda y: len(y) == 1 or len(y) == 2),
                    p.map(lambda y: [y[0], None] if len(y) == 1 else y),
                    dict,
                    lambda y: y if len(y.keys()) != 1 else (
                            y if list(y.values())[0] is not None else list(y.keys())[0]
                    ),
                ),
            ]),
            list,
    ):
        try:
            index = int(lst[0])
            dct['notes'].append(lst[1])
            dct['notes'][-1]['Index'] = index
        except ValueError:
            dct[lst[0]] = lst[1]
    return dct


if __name__ == '__main__':
    pass

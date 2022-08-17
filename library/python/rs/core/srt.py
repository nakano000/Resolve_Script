from datetime import timedelta
from pathlib import Path
from typing import List

import dataclasses
from rs.core import pipe as p


def seconds2str(s: float) -> str:
    t = timedelta(seconds=s)
    l: List[str] = str(t).split(':')
    if len(l) == 3:
        l[0] = l[0].zfill(2)
        if len(l[2]) == 2:
            l[2] += '.000000'
        l[2] = l[2].replace('.', ',')[:6]
    return ':'.join(l)


@dataclasses.dataclass
class Subtitle:
    start_time: float = 0.0  # seconds
    end_time: float = 0.0  # seconds
    text: str = ''

    def __str__(self) -> str:
        return '%s --> %s\n%s' % (
            seconds2str(self.start_time),
            seconds2str(self.end_time),
            self.text.strip(),
        )


class Srt:
    def __init__(self):
        self.subtitles: List[Subtitle] = []

    def __str__(self) -> str:
        return p.pipe(
            self.subtitles,
            enumerate,
            p.map(lambda x: '%d\n%s\n' % (x[0] + 1, x[1])),
            '\n'.join,
        )

    def save(self, path: Path) -> None:
        path.write_text(
            str(self),
            encoding='utf-8',
        )


if __name__ == '__main__':
    srt = Srt()
    s1 = Subtitle(0, 1.2, 'おはようございます。')
    s2 = Subtitle()
    s2.start_time = 0.0
    s2.end_time = 3456.3333333
    s2.text = 'こんばんは'
    srt.subtitles.append(s1)
    srt.subtitles.append(s2)
    print(str(srt))
    print('end')

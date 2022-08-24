from pathlib import Path
from rs.core import pipe as p

_NONE = 0
_N = 1
_A = 2
_I = 3
_U = 4
_E = 5
_O = 6


def sign2int(s: str):
    if s in ['pau']:
        return _N
    if s in ['a', 'A']:
        return _A
    if s in ['i', 'I']:
        return _I
    if s in ['u', 'U']:
        return _U
    if s in ['e', 'E']:
        return _E
    if s in ['o', 'O']:
        return _O
    if s in ['N', 'cl']:
        return _N
    return _E


def lab2anim(path: Path, fps) -> str:
    n = 10000000
    dct = {}
    for d in p.pipe(
            path.read_text(encoding='utf-8-sig').split('\n'),
            p.map(p.call.split(' ')),
            p.filter(lambda x: len(x) == 3),
            p.map(lambda x: {
                's': round(int(x[0]) * fps / n),
                'e': round(int(x[1]) * fps / n),
                'sign': sign2int(x[2]),
            }),
            list,
    ):
        dct[d['s']] = d['sign']
        dct[d['e']] = _NONE

    if len(dct) < 2:
        return ''

    space = '\t\t\t\t'
    key01_block = '[%d] = { %d,'
    # key02_block = ' LHrel = { %s, %s },'
    # key03_block = ' RHrel = { %s, %s },'
    key02_block = ' LH = { %s, %s },'
    key03_block = ' RH = { %s, %s },'
    flagA_block = ' Flags = { Linear = true } }'
    flagB_block = ' Flags = { StepIn = true } }'

    key_list = []
    size = len(dct)
    flame_list = list(dct.keys())

    # 最初と最後は_NONEにしておく
    dct[flame_list[0]] = _NONE
    dct[flame_list[size - 1]] = _NONE

    for i, frame in enumerate(flame_list):
        v = dct[frame]
        s = key01_block % (frame, v)
        if i != 0:
            s += key02_block % (str(frame), str(v + ((dct[flame_list[i - 1]] - v) / 3.0)))
        if i != size - 1:
            s += key03_block % (str(frame + ((flame_list[i + 1] - frame) / 3.0)), str(v))
        if i == 0:
            s += flagA_block
        else:
            s += flagB_block
        key_list.append(s)

    return space + (',\n' + space).join(key_list)


if __name__ == '__main__':
    setting = lab2anim(Path(r'\\qnap\PJ\youtube\test\out06\001_四国めたん（ノーマル）_おはようございます。.lab'), 30)
    print(setting)

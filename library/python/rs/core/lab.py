from pathlib import Path
import numpy as np
import librosa
from rs.core import (
    anim,
    pipe as p,
)

_NONE = 0
_N = 1
_A = 2
_I = 3
_U = 4
_E = 5
_O = 6
_S = 7


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
    return _S


def sign2intE(s: str):
    """子音はEとして扱う"""
    n: int = sign2int(s)
    if n == _S:
        return _E
    return n


def dict2anim(dct) -> str:
    space = '\t\t\t\t'
    key01_block = '[%d] = { %s,'
    key02_block = ' LH = { %s, %s },'
    key03_block = ' RH = { %s, %s },'
    flagA_block = ' Flags = { Linear = true } }'
    flagB_block = ' Flags = { StepIn = true } }'

    if len(dct) < 2:
        return ''

    key_list = []
    size = len(dct)
    flame_list = list(dct.keys())

    # 最初と最後は0にしておく
    dct[flame_list[0]] = 0
    dct[flame_list[size - 1]] = 0

    for i, frame in enumerate(flame_list):
        v = dct[frame]
        s = key01_block % (frame, str(v))
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


def lab2anim(path: Path, fps, anim_tpe, offset: int = 0) -> str:
    n = 10000000
    func = sign2intE
    if anim_tpe == anim.Type.aiueo2:
        func = sign2int

    # lab 読み込み
    data = p.pipe(
        path.read_text(encoding='utf-8-sig').split('\n'),
        p.map(p.call.split(' ')),
        p.filter(lambda x: len(x) == 3),
        p.map(lambda x: {
            's': offset + round(int(x[0]) * fps / n),
            'e': offset + round(int(x[1]) * fps / n),
            'sign': func(x[2]),
        }),
        list,
    )

    # 子音除去
    pre_sign = _N
    for i in reversed(range(len(data))):
        if data[i]['sign'] == _S:
            data[i]['sign'] = pre_sign
        else:
            pre_sign = data[i]['sign']

    # dict 作成
    dct = {}
    for d in data:
        dct[d['s']] = d['sign']
        dct[d['e']] = _NONE

    return dict2anim(dct)


def wav2anim(path: Path, fps, offset: int = 0) -> str:
    y, sr = librosa.load(str(path))
    rms = librosa.feature.rms(y=y)
    m = rms.max() + 0.001
    rms_n = rms / m
    times = librosa.times_like(rms, sr=sr)
    frame = np.round(times * fps)
    dct = {}
    for i, v in enumerate(frame):
        dct[int(v) + offset] = rms_n[0][i]
    return dict2anim(dct)


if __name__ == '__main__':
    p.pipe(
        lab2anim(
            Path(r'\\qnap\PJ\youtube\test\out06\001_四国めたん（ノーマル）_おはようございます。.lab'),
            30,
            anim.Type.aiueo,
        ),
        print,
    )
    p.pipe(
        lab2anim(
            Path(r'\\qnap\PJ\youtube\test\out06\001_四国めたん（ノーマル）_おはようございます。.lab'),
            30,
            anim.Type.aiueo2,
        ),
        print,
    )
    print(anim.TYPE_LIST)

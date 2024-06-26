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


def _dict2anim_process(dct) -> str:
    space = '\t\t\t\t'
    key01_block = '[%d] = { %s,'
    key02_block = ' LH = { %s, %s },'
    key03_block = ' RH = { %s, %s },'
    flagA_block = ' Flags = { Linear = true } }'
    flagB_block = ' Flags = { StepIn = true } }'

    key_list = []
    size = len(dct)
    flame_list = list(dct.keys())

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


def dict2anim(dct) -> str:
    size = len(dct)
    flame_list = list(dct.keys())

    if len(dct) < 2:
        return ''

    # 最初と最後は0にしておく
    dct[flame_list[0]] = 0
    dct[flame_list[size - 1]] = 0

    return _dict2anim_process(dct)


def dict2anim_mm(dct) -> list:
    anim_list = []
    if len(dct) < 2:
        return anim_list
    size = len(dct)
    flame_list = list(dct.keys())

    # 最初と最後は0にしておく
    dct[flame_list[0]] = 0
    dct[flame_list[size - 1]] = 0

    for i in range(7):
        _dct = {}
        for frame in flame_list:
            if dct[frame] == i:
                _dct[frame] = 1
            else:
                _dct[frame] = 0
        anim_list.append(_dict2anim_process(_dct))
    return anim_list


def read(path: Path):
    lst = p.pipe(
        path.read_text(encoding='utf-8-sig').split('\n'),
        p.map(p.call.split(' ')),
        p.filter(lambda x: len(x) == 3),
        p.map(lambda x: {
            's': int(x[0]),
            'e': int(x[1]),
            'sign': x[2],
        }),
        p.filter(lambda x: x['s'] < x['e']),
        list,
    )
    if lst[0]['s'] != 0:
        lst.insert(0, {
            's': 0,
            'e': lst[0]['s'],
            'sign': 'pau',
        })
    return lst


def _lab2anim(path: Path, fps, anim_tpe, offset: int = 0, is_mm: bool = False) -> list:
    n = 10000000
    scale = 0.8

    func = sign2intE
    if anim_tpe in [anim.Type.aiueo2, anim.Type.aiueo3]:
        func = sign2int

    # lab 読み込み
    pre_data = p.pipe(
        read(path),
        p.map(lambda x: {
            's': offset + round(x['s'] * fps / n),
            'e': offset + round(x['e'] * fps / n),
            'sign': x['sign'],
        }),
        list,
    )
    data = p.pipe(
        pre_data,
        p.map(lambda x: {
            's': x['s'], 'e': x['e'], 'sign': func(x['sign'])
        }),
        list,
    )
    scale_data = []
    if anim_tpe == anim.Type.aiueo3:
        scale_data = p.pipe(
            pre_data,
            p.map(lambda x: {
                's': x['s'], 'e': x['e'], 'sign': func(x['sign'])
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
    scale_dct = {}
    if anim_tpe == anim.Type.aiueo3:
        for d in scale_data:
            scale_dct[d['s']] = scale if d['sign'] == _S else 1.0
            scale_dct[d['e']] = 1.0

    if is_mm:
        anim_list = dict2anim_mm(dct)
        if anim_tpe == anim.Type.aiueo3:
            anim_list.append(_dict2anim_process(scale_dct))
        return anim_list
    else:
        return [dict2anim(dct)]


def lab2anim(path: Path, fps, anim_tpe, offset: int = 0) -> str:
    anim_list = _lab2anim(path, fps, anim_tpe, offset)
    return anim_list[0]


def lab2anim_mm(path: Path, fps, anim_tpe, offset: int = 0) -> list:
    return _lab2anim(path, fps, anim_tpe, offset, is_mm=True)


def get_wav_data(path: Path, fps, offset: int = 0):
    y, sr = librosa.load(str(path))
    rms = librosa.feature.rms(y=y)
    m = rms.max() + 0.001  # 0 除算防止
    rms_n = rms / m
    times = librosa.times_like(rms, sr=sr)
    frame = np.round(times * fps)
    dct = {}
    for i, v in enumerate(frame):
        dct[int(v) + offset] = rms_n[0][i]
    return dct


def wav2anim(path: Path, fps, offset: int = 0) -> str:
    dct = get_wav_data(path, fps, offset)
    return dict2anim(dct)


def to_mm_setting(anim_list) -> str:
    header_text = '''
    {
        Tools = ordered() {
            MouthAnim = PipeRouter {
                CtrlWZoom = false,
                NameSet = true,
                Inputs = {'''
    input_text = '''
                    LayerEnabled%d = Input {
                        SourceOp = "MouthAnimLayerEnabled%d",
                        Source = "Value",
                    },'''
    middle_text = '''
                },
                ViewInfo = OperatorInfo { Pos = { 13365, 115.5 } },
                Colors = { TileColor = { R = 0.92156862745098, G = 0.431372549019608, B = 0 }, }
            },'''
    spline_header_text = '''
            MouthAnimLayerEnabled%d = BezierSpline {
                SplineColor = { Red = 198, Green = 82, Blue = 232 },
                CtrlWZoom = false,
                NameSet = true,
                KeyFrames = {'''
    spline_footer_text = '''
                }
            },'''
    footer_text = '''
        },
    }'''

    layer_max = len(anim_list)
    input_list = []
    spline_list = []
    for i in range(1, layer_max + 1):
        input_list.append(input_text % (i, i))
        spline_list.append('\n'.join([
            spline_header_text % i,
            anim_list[i - 1],
            spline_footer_text
        ]))
    return '\n'.join(
        [header_text] + input_list + [middle_text] + spline_list + [footer_text]
    )


def wav2setting_mm(comp, path: Path, fps, offset: int = 0) -> str:
    tool = comp.FindTool('MouthOpenAnim')
    if tool is None:
        return []
    layer_max = int(tool.GetInput('M_Open', comp.CurrentTime))
    threshold = tool.GetInput('Threshold', comp.CurrentTime)
    # make threshold_list
    threshold_list = list(np.linspace(0.0, threshold, layer_max - 1))
    threshold_list.insert(0, -1.0)  # 最小値は0.0なので、最初は下限なしの意味で-1.0を追加
    threshold_list.append(2.0)  # 最大値は1.0なので、最後は上限なしの意味で2.0を追加
    # get wav data
    dct = get_wav_data(path, fps, offset)
    # make anim
    anim_list = []
    for i in range(1, layer_max + 1):
        _dct = {}
        _sup = threshold_list[i - 1]
        _inf = threshold_list[i]
        for frame in dct.keys():
            if _inf > dct[frame] >= _sup:
                _dct[frame] = 1
            else:
                _dct[frame] = 0
        anim_list.append(_dict2anim_process(_dct))
    # return setting
    return to_mm_setting(anim_list)


if __name__ == '__main__':
    _lab_file = Path(r'C:\work\wave\00120230716164846_琴葉 茜_今は昔、竹取の翁とい.lab')
    p.pipe(
        lab2anim(
            _lab_file,
            30,
            anim.Type.aiueo,
        ),
        print,
    )
    p.pipe(
        lab2anim(
            _lab_file,
            30,
            anim.Type.aiueo2,
        ),
        print,
    )
    p.pipe(
        lab2anim_mm(
            _lab_file,
            30,
            anim.Type.aiueo2,
        ),
        print,
    )
    print(anim.TYPE_LIST)

from collections import OrderedDict
from pathlib import Path
from typing import (
    List,
    Optional,
    Tuple,
)
from rs.core import (
    pipe as p,
)

OTHER = 'other'
TOP = 'top'
BOTTOM = 'bottom'
HAIR = 'hair'
EYEBROW = 'eyebrow'
EYE = 'eye'
MOUTH = 'mouth'
FACE = 'face'
BODY = 'body'

PARTS_DICT = OrderedDict((
    (BODY, '体'),
    (FACE, '顔'),
    (MOUTH, '口'),
    (EYE, '目'),
    (HAIR, '髪'),
    (EYEBROW, '眉'),
    (BOTTOM, '服下'),
    (TOP, '服上'),
    (OTHER, '他'),
))

MULTIPLE_SUFFIX_DICT = OrderedDict([
    ('x', (0, 0)),
    ('z', (None, 0)),
])
MULTIPLE_SUFFIX_LIST = list(MULTIPLE_SUFFIX_DICT.keys())

OFFSET_SUFFIX_DICT = OrderedDict([
    ('-15', (15, 15)),
    ('-10', (10, 10)),
    ('+4m', (None, -4)),
    ('+7m', (None, -7)),
    ('+8m', (None, -8)),
    ('+10m', (None, -10)),
])
OFFSET_SUFFIX_LIST = list(OFFSET_SUFFIX_DICT.keys())


def path_to_dict(path: Path) -> OrderedDict:
    dct = OrderedDict()
    if not path.is_dir():
        return dct
    for f in p.pipe(
            path.iterdir(),
            p.filter(p.call.is_file()),
            p.filter(lambda x: len(x.name) > 2 and x.name[:2].isdigit()),
            p.map(str),
            sorted,
            p.map(Path),
    ):
        f: Path
        key = f.name[:2]
        if key not in dct:
            dct[key] = []
        dct[key].append(f)
    return dct


def get_key_file(lst: List[Path], is_anim=False) -> Tuple[Optional[Path], Optional[Path], Optional[Path]]:
    base_file = lst[0] if len(lst) > 0 else None
    v_file = None
    shadow_file = None
    if is_anim:
        for f in lst:
            s: str = f.name.split('.')[0]
            if s in p.pipe(
                    [''] + MULTIPLE_SUFFIX_LIST + OFFSET_SUFFIX_LIST,
                    p.map(lambda x: s[:2] + x),
                    list,
            ):
                base_file = f
            if s in p.pipe(
                    [''] + MULTIPLE_SUFFIX_LIST + OFFSET_SUFFIX_LIST,
                    p.map(lambda x: s[:2] + 'v' + x),
                    list,
            ):
                v_file = f
    else:
        _base_file = None
        c_file = None
        o_file = None
        for f in lst:
            s: str = f.name.split('.')[0]
            if len(s) == 2:
                _base_file = f
            elif len(s) == 3:
                if s.endswith('c'):
                    c_file = f
                if s.endswith('o'):
                    o_file = f
                if s.endswith('v'):
                    v_file = f
                if s.endswith('s'):
                    shadow_file = f
        if _base_file is None:
            _base_file = o_file
        if _base_file is None:
            _base_file = c_file
        if _base_file is not None:
            base_file = _base_file
    return base_file, v_file, shadow_file


def get_anim_file_list(base_name: str, lst: List[Path]) -> List[Path]:
    is_v = base_name[2] == 'v'
    size = 3 if is_v else 2

    def check(path: Path) -> bool:
        flag = path.name[2] == 'v'
        return flag if is_v else not flag

    return p.pipe(
        lst,
        p.filter(check),
        p.filter(lambda x: len(x.name) > len(base_name)),
        p.filter(lambda x: x.name[size:size + len(x.name) - len(base_name)].isalpha()),
        list,
    )


def make_anim(step: int, lst: List[Path]) -> List[Path]:
    anim_list = []
    tmp_list = lst + list(reversed(lst))[1:]
    for f in tmp_list:
        for i in range(step):
            anim_list.append(f)
    return anim_list


def make_anim02(step: int, idle: int, offset: int, base_file: Path, lst: List[Path]) -> List[Path]:
    anim_list = make_anim(step, lst)
    if len(anim_list) == 0:
        return []
    pre_list = []
    suf_list = []
    for i in range(idle):
        if i < offset:
            pre_list.append(base_file)
        else:
            suf_list.append(base_file)
    return pre_list + anim_list + suf_list


def get_offset(path: Path):
    mouth_offset = None
    eyebrow_offset = None
    s = path.name.split('.')[0]
    for key in OFFSET_SUFFIX_LIST:
        if s.endswith(key):
            mouth_offset, eyebrow_offset = OFFSET_SUFFIX_DICT[key]
    return mouth_offset, eyebrow_offset


def get_blend(path: Path):
    mouth_blend = None
    eyebrow_blend = None
    s = path.name.split('.')[0]
    for key in MULTIPLE_SUFFIX_LIST:
        if s.endswith(key):
            mouth_blend, eyebrow_blend = MULTIPLE_SUFFIX_DICT[key]
    return mouth_blend, eyebrow_blend

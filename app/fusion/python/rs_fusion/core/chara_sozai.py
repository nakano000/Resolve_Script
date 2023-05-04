import json

from rs.core import (
    pipe as p,
)
from rs_fusion.core import ordered_dict_to_dict

OTHER = '他'
HAIR = '髪'
EYEBROW = '眉'
EYE = '目'
MOUTH = '口'
FACE = '顔'
BODY = '体'
ALL = '全'
BACK = '後'
FRONT = '前'


def _connect(comp, xf_list, ld_list):
    for i in range(len(xf_list) - len(ld_list)):
        ld_list.append(ld_list[-1])
    for xf_name, ld_name in zip(xf_list, ld_list):
        xf = comp.FindTool(xf_name)
        if xf is None:
            print('Tool not found: {}'.format(xf_name))
            continue
        ld = comp.FindTool(ld_name)
        if ld is None:
            print('Tool not found: {}'.format(ld_name))
            continue
        xf.ConnectInput('Input', ld)


def _set_for_eye(comp, key, data):
    if data['part'] == EYE:
        xf_list = p.pipe(
            data['xf'][MOUTH] + data['xf'][EYEBROW],
            p.map(lambda x: comp.FindTool(x)),
            list,
        )
        mg_eyebrow = comp.FindTool(data['mg'][EYEBROW])
        mg_mouth = comp.FindTool(data['mg'][MOUTH])

        # -15
        offset = data['offset'] if key.endswith('-15') else 0
        for xf in xf_list:
            xf.Center = [0.5, 0.5 + offset]
        # +眉 +眉口
        mg_eyebrow.SetAttrs({'TOOLB_PassThrough': key.endswith('+眉口') or key.endswith('+眉')})
        mg_mouth.SetAttrs({'TOOLB_PassThrough': key.endswith('+眉口')})


def _set_preview(comp, key, data):
    preview = data['preview']
    xf = comp.FindTool('Root')
    xf.SetInput(preview, key)


def connect(comp, xf_name, key):
    xf = comp.FindTool(xf_name)
    if xf is None:
        return
    json_txt = xf.GetInput('Comments')
    data = json.loads(json_txt)
    part = data['part']
    xf_list: list = data['xf'][part]
    ld_data: dict = data['ld']
    if key not in ld_data.keys():
        return
    ld_list = ld_data[key]
    # main
    _connect(comp, xf_list, ld_list)
    _set_for_eye(comp, key, data)
    _set_preview(comp, key, data)


def prev_next(comp, xf_name: str, is_next=False):
    xf = comp.FindTool(xf_name)
    if xf is None:
        return
    json_txt = xf.GetInput('Comments')
    data = json.loads(json_txt)
    part = data['part']
    xf_list: list = data['xf'][part]
    ld_data: dict = data['ld']
    outp = xf.Input.GetConnectedOutput()
    # find index
    index = 0
    if outp is not None:
        _name = outp.GetTool().Name
        for i, (k, v) in enumerate(ld_data.items()):
            if v[0] == _name:
                index = i
                break
    # set index
    if is_next:
        index = min(index + 1, len(ld_data) - 1)
    else:
        index = max(index - 1, 0)

    # set data
    key, ld_list = list(ld_data.items())[index]
    # main
    _connect(comp, xf_list, ld_list)
    _set_for_eye(comp, key, data)
    _set_preview(comp, key, data)


def set_blink(comp, xf_name):
    tool = comp.FindTool('Root')
    if tool is None:
        return
    blink: int = tool.GetInput('Blink')
    other: int = tool.GetInput('Other')
    close: int = tool.GetInput('Close')

    xf = comp.FindTool(xf_name)
    if xf is None:
        return
    json_txt = xf.GetInput('Comments')
    data = json.loads(json_txt)
    dx_list: list = data['eye_dx']

    header = '''
{
    Tools = ordered() {
        EyeBlink = PipeRouter {
            CtrlWZoom = false,
            Inputs = {
                Mix = Input {
                    SourceOp = "EyeBlink_BackgroundForeground",
                    Source = "Value",
                },
            },
            ViewInfo = OperatorInfo { Pos = { 10285, -940.5 } },
        },
        EyeBlink_BackgroundForeground = BezierSpline {
            SplineColor = { Red = 16, Green = 164, Blue = 235 },
            CtrlWZoom = false,
            NameSet = true,
            KeyFrames = {
                [0] = { 0, Flags = { Linear = true, Loop = true, PreLoop = true } },'''
    key_text = '''
                [%d] = { %d, Flags = { StepIn = true } },'''
    footer = '''
                [%d] = { 0, Flags = { StepIn = true, Loop = true, PreLoop = true } }
            }
        }
    },
    ActiveTool = "EyeBlink"
}
''' % blink

    #
    comp.Lock()
    comp.StartUndo('RS EyeBlink')
    size = len(dx_list)
    sf = 2 * (size - 1) * other + close
    for i, _dx_name in enumerate(dx_list):
        _dx = comp.FindTool(_dx_name)
        if _dx is None:
            continue
        step = i * other
        lst = [header, key_text % (blink - sf + step, 1)]
        if i != 0:
            lst.append(key_text % (blink - step, 0))
        lst.append(footer)

        text = '\n'.join(lst)
        st = ordered_dict_to_dict(bmd.readstring(text))
        _dx.LoadSettings(st)
    comp.EndUndo(True)
    comp.Unlock()

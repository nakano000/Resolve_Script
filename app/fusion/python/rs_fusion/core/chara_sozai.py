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


def _set_for_eye(comp, key, data):
    if data['part'] == EYE:
        xf_list = p.pipe(
            data['xf'][MOUTH] + data['xf'][EYEBROW],
            p.map(comp.FindTool),
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


def _connect(comp, key, data, ld_name_list):
    part = data['part']
    xf_list = p.pipe(
        data['xf'][part],
        p.map(comp.FindTool),
        list,
    )
    ld_list = p.pipe(
        ld_name_list,
        p.map(comp.FindTool),
        list,
    )
    # preview
    root = comp.FindTool('Root')
    preview_param = data['preview']
    # main

    # connect
    _ld = None
    for i, xf in enumerate(xf_list):
        if i < len(ld_list):
            _ld = ld_list[i]
        xf.ConnectInput('Input', _ld)
    # set for eye
    _set_for_eye(comp, key, data)
    # preview
    root.SetInput(preview_param, key, comp.CurrentTime)



def connect(comp, xf_name, key):
    xf = comp.FindTool(xf_name)
    if xf is None:
        return
    json_txt = xf.GetInput('Comments')
    data = json.loads(json_txt)
    ld_data: dict = data['ld']
    if key not in ld_data.keys():
        return
    comp.Lock()
    comp.StartUndo('RS Pose')
    _connect(comp, key, data, ld_data[key])
    comp.EndUndo(True)
    comp.Unlock()


def prev_next(comp, xf_name: str, is_next=False):
    xf = comp.FindTool(xf_name)
    if xf is None:
        return
    json_txt = xf.GetInput('Comments')
    data = json.loads(json_txt)
    ld_data: dict = data['ld']
    outp = xf.Input.GetConnectedOutput()
    # find index
    index = 0
    if outp is not None:
        _name = outp.GetTool().Name
        for i, v in enumerate(ld_data.values()):
            if v[0] == _name:
                index = i
                break
    # set index
    max_index = len(ld_data) - 1
    if is_next:
        index += 1
        if index > max_index:
            index = 0
    else:
        index -= 1
        if index < 0:
            index = max_index

    # set data
    key, ld_name_list = list(ld_data.items())[index]
    comp.Lock()
    comp.StartUndo('RS Pose')
    _connect(comp, key, data, ld_name_list)
    comp.EndUndo(True)
    comp.Unlock()


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

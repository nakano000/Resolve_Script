from pathlib import Path
from collections import OrderedDict
import random

from PySide2.QtWidgets import QFileDialog
from rs.core import (
    pipe as p,
)


def loader(comp, use_post_multiply=False):
    flow = comp.CurrentFrame.FlowView
    _x = -32768  # 自動的に配置する
    _y = -32768

    # Files
    urls, _ = QFileDialog.getOpenFileNames(
        caption="画像選択",
        filter="music(*.dpx *.exr *.j2c *.jpg *.png *.tga *.tif)")
    if not urls:
        return

    # undo
    comp.Lock()
    comp.StartUndo('RS Loader')

    # deselect
    flow.Select()

    # import
    for url in urls:
        node = comp.AddTool('Loader', _x, _y)
        if _x == -32768:
            _x, _y = flow.GetPosTable(node).values()
            _x = int(_x)
            _y = int(_y)
            flow.SetPos(node, _x, _y)
        node.Clip[1] = comp.ReverseMapPath(url.replace('/', '\\'))
        node.Loop[1] = 1
        node.PostMultiplyByAlpha = 1 if use_post_multiply else 0
        node.GlobalIn = -1000
        node.GlobalOut = -1000

        flow.Select(node)
        _x += 1

    # end
    comp.EndUndo(True)
    comp.Unlock()


def merge(comp):
    # tools
    tools = list(comp.GetToolList(True).values())
    if len(tools) < 2:
        return

    flow = comp.CurrentFrame.FlowView
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])

    # undo
    comp.Lock()
    comp.StartUndo('RS Marge')

    pre_node = None

    flow.Select()
    for tool in tools:
        if pre_node is None:
            pre_node = tool
            continue
        _x, _y = flow.GetPosTable(tool).values()
        mg = comp.AddTool('Merge', round(_x), round(_y) + 4)
        mg.ConnectInput('Foreground', tool)
        mg.ConnectInput('Background', pre_node)
        pre_node = mg
        flow.Select(mg)
    # end
    comp.EndUndo(True)
    comp.Unlock()


def insert(comp, node_id):
    # tools
    tools = list(comp.GetToolList(True).values())
    if len(tools) < 1:
        return

    flow = comp.CurrentFrame.FlowView
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])

    # undo
    comp.Lock()
    comp.StartUndo('RS Insert')

    flow.Select()
    for tool in tools:
        _x, _y = flow.GetPosTable(tool).values()
        node = comp.AddTool(node_id, round(_x), round(_y) + 4)
        flow.Select(node)
        outp = tool.FindMainOutput(1)
        if outp is None:
            continue
        inp = node.FindMainInput(1)
        if inp is None:
            continue
        inp.ConnectTo(tool.Output)
        inputs = outp.GetConnectedInputs()
        for i in inputs.values():
            i.ConnectTo(node.Output)
        # end
    comp.EndUndo(True)
    comp.Unlock()


def get_modifiers(tool, param_list=None):
    modifiers = {}
    for inp in tool.GetInputList().values():
        if param_list is not None and inp.ID not in param_list:
            continue
        outp = inp.GetConnectedOutput()
        if outp is None:
            continue
        x = outp.GetTool()
        if x.GetAttrs()['TOOLB_Visible']:
            continue
        modifiers[x.Name] = x
        modifiers.update(get_modifiers(x))
    return modifiers


def ordered_dict_to_dict(org_dict):
    dct = dict(org_dict)
    for k, v in dct.items():
        if isinstance(v, dict):
            dct[k] = ordered_dict_to_dict(v)
    if isinstance(org_dict, OrderedDict):
        dct['__flags'] = 2097152
    return dct


def copy(comp, src_tool_name, param_list=None, sift_step=0, jitter_inf=0, jitter_sup=0):
    # tools
    src_tool = comp.FindTool(src_tool_name)
    if src_tool is None:
        return
    tools = list(comp.GetToolList(True, src_tool.ID).values())
    if len(tools) < 1:
        return

    flow = comp.CurrentFrame.FlowView
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[1])
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])

    comp.Lock()
    comp.StartUndo('RS Copy Param')
    # main
    cnt = 0
    for tool in tools:
        modifiers = get_modifiers(src_tool, param_list)
        st = ordered_dict_to_dict(src_tool.SaveSettings())

        # animation shift
        splines = []
        for modifier in modifiers.values():
            if modifier.ID == 'BezierSpline':
                splines.append(modifier.Name)
        for node in st['Tools'].keys():
            if node in splines:
                keys = st['Tools'][node]['KeyFrames']
                new_keys = {}
                jitter = random.randint(jitter_inf, jitter_sup)
                frame_offset = cnt * sift_step + jitter
                for frame in keys:
                    key = keys[frame]
                    if 'RH' in key.keys():
                        key['RH'][1] += frame_offset
                    if 'LH' in key.keys():
                        key['LH'][1] += frame_offset
                    new_keys[frame + frame_offset] = keys[frame]
                st['Tools'][node]['KeyFrames'] = new_keys
        cnt += 1

        # all param
        if param_list is None:
            # apply
            tool.LoadSettings(st)
            continue

        # selected param
        dst_st = ordered_dict_to_dict(tool.SaveSettings())
        # set param
        for param in param_list:
            if param in st['Tools'][src_tool.Name]['Inputs']:
                dst_st['Tools'][tool.Name]['Inputs'][param] = st['Tools'][src_tool.Name]['Inputs'][param]
            else:
                dst_st['Tools'][tool.Name]['Inputs'].pop(param, None)
        # set modifiers
        for other in st['Tools'].keys():
            if other in modifiers.keys():
                dst_st['Tools'][other] = st['Tools'][other]
        # apply
        tool.LoadSettings(dst_st)

    comp.EndUndo(True)
    comp.Unlock()


def background(comp, padding_x=0, padding_y=0, is_square=False):
    # tools
    tools = list(comp.GetToolList(True).values())
    if len(tools) < 1:
        return

    flow = comp.CurrentFrame.FlowView
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])

    x_attr = 'TOOLI_ImageWidth'
    y_attr = 'TOOLI_ImageHeight'
    comp_x = comp.GetPrefs("Comp.FrameFormat.Width")
    comp_y = comp.GetPrefs("Comp.FrameFormat.Height")

    # undo
    comp.Lock()
    comp.StartUndo('RS BG')

    flow.Select()
    for tool in tools:
        _x, _y = flow.GetPosTable(tool).values()
        # add
        mask = comp.AddTool('RectangleMask', round(_x) - 2, round(_y) + 4)
        bg = comp.AddTool('Background', round(_x) - 1, round(_y) + 4)
        mg = comp.AddTool('Merge', round(_x), round(_y) + 4)
        flow.Select(mask)
        flow.Select(bg)
        flow.Select(mg)

        # connect
        outp = tool.FindMainOutput(1)
        if outp is not None:
            inputs = outp.GetConnectedInputs()
            for i in inputs.values():
                i.ConnectTo(mg.Output)

        mg.ConnectInput('Foreground', tool)
        mg.ConnectInput('Background', bg)
        bg.ConnectInput('EffectMask', mask)

        # set param
        attrs = tool.GetAttrs()
        if x_attr not in attrs.keys() or y_attr not in attrs.keys():
            continue
        x_size = attrs[x_attr]
        y_size = attrs[y_attr]
        if None in (outp, x_size, y_size):
            continue
        bg.UseFrameFormatSettings = int(comp_x == x_size and comp_y == y_size)
        bg.Width = x_size
        bg.Height = y_size
        dod = outp.GetDoD()
        if dod is None:
            dod = {1: 0, 2: 0, 3: x_size, 4: y_size}
        mask.Center = {
            1: (dod[1] + dod[3]) / (2 * x_size),
            2: (dod[2] + dod[4]) / (2 * y_size),
        }
        _w = dod[3] - dod[1] + (padding_x * 2)
        _h = dod[4] - dod[2] + (padding_y * 2)
        if is_square:
            _w = max(_w, _h)
            _h = _w
        mask.Width = _w / x_size
        mask.Height = _h / y_size
    comp.EndUndo(True)
    comp.Unlock()


def apply_color(comp, color_list, is_random=False):
    # tools
    tools = list(comp.GetToolList(True).values())
    if len(tools) < 1:
        return

    flow = comp.CurrentFrame.FlowView
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[1])
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])
    if is_random:
        random.shuffle(tools)

    color_attrs = [
        ['TopLeftRed', 'TopLeftGreen', 'TopLeftBlue'],
        ['Red1', 'Green1', 'Blue1'],
        ['Red', 'Green', 'Blue'],
    ]

    # undo
    comp.Lock()
    comp.StartUndo('RS Color')

    cnt = 0
    for tool in tools:
        color_attr = None
        for c in color_attrs:
            if tool.GetInput(c[0], comp.CurrentTime) is not None:
                color_attr = c
                break
        if color_attr is None:
            continue
        color = color_list[cnt % len(color_list)]
        for i in range(3):
            tool.SetInput(color_attr[i], color[i], comp.CurrentTime)

        cnt += 1
    comp.EndUndo(True)
    comp.Unlock()


if __name__ == '__main__':
    # print(isinstance(OrderedDict(), dict))
    # print(isinstance({}, OrderedDict))
    pass

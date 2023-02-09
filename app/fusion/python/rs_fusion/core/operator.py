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
    # for n in comp.GetToolList(False):
    #     flow.Select(n, False)

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


if __name__ == '__main__':
    # print(isinstance(OrderedDict(), dict))
    # print(isinstance({}, OrderedDict))
    pass

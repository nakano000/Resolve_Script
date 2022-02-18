from pathlib import Path
from typing import List

from rs.core import (
    chara_sozai as cs,
)


def set_pref(comp, name, fps):
    comp.SetPrefs({
        "Comp.FrameFormat.Name": name,
        "Comp.FrameFormat.Width": 1920,
        "Comp.FrameFormat.Height": 1080,
        "Comp.FrameFormat.AspectX": 1.0,
        "Comp.FrameFormat.AspectY": 1.0,
        "Comp.FrameFormat.GuideRatio": float(1920) / float(1080),
        "Comp.FrameFormat.Rate": fps,
        "Comp.FrameFormat.DepthInteractive": 2,  # 16 bits Float
        "Comp.FrameFormat.DepthFull": 2,  # 16 bits Float
        "Comp.FrameFormat.DepthPreview": 2  # 16 bits Float
    })


def get_uc(name, min_v, max_v, center=None):
    v = -1 if name == cs.OTHER else 0
    dct = {
        'LINKS_Name': name,
        'LINKID_DataType': "Number",
        'INPID_InputControl': "SliderControl",
        'INP_Default': v,
        'INP_Integer': True,
        'INP_MinScale': min_v,
        'INP_MaxScale': max_v,
        'INP_MinAllowed': min_v,
        'INP_MaxAllowed': max_v,
        'ICS_ControlPage': "Controls",
    }
    if center is not None:
        dct['ICD_Center'] = center
    return dct


def make_setting_file(base: str, uc_list):
    header_text = '\n'.join([
        '{',
        'Tools = ordered() {',
        'RigTool = GroupOperator {',
        'Inputs = ordered() {',
    ])
    uc_text = '\n'.join([
        'Input%d = InstanceInput {',
        'SourceOp = "Ctrl_Transform",',
        'Source = "%s",',
        'Page = "Controls",',
        'Default = 0,',
        '},'
    ])
    mid_text = '\n'.join([
        '},',
        'Outputs = {',
        'MainOutput1 = InstanceOutput {',
        'SourceOp = "Ctrl_Transform",',
        'Source = "Output",',
        '}'
        '},'
        'ViewInfo = GroupInfo { Pos = { 0, 0 } },'
    ])
    footer_text = '\n'.join([
        '}'
        '},'
        'ActiveTool = "RigTool"'
        '}'
    ])
    setting_list: List[str] = [header_text]
    for i in range(len(uc_list)):
        setting_list.append(uc_text % (i + 1, uc_list[i]))
    setting_list.append(mid_text)
    setting_list.append('\n'.join(base.split('\n')[1:-1]))
    setting_list.append(footer_text)
    return '\n'.join(setting_list)


def add_ld(comp, x_pos, y_pos, path: Path):
    ld = comp.AddTool('Loader', x_pos, y_pos)
    ld.Clip[1] = str(path)
    ld.Loop[1] = 1
    # ss = path.name.split('.')[0]
    # ld.SetAttrs({'TOOLS_Name': '%s_%s' % (ss[1], ss[0])})
    return ld


def make_offset_expression(lst):
    header_text = '\n'.join([
        ':x = 0.5;',
        'dy = 1.0 / self.Input.Height;',
        'v = Ctrl_Transform.eye;',
    ])
    if_text = '\n'.join([
        'if v == %d then;',
        'y = 0.5 + dy * (%d);',
    ])
    elseif_text = '\n'.join([
        'elseif v == %d then;',
        'y = 0.5 + dy * (%d);',
    ])
    footer_text = '\n'.join([
        'else;'
        'y = 0.5;'
        'end;'
        'return Point(x,y)'
    ])
    exp: List[str] = [header_text]
    for i in range(len(lst)):
        base_text = elseif_text
        if i == 0:
            base_text = if_text
        exp.append(base_text % lst[i])
    exp.append(footer_text)

    return '\n'.join(exp)


def make_blend_expression(lst):
    header_text = '\n'.join([
        ':v = Ctrl_Transform.eye;',
    ])
    if_text = '\n'.join([
        'if v == %d then;',
        't = %d;',
    ])
    elseif_text = '\n'.join([
        'elseif v == %d then;',
        't = %d;',
    ])
    footer_text = '\n'.join([
        'else;'
        't = 1;'
        'end;'
        'return t'
    ])
    exp: List[str] = [header_text]
    for i in range(len(lst)):
        base_text = elseif_text
        if i == 0:
            base_text = if_text
        exp.append(base_text % lst[i])
    exp.append(footer_text)

    return '\n'.join(exp)


def copy_all_nodes(comp):
    flow = comp.CurrentFrame.FlowView
    tool_list = comp.GetToolList()
    for key in tool_list:
        flow.Select(tool_list[key])
    comp.Copy()

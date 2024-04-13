import decimal
import enum
import random

from PySide6.QtWidgets import QFileDialog

from rs.core import (
    pipe as p,
)
from rs_fusion.core import ordered_dict_to_dict


def to_int(value):
    return int(decimal.Decimal(str(value)).quantize(decimal.Decimal('0'), rounding=decimal.ROUND_HALF_UP))


def get_tools(comp, min_size, is_random=False, is_reverse=False):
    tools = list(comp.GetToolList(True).values())
    if len(tools) < min_size:
        return None
    flow = comp.CurrentFrame.FlowView
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[1])
    tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])
    if is_random:
        random.shuffle(tools)
    if is_reverse:
        tools.reverse()
    return tools


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
            _x = to_int(_x)
            _y = to_int(_y)
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
    tools = get_tools(comp, 2, False)
    if tools is None:
        return

    flow = comp.CurrentFrame.FlowView

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
        mg = comp.AddTool('Merge', to_int(_x), to_int(_y) + 4)
        mg.ConnectInput('Foreground', tool)
        mg.ConnectInput('Background', pre_node)
        pre_node = mg
        flow.Select(mg)
    # end
    comp.EndUndo(True)
    comp.Unlock()


def get_main_input(tool, out_data_type):
    attr_filter = [out_data_type]
    if out_data_type == 'Image':
        attr_filter.append('MtlGraph3D')

    i = 1
    while True:
        inp = tool.FindMainInput(i)
        if inp is None:
            break
        in_data_type = inp.GetAttrs()['INPS_DataType']
        if in_data_type in attr_filter:
            return inp
        i += 1
    return tool.FindMainInput(1)


def insert(comp, node_id):
    tools = get_tools(comp, 1, False)
    if tools is None:
        return

    flow = comp.CurrentFrame.FlowView

    # undo
    comp.Lock()
    comp.StartUndo('RS Insert')

    flow.Select()
    for tool in tools:
        _x, _y = flow.GetPosTable(tool).values()
        node = comp.AddTool(node_id, to_int(_x), to_int(_y) + 4)
        flow.Select(node)
        outp = tool.FindMainOutput(1)
        if outp is None:
            continue
        out_data_type = outp.GetAttrs()['OUTS_DataType']
        inp = get_main_input(node, out_data_type)
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


def copy(
        comp,
        src_tool_name,
        param_list=None,
        offset=0, sift_step=0,
        jitter_inf=0,
        jitter_sup=0,
        is_random=False,
        is_reverse=False
):
    # tools
    src_tool = comp.FindTool(src_tool_name)
    if src_tool is None:
        return
    tools = get_tools(comp, 1, is_random, is_reverse)
    if tools is None:
        return

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
                frame_offset = cnt * sift_step + jitter + offset
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


def paste_setting(comp, text, param_list):
    tools = get_tools(comp, 1, False)
    if tools is None:
        return
    _st = ordered_dict_to_dict(bmd.readstring(text))
    if _st is None:
        return
    if 'Tools' not in _st.keys():
        return
    src_name = None
    for k in _st['Tools'].keys():
        if type(_st['Tools'][k]) == dict and 'Inputs' in _st['Tools'][k].keys():
            src_name = k
            break
    if src_name is None:
        return

    comp.Lock()
    comp.StartUndo('RS Paste Setting')
    # main
    for tool in tools:
        st = ordered_dict_to_dict(bmd.readstring(text))

        dst_st = ordered_dict_to_dict(tool.SaveSettings())
        # set param
        for param in param_list:
            if param in dst_st['Tools'][tool.Name]['Inputs']:
                st['Tools'][src_name]['Inputs'][param] = dst_st['Tools'][tool.Name]['Inputs'][param]
            else:
                st['Tools'][src_name]['Inputs'].pop(param, None)

        if tool.ID not in ['GroupOperator', 'MacroOperator']:
            tool = tool.Refresh()
        tool.LoadSettings(st)

    comp.EndUndo(True)
    comp.Unlock()


def background(comp, padding_x=0, padding_y=0, is_square=False):
    tools = get_tools(comp, 1, False)
    if tools is None:
        return

    flow = comp.CurrentFrame.FlowView

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
    tools = get_tools(comp, 1, is_random)
    if tools is None:
        return

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


def apply_font(comp, font_name, font_style):
    tools = get_tools(comp, 1, False)
    if tools is None:
        return

    # undo
    comp.Lock()
    comp.StartUndo('RS Font')

    for tool in tools:
        if tool.ID not in ['TextPlus', 'Text3D']:
            continue

        tool.SetInput('Font', font_name, comp.CurrentTime)
        tool.SetInput('Style', font_style, comp.CurrentTime)

    comp.EndUndo(True)
    comp.Unlock()


class AlignType(enum.Enum):
    L = 0
    C = 1
    R = 2


class AlignType2D(enum.Enum):
    L = 0
    VC = 1
    R = 2
    T = 3
    HC = 4
    B = 5


def align(comp, attr_id: str, align_type: AlignType):
    tools = get_tools(comp, 2, False)
    if tools is None:
        return
    # get range
    min_v = max_v = None
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        if min_v is None:
            min_v = max_v = _v
        min_v = min(min_v, _v)
        max_v = max(max_v, _v)

    # main
    comp.Lock()
    comp.StartUndo('RS Align')
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue

        if align_type == AlignType.L:
            tool.SetInput(attr_id, min_v, comp.CurrentTime)
        elif align_type == AlignType.R:
            tool.SetInput(attr_id, max_v, comp.CurrentTime)
        elif align_type == AlignType.C:
            tool.SetInput(attr_id, (min_v + max_v) / 2, comp.CurrentTime)
    comp.EndUndo(True)
    comp.Unlock()


def align2d(comp, attr_id: str, align_type: AlignType2D, use_canvas=False):
    tools = get_tools(comp, 2, False)
    if tools is None:
        return

    # get range
    min_x = min_y = max_x = max_y = None
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        if min_x is None:
            min_x = _v[1]
            min_y = _v[2]
            max_x = _v[1]
            max_y = _v[2]
        min_x = min(min_x, _v[1])
        min_y = min(min_y, _v[2])
        max_x = max(max_x, _v[1])
        max_y = max(max_y, _v[2])

    if use_canvas:
        min_x = 0.0
        min_y = 0.0
        max_x = 1.0
        max_y = 1.0
    # main
    comp.Lock()
    comp.StartUndo('RS Align')
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue

        if align_type == AlignType2D.L:
            tool.SetInput(attr_id, {
                1: min_x,
                2: _v[2],
            }, comp.CurrentTime)
        elif align_type == AlignType2D.R:
            tool.SetInput(attr_id, {
                1: max_x,
                2: _v[2],
            }, comp.CurrentTime)
        elif align_type == AlignType2D.T:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: max_y,
            }, comp.CurrentTime)
        elif align_type == AlignType2D.B:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: min_y,
            }, comp.CurrentTime)
        elif align_type == AlignType2D.VC:
            tool.SetInput(attr_id, {
                1: (min_x + max_x) / 2,
                2: _v[2],
            }, comp.CurrentTime)
        elif align_type == AlignType2D.HC:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: (min_y + max_y) / 2,
            }, comp.CurrentTime)
    comp.EndUndo(True)
    comp.Unlock()


def align_dod(fusion, comp, attr_id: str, align_type: AlignType2D, use_canvas=False):
    tools = get_tools(comp, 2, False)
    if tools is None:
        return

    x_attr = 'TOOLI_ImageWidth'
    y_attr = 'TOOLI_ImageHeight'
    mask_list = p.pipe(
        fusion.GetRegList(fusion.CT_Mask).values(),
        p.map(lambda x: x.ID),
        list
    )
    # get range
    min_x = min_y = max_x = max_y = None
    data = []
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        attrs = tool.GetAttrs()
        if x_attr not in attrs.keys() or y_attr not in attrs.keys():
            continue
        x_size = attrs[x_attr]
        y_size = attrs[y_attr]
        if None in (x_size, y_size):
            continue

        if tool.ID in mask_list:
            outp = tool.FindMainOutput(1)
            if outp is None:
                continue

            dod = outp.GetDoD()
            if dod is None:
                continue
            dod[1] = dod[1] / x_size - (_v[1] - 0.5)
            dod[2] = dod[2] / y_size - (_v[2] - 0.5)
            dod[3] = dod[3] / x_size - (_v[1] - 0.5)
            dod[4] = dod[4] / y_size - (_v[2] - 0.5)
        else:
            inp = tool.FindMainInput(1)
            if tool.ID == 'Merge':
                inp = tool.Foreground
            if inp is None:
                continue
            outp = inp.GetConnectedOutput()
            if outp is None:
                continue

            dod = outp.GetDoD()
            if dod is None:
                continue
            dod[1] = dod[1] / x_size
            dod[2] = dod[2] / y_size
            dod[3] = dod[3] / x_size
            dod[4] = dod[4] / y_size

        if min_x is None:
            min_x = dod[1] + _v[1] - 0.5
            min_y = dod[2] + _v[2] - 0.5
            max_x = dod[3] + _v[1] - 0.5
            max_y = dod[4] + _v[2] - 0.5
        min_x = min(min_x, dod[1] + _v[1] - 0.5)
        min_y = min(min_y, dod[2] + _v[2] - 0.5)
        max_x = max(max_x, dod[3] + _v[1] - 0.5)
        max_y = max(max_y, dod[4] + _v[2] - 0.5)
        data.append({
            'tool': tool,
            'dod': dod,
            'value': _v,
        })

    if len(data) < 2:
        return

    if use_canvas:
        min_x = 0.0
        min_y = 0.0
        max_x = 1.0
        max_y = 1.0
    # main
    comp.Lock()
    comp.StartUndo('RS Align')
    for d in data:
        tool = d['tool']
        dod = d['dod']
        _v = d['value']

        if align_type == AlignType2D.L:
            tool.SetInput(attr_id, {
                1: min_x - dod[1] + 0.5,
                2: _v[2],
            }, comp.CurrentTime)
        elif align_type == AlignType2D.R:
            tool.SetInput(attr_id, {
                1: max_x - dod[3] + 0.5,
                2: _v[2],
            }, comp.CurrentTime)
        elif align_type == AlignType2D.T:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: max_y - dod[4] + 0.5,
            }, comp.CurrentTime)
        elif align_type == AlignType2D.B:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: min_y - dod[2] + 0.5,
            }, comp.CurrentTime)
        elif align_type == AlignType2D.VC:
            tool.SetInput(attr_id, {
                1: (min_x + max_x - (dod[1] + dod[3])) / 2 + 0.5,
                2: _v[2],
            }, comp.CurrentTime)
        elif align_type == AlignType2D.HC:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: (min_y + max_y - (dod[2] + dod[4])) / 2 + 0.5,
            }, comp.CurrentTime)
    comp.EndUndo(True)
    comp.Unlock()


def distribute(comp, attr_id: str, is_random=False, is_reverse=False):
    tools = get_tools(comp, 3, is_random, is_reverse)
    if tools is None:
        return

    # get range
    min_v = max_v = None
    cnt = 0  # 有効なノードの数
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        if min_v is None:
            min_v = max_v = _v
        min_v = min(min_v, _v)
        max_v = max(max_v, _v)
        cnt += 1

    # undo
    comp.Lock()
    comp.StartUndo('RS Distribute')
    step = (max_v - min_v) / (cnt - 1)
    offset = 0
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        tool.SetInput(attr_id, min_v + offset, comp.CurrentTime)
        offset += step

    comp.EndUndo(True)
    comp.Unlock()


def distribute2d(
        comp,
        attr_id: str,
        is_x=True,
        is_random=False,
        is_reverse=False,
        use_canvas=False,
):
    tools = get_tools(comp, 3, is_random, is_reverse)
    if tools is None:
        return

    # get range
    min_x = min_y = max_x = max_y = None
    cnt = 0  # 有効なノードの数
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        if min_x is None:
            min_x = _v[1]
            min_y = _v[2]
            max_x = _v[1]
            max_y = _v[2]
        min_x = min(min_x, _v[1])
        min_y = min(min_y, _v[2])
        max_x = max(max_x, _v[1])
        max_y = max(max_y, _v[2])
        cnt += 1

    if use_canvas:
        min_x = 0.0
        min_y = 0.0
        max_x = 1.0
        max_y = 1.0
    # main
    comp.Lock()
    comp.StartUndo('RS Distribute')
    x_step = (max_x - min_x) / (cnt - 1)
    y_step = (max_y - min_y) / (cnt - 1)
    offset = 0
    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue

        if is_x:
            tool.SetInput(attr_id, {
                1: min_x + offset,
                2: _v[2],
            }, comp.CurrentTime)
            offset += x_step
        else:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: min_y + offset,
            }, comp.CurrentTime)
            offset += y_step

    comp.EndUndo(True)
    comp.Unlock()


def distribute_dod(
        fusion,
        comp,
        attr_id: str,
        is_x=True,
        is_random=False,
        is_reverse=False,
        use_canvas=False,
):
    tools = get_tools(comp, 3, is_random, is_reverse)
    if tools is None:
        return

    x_attr = 'TOOLI_ImageWidth'
    y_attr = 'TOOLI_ImageHeight'
    mask_list = p.pipe(
        fusion.GetRegList(fusion.CT_Mask).values(),
        p.map(lambda x: x.ID),
        list
    )
    # get range
    min_x = min_y = max_x = max_y = None
    data = []
    length_x = 0
    length_y = 0

    for tool in tools:
        _v = tool.GetInput(attr_id, comp.CurrentTime)
        if _v is None:
            continue
        attrs = tool.GetAttrs()
        if x_attr not in attrs.keys() or y_attr not in attrs.keys():
            continue
        x_size = attrs[x_attr]
        y_size = attrs[y_attr]
        if None in (x_size, y_size):
            continue

        if tool.ID in mask_list:
            outp = tool.FindMainOutput(1)
            if outp is None:
                continue

            dod = outp.GetDoD()
            if dod is None:
                continue
            dod[1] = dod[1] / x_size - (_v[1] - 0.5)
            dod[2] = dod[2] / y_size - (_v[2] - 0.5)
            dod[3] = dod[3] / x_size - (_v[1] - 0.5)
            dod[4] = dod[4] / y_size - (_v[2] - 0.5)
        else:
            inp = tool.FindMainInput(1)
            if tool.ID == 'Merge':
                inp = tool.Foreground
            if inp is None:
                continue
            outp = inp.GetConnectedOutput()
            if outp is None:
                continue

            dod = outp.GetDoD()
            if dod is None:
                continue
            dod[1] = dod[1] / x_size
            dod[2] = dod[2] / y_size
            dod[3] = dod[3] / x_size
            dod[4] = dod[4] / y_size
        if min_x is None:
            min_x = dod[1] + _v[1] - 0.5
            min_y = dod[2] + _v[2] - 0.5
            max_x = dod[3] + _v[1] - 0.5
            max_y = dod[4] + _v[2] - 0.5
        min_x = min(min_x, dod[1] + _v[1] - 0.5)
        min_y = min(min_y, dod[2] + _v[2] - 0.5)
        max_x = max(max_x, dod[3] + _v[1] - 0.5)
        max_y = max(max_y, dod[4] + _v[2] - 0.5)
        data.append({
            'tool': tool,
            'dod': dod,
            'value': _v,
        })
        length_x += dod[3] - dod[1]
        length_y += dod[4] - dod[2]

    if len(data) < 3:
        return

    if use_canvas:
        min_x = 0.0
        min_y = 0.0
        max_x = 1.0
        max_y = 1.0
    # main
    comp.Lock()
    comp.StartUndo('RS Distribute')
    x_step = ((max_x - min_x) - length_x) / (len(data) - 1)
    y_step = ((max_y - min_y) - length_y) / (len(data) - 1)
    offset_x = min_x
    offset_y = min_y

    for d in data:
        tool = d['tool']
        dod = d['dod']
        _v = d['value']

        if is_x:
            tool.SetInput(attr_id, {
                1: offset_x - dod[1] + 0.5,
                2: _v[2],
            }, comp.CurrentTime)
            offset_x += (dod[3] - dod[1]) + x_step
        else:
            tool.SetInput(attr_id, {
                1: _v[1],
                2: offset_y - dod[2] + 0.5,
            }, comp.CurrentTime)
            offset_y += (dod[4] - dod[2]) + y_step

    comp.EndUndo(True)
    comp.Unlock()


def get_frame_by_index(tool, attr_id: str, index: int):
    target_time = None
    x = tool.GetInputList().values()
    for inp in x:
        if inp.GetAttrs()['INPS_ID'] == attr_id:
            outp = inp.GetConnectedOutput()
            if outp is None:
                continue
            x = outp.GetTool()
            if x.ID == 'BezierSpline':
                _frames = list(x.GetKeyFrames().keys())
                key_frames = {}
                for i, frame in enumerate(_frames):
                    key_frames[i + 1] = frame
                if index in key_frames:
                    target_time = key_frames[index]
            elif x.ID == 'PolyPath':
                target_time = get_frame_by_index(x, 'Displacement', index)
            break

    return target_time


def tools2modifiers(tools, attr_id: str):
    modifiers = []
    for tool in tools:
        x = tool.GetInputList().values()
        for inp in x:
            if inp.GetAttrs()['INPS_ID'] == attr_id:
                outp = inp.GetConnectedOutput()
                if outp is None:
                    continue
                modifiers.append(outp.GetTool())
    return modifiers


def set_value(
        comp, attr_id: str,
        value, step,
        modi_attr_id=None,
        is_abs=True, is_random=False, is_reverse=False,
        use_key=False, key_index=1,
):
    tools = get_tools(comp, 1, is_random, is_reverse)
    if tools is None:
        return

    # modifiers
    if modi_attr_id is not None:
        tools = tools2modifiers(tools, attr_id)
        if tools is None:
            return
        attr_id = modi_attr_id

    comp.Lock()
    comp.StartUndo('RS Set Value')
    offset = 0
    for tool in tools:
        target_frame = comp.CurrentTime if not use_key else get_frame_by_index(tool, attr_id, key_index)
        if target_frame is None:
            continue
        _v = tool.GetInput(attr_id, target_frame)
        if _v is None:
            continue
        _value = value + offset
        if not is_abs:
            _value += _v

        tool.SetInput(attr_id, _value, target_frame)
        offset += step
    comp.EndUndo(True)
    comp.Unlock()


def set_value2d(
        comp, attr_id: str,
        x, y,
        x_step, y_step,
        lock_x=False, lock_y=False,
        is_abs=True, is_random=False, is_reverse=False,
        use_key=False, key_index=1,
):
    tools = get_tools(comp, 1, is_random, is_reverse)
    if tools is None:
        return
    comp.Lock()
    comp.StartUndo('RS Set Value')
    x_offset = 0
    y_offset = 0
    for tool in tools:
        target_frame = comp.CurrentTime if not use_key else get_frame_by_index(tool, attr_id, key_index)
        if target_frame is None:
            continue
        _v = tool.GetInput(attr_id, target_frame)
        if _v is None:
            continue
        if lock_x:
            _x = _v[1]
        else:
            _x = x + x_offset
            if not is_abs:
                _x += _v[1]
        if lock_y:
            _y = _v[2]
        else:
            _y = y + y_offset
            if not is_abs:
                _y += _v[2]

        tool.SetInput(attr_id, {
            1: _x,
            2: _y,
        }, target_frame)
        x_offset += x_step
        y_offset += y_step

    comp.EndUndo(True)
    comp.Unlock()


def random_value(
        comp, attr_id: str,
        inf, sup,
        modi_attr_id=None,
        is_abs=True, is_random=False,
        use_key=False, key_index=1,
):
    tools = get_tools(comp, 1, is_random)
    if tools is None:
        return
    # modifiers
    if modi_attr_id is not None:
        tools = tools2modifiers(tools, attr_id)
        if tools is None:
            return
        attr_id = modi_attr_id

    comp.Lock()
    comp.StartUndo('RS Random Value')
    for tool in tools:
        target_frame = comp.CurrentTime if not use_key else get_frame_by_index(tool, attr_id, key_index)
        if target_frame is None:
            continue
        _v = tool.GetInput(attr_id, target_frame)
        if _v is None:
            continue
        _value = random.uniform(inf, sup)
        if not is_abs:
            _value += _v

        tool.SetInput(attr_id, _value, target_frame)
    comp.EndUndo(True)
    comp.Unlock()


def random_value2d(
        comp, attr_id: str,
        x_inf, y_inf, x_suo, y_sup,
        lock_x=False, lock_y=False,
        is_abs=True, is_random=False,
        use_key=False, key_index=1,
):
    tools = get_tools(comp, 1, is_random)
    if tools is None:
        return
    comp.Lock()
    comp.StartUndo('RS Random Value')
    for tool in tools:
        target_frame = comp.CurrentTime if not use_key else get_frame_by_index(tool, attr_id, key_index)
        if target_frame is None:
            continue
        _v = tool.GetInput(attr_id, target_frame)
        if _v is None:
            continue
        if lock_x:
            _x = _v[1]
        else:
            _x = random.uniform(x_inf, x_suo)
            if not is_abs:
                _x += _v[1]
        if lock_y:
            _y = _v[2]
        else:
            _y = random.uniform(y_inf, y_sup)
            if not is_abs:
                _y += _v[2]

        tool.SetInput(attr_id, {
            1: _x,
            2: _y,
        }, target_frame)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == '__main__':
    pass

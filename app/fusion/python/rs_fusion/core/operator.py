from PySide2.QtWidgets import QFileDialog


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
    for n in comp.GetToolList(False):
        flow.Select(n, False)

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

    for tool in tools:
        if pre_node is None:
            pre_node = tool
            continue
        _x, _y = flow.GetPosTable(tool).values()
        mg = comp.AddTool('Merge', round(_x), round(_y) + 4)
        mg.ConnectInput('Foreground', tool)
        mg.ConnectInput('Background', pre_node)
        pre_node = mg
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
    for tool in tools:
        _x, _y = flow.GetPosTable(tool).values()
        node = comp.AddTool(node_id, round(_x), round(_y) + 4)
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

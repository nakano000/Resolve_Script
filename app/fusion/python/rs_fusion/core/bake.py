from rs_fusion.core import ordered_dict_to_dict


# data = {'tool_name': ['param1', 'param2', 'param3', ... ], ...}
def apply(comp, data: dict, sf: int, ef: int):
    header = '''
{
    Tools = ordered() {
'''
    bake_header = '''
        Bake = PipeRouter {
            CtrlWZoom = false,
            Inputs = {
'''
    input_body = '''
                %s = Input {
                    SourceOp = "BAKE_%s_%s",
                    Source = "Value",
                },
'''
    bake_footer = '''
            },
            ViewInfo = OperatorInfo { Pos = { 10285, -940.5 } },
        },
'''
    spline_header = '''
        ["BAKE_%s_%s"] = BezierSpline {
            CtrlWZoom = false,
            NameSet = true,
            KeyFrames = {
'''
    key_body = '''
                [%d] = { %f, Flags = { Linear = true } },
    '''
    spline_footer = '''
            }
        },
'''
    footer = '''
    },
    ActiveTool = "Bake"
}
'''

    #
    comp.Lock()
    comp.StartUndo('RS Bake')

    for tool_name, params in data.items():
        tool = comp.FindTool(tool_name)
        if tool is None:
            continue

        # Header, Bake Header
        text = header
        text += bake_header

        # Inputs
        for param in params:
            if tool.GetInput(param, sf) is None:
                continue
            text += input_body % (param, tool_name, param)

        # Bake Footer
        text += bake_footer

        # Splines
        for param in params:
            if tool.GetInput(param, sf) is None:
                continue
            text += spline_header % (tool_name, param)
            for i in range(sf, ef + 1):
                v = tool.GetInput(param, i)
                text += key_body % (i, v)
            text += spline_footer

        # Footer
        text += footer

        # apply
        st = ordered_dict_to_dict(bmd.readstring(text))
        comment = tool.GetInput('Comments', comp.CurrentTime)
        tool.LoadSettings(st)
        tool.SetInput('Comments', comment, comp.CurrentTime)

    comp.EndUndo(True)
    comp.Unlock()


if __name__ == '__main__':
    pass

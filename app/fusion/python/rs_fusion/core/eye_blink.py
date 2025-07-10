from rs_fusion.core import ordered_dict_to_dict


def apply(comp, length: int, close_length: int):
    tool = comp.FindTool('EyeBlink')
    if tool is None:
        return

    close_frame = length - close_length
    text = '''
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
                [0] = { 0, RH = { %d, 0 }, Flags = { Linear = true, Loop = true, PreLoop = true } },
                [%d] = { 1, LH = { %d, 0.666666666666667 }, RH = { %d, 1 }, Flags = { StepIn = true } },
                [%d] = { 0, LH = { %d, 0.333333333333333 }, Flags = { StepIn = true, Loop = true, PreLoop = true } }
            }
        }
    },
    ActiveTool = "EyeBlink"
}
''' % (
        close_frame / 3.0,
        close_frame, close_frame, close_frame + (close_length / 3.0),
        length, length,
    )
    st = ordered_dict_to_dict(bmd.readstring(text))

    #
    comp.Lock()
    comp.StartUndo('RS EyeBlink')
    tool.LoadSettings(st)
    comp.EndUndo(True)
    comp.Unlock()


def apply_mm(comp, length: int, close_length: int, offset: int = 0):
    tool = comp.FindTool('EyeAnim')
    if tool is None:
        return

    close_frame = length - close_length
    text = '''
{
    Tools = ordered() {
        EyeAnim = PipeRouter {
            CtrlWZoom = false,
            Inputs = {
                LayerEnabled1 = Input {
                    SourceOp = "EyeAnimLayerEnabled1",
                    Source = "Value",
                },
                LayerEnabled2 = Input {
                    SourceOp = "EyeAnimLayerEnabled2",
                    Source = "Value",
                },
            },
            ViewInfo = OperatorInfo { Pos = { 10285, -940.5 } },
        },
        EyeAnimLayerEnabled1 = BezierSpline {
            SplineColor = { Red = 198, Green = 82, Blue = 232 },
            CtrlWZoom = false,
            NameSet = true,
            KeyFrames = {
                [%d] = { 1, Flags = { Linear = true, Loop = true, PreLoop = true } },
                [%d] = { 0, Flags = { StepIn = true } },
                [%d] = { 1, Flags = { StepIn = true, Loop = true, PreLoop = true } }
            }
        },
        EyeAnimLayerEnabled2 = BezierSpline {
            SplineColor = { Red = 232, Green = 82, Blue = 214 },
            CtrlWZoom = false,
            NameSet = true,
            KeyFrames = {
                [%d] = { 0, Flags = { Linear = true, Loop = true, PreLoop = true } },
                [%d] = { 1, Flags = { StepIn = true } },
                [%d] = { 0, Flags = { StepIn = true, Loop = true, PreLoop = true } }
            }
        }
    },
    ActiveTool = "EyeAnim"
}
''' % (
        offset,
        offset + close_frame,
        offset + length,
        offset,
        offset + close_frame,
        offset + length,
    )
    st = ordered_dict_to_dict(bmd.readstring(text))

    # store
    parm_name_list = [
        'Comments',
        'LayerName1',
        'LayerName2',
    ]
    parm_dct = {}
    for parm in parm_name_list:
        parm_dct[parm] = tool.GetInput(parm, comp.CurrentTime)

    # apply
    comp.Lock()
    comp.StartUndo('RS EyeBlink')

    tool.LoadSettings(st)

    # restore
    for parm in parm_name_list:
        tool.SetInput(parm, parm_dct[parm], comp.CurrentTime)

    comp.EndUndo(True)
    comp.Unlock()


def delete_mm(comp):
    tool = comp.FindTool('EyeAnim')
    if tool is None:
        return
    # apply
    comp.Lock()
    comp.StartUndo('RS Delete EyeBlink')
    tool.LayerEnabled1.ConnectTo()
    tool.LayerEnabled1 = 1
    tool.LayerEnabled2.ConnectTo()
    tool.LayerEnabled2 = 0
    comp.EndUndo(True)
    comp.Unlock()


def apply_sw(comp, length: int, close_length: int, offset: int = 0):
    tool = comp.FindTool('EyeAnim')
    if tool is None:
        return

    close_frame = length - close_length
    text = '''
{
    Tools = ordered() {
        EyeAnim = PipeRouter {
            CtrlWZoom = false,
            Inputs = {
				Source = Input {
					SourceOp = "EyeAnimSource",
					Source = "Value",
				}
			},
            ViewInfo = OperatorInfo { Pos = { 10285, -940.5 } },
        },
        EyeAnimSource = BezierSpline {
			SplineColor = { Red = 220, Green = 245, Blue = 25 },
			CtrlWZoom = false,
			NameSet = true,
            KeyFrames = {
                [%d] = { 0, Flags = { Linear = true, Loop = true, PreLoop = true } },
                [%d] = { 1, Flags = { StepIn = true } },
                [%d] = { 0, Flags = { StepIn = true, Loop = true, PreLoop = true } }
            }
        },
    },
    ActiveTool = "EyeAnim"
}
''' % (
        offset,
        offset + close_frame,
        offset + length,
    )
    st = ordered_dict_to_dict(bmd.readstring(text))

    # store
    parm_name_list = [
        'Comments',
        'LayerName1',
        'LayerName2',
    ]
    parm_dct = {}
    for parm in parm_name_list:
        parm_dct[parm] = tool.GetInput(parm, comp.CurrentTime)

    # apply
    comp.Lock()
    comp.StartUndo('RS EyeBlink')

    tool.LoadSettings(st)

    # restore
    for parm in parm_name_list:
        tool.SetInput(parm, parm_dct[parm], comp.CurrentTime)

    comp.EndUndo(True)
    comp.Unlock()

def delete_sw(comp):
    tool = comp.FindTool('EyeAnim')
    if tool is None:
        return
    comp.Lock()
    comp.StartUndo('RS Delete EyeBlink')
    tool.Source.ConnectTo()
    tool.Source = 0
    comp.EndUndo(True)
    comp.Unlock()

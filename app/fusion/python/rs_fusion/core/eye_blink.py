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

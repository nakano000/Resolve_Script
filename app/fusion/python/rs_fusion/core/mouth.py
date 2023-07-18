from rs_fusion.core import ordered_dict_to_dict


def delete_mm(comp):
    tool = comp.FindTool('MouthAnim')
    if tool is None:
        return

    text = '''
    {
        Tools = ordered() {
            MouthAnim = PipeRouter {
                CtrlWZoom = false,
                Inputs = {
                    LayerEnabled1 = Input { Value = 1, },
                    LayerEnabled2 = Input { Value = 0, },
                    LayerEnabled3 = Input { Value = 0, },
                    LayerEnabled4 = Input { Value = 0, },
                    LayerEnabled5 = Input { Value = 0, },
                    LayerEnabled6 = Input { Value = 0, },
                    LayerEnabled7 = Input { Value = 0, },
                },
                ViewInfo = OperatorInfo { Pos = { 10285, -940.5 } },
            },
        },
        ActiveTool = "MouthAnim"
    }
    '''
    st = ordered_dict_to_dict(bmd.readstring(text))

    # store
    parm_name_list = [
        'Comments',
        'LayerName1',
        'LayerName2',
        'LayerName3',
        'LayerName4',
        'LayerName5',
        'LayerName6',
        'LayerName7',
    ]
    parm_dct = {}
    for parm in parm_name_list:
        parm_dct[parm] = tool.GetInput(parm, comp.CurrentTime)

    # apply
    comp.Lock()
    comp.StartUndo('RS Mouth')

    tool.LoadSettings(st)

    # restore
    for parm in parm_name_list:
        tool.SetInput(parm, parm_dct[parm], comp.CurrentTime)

    comp.EndUndo(True)
    comp.Unlock()

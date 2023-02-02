def make_bg(name, x, y):
    return bmd.readstring("""{
    Tools = ordered() {
        ['""" + name + """'] = Background {
            CtrlWZoom = false,
            Inputs = {
                Width = Input { Value = 1920, },
                Height = Input { Value = 1080, },
                UseFrameFormatSettings = Input { Value = 1, },
                ["Gamut.SLogVersion"] = Input { Value = FuID { "SLog2" }, },
                TopLeftAlpha = Input { Value = 0, },
            },
            ViewInfo = OperatorInfo { Pos = { """ + str(x) + """, """ + str(y) + """ } },
        }
    }
}""")


def make_mg(name, back, fore, x, y):
    return bmd.readstring("""{
    Tools = ordered() {
        ['""" + name + """'] = Merge {
            CtrlWZoom = false,
            Inputs = {
                Background = Input {
                    SourceOp = '""" + back + """',
                    Source = "Output",
                },
                Foreground = Input {
                    SourceOp = '""" + fore + """',
                    Source = "Output",
                },
                PerformDepthMerge = Input { Value = 0, },
            },
            ViewInfo = OperatorInfo { Pos = { """ + str(x) + """, """ + str(y) + """ } },
        }
    }
}""")


def make_instance(instance_name, source_name, s, e, x, y):
    return bmd.readstring("""{
    Tools = ordered() {
        ['""" + instance_name + """'] = TextPlus {
            SourceOp = '""" + source_name + """',
            Inputs = {
                SettingsNest = Input { },
                ImageNest = Input { },
                ["Gamut.ColorSpaceNest"] = Input { },
                ["Gamut.GammaSpaceNest"] = Input { },
                Layout = Input { },
                LayoutRotation = Input { Value = 1, },
                Background = Input { },
                TransformTransform = Input { },
                TransformRotation = Input { Value = 1, },
                TransformShear = Input { },
                TransformSize = Input { },
                Properties1 = Input { },
                Softness1 = Input { Value = 1, },
                Position1 = Input { },
                Rotation1 = Input { },
                Shear1 = Input { },
                Size1 = Input { },
                TextText = Input { },
                Start = Input { Value = """ + str(s) + """, },
                End = Input { Value = """ + str(e) + """, },
                TabSpacing = Input { },
                AdvancedFontControls = Input { },
                Internal = Input { },
                CommentsNest = Input { },
                FrameRenderScriptNest = Input { },
                StartRenderScripts = Input { },
                EndRenderScripts = Input { },
                EffectMask = Input { }
            },
            ViewInfo = OperatorInfo { Pos = { """ + str(x) + ', ' + str(y) + """ } },
        }
    }
}""")


def separate():
    tool_list: dict = comp.GetToolList(True, 'TextPlus')
    comp.Lock()
    comp.StartUndo('RS Paste Instance')
    for v in tool_list.values():
        txt = v.GetInput('StyledText')
        if txt == '':
            continue
        step = 1 / len(txt)
        st = v.SaveSettings()
        pos = st['Tools'][v.Name]['ViewInfo']['Pos']
        x_step = 110
        y_step = 100

        # make background
        bg_name = 'Background1'
        bg_st = make_bg(
            bg_name,
            -x_step + pos[1],
            2 * y_step + pos[2],
        )
        st['Tools'][bg_name] = bg_st['Tools'][bg_name]
        prev = bg_name
        for i, c in enumerate(txt):
            # make instance
            inst_name = 'Instance' + v.Name + '_' + str(i) + '_' + c
            inst_st = make_instance(
                inst_name,
                v.Name,
                (i - 0.5) * step,
                (i + 0.5) * step,
                x_step * i + pos[1],
                y_step + pos[2],
            )
            st['Tools'][inst_name] = inst_st['Tools'][inst_name]

            # make merge
            mg_name = 'Merge' + str(i) + '_' + c
            mg_st = make_mg(
                mg_name,
                prev,
                inst_name,
                x_step * i + pos[1],
                2 * y_step + pos[2],
            )
            st['Tools'][mg_name] = mg_st['Tools'][mg_name]
            prev = mg_name

        # make
        v.Delete()
        comp.Paste(st)

    comp.EndUndo(True)
    comp.Unlock()


separate()

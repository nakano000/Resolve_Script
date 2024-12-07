win_name = 'VoiceDropper'

try:
  ui = fu.UIManager
  disp = bmd.UIDispatcher(ui)
  dlg = disp.AddWindow(
      {'WindowTitle': win_name, 'ID': win_name + 'Splash', },
      [
          ui.VGroup({"Spacing": 5, },
                    [
                        ui.Label({
                            'ID': 'Message',
                            'Text': win_name + '\n起動中...',
                            'Alignment': {'AlignHCenter': True, 'AlignVCenter': True},
                            'StyleSheet': 'font-size: 24px;',
                        }),
                    ]),
      ]
  )

  dlg.Show()
  from rs_resolve.tool.voice_dropper import run
  dlg.Hide()
except:
  from rs_resolve.tool.voice_dropper import run

run(app)

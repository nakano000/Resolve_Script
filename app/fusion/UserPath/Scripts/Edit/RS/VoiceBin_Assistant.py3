ui = fu.UIManager
disp = bmd.UIDispatcher(ui)
dlg = disp.AddWindow(
    {"WindowTitle": "VoiceBin アシスタント", "ID": "VoiceBinSplash", },
    [
        ui.VGroup({"Spacing": 5, },
                  [
                      ui.Label({
                          'ID': 'MyLabel',
                          'Text': 'VoiceBinアシスタント\n起動中...',
                          'Alignment': {'AlignHCenter': True, 'AlignVCenter': True},
                          'StyleSheet': 'font-size: 24px;',
                      }),
                  ]),
    ]
)
dlg.Show()
from rs_resolve.tool.voice_bin_assistant import run

dlg.Hide()

run(app)

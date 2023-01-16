#Requires AutoHotkey v2.0
#HotIf WinActive("ahk_exe voicepeak.exe")

; Ctrl-Space ブロック再生
^Space::{
    SetKeyDelay 75, 25
    SendEvent '^{a}{Tab}{Space}+{Tab}'
}

; Ctrl-Click 字幕コピー ブロック音声出力
^LButton::{
    Click
    Sleep 100
    Send '^{a}^{c}'
    Sleep 100
    Click "Right"
    Send '{Up}'
    Send '{Enter}'
    Sleep 250
    Click 100, 100
    Send '{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}'
    Send '{Enter}'
    Sleep 250
    Send '{Enter}'
}

#HotIf


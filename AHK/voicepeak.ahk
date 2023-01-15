#Requires AutoHotkey v2.0
#HotIf WinActive("ahk_exe voicepeak.exe")

^Space::{
    SetKeyDelay 75, 25
    SendEvent '^{a}{Tab}{Space}+{Tab}'
}

^LButton::{
    Click
    Send '^{a}^{c}'
    Click "Right"
    Send '{Up}'
    Send '{Enter}'
    Sleep 500
    Click 100, 100
    Send '{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}{Tab}'
    Send '{Enter}'
    Sleep 500
    Send '{Enter}'
}

#HotIf


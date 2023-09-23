import subprocess

import pywinctl

from rs.core import util


def get_resolve_window(pj_name):
    for t in pywinctl.getAllTitles():
        if not util.IS_MAC:
            flag = t.startswith('DaVinci Resolve') and t.endswith(pj_name)
            flag = flag or t.startswith('DaVinci Resolve by Blackmagic Design')
        else:
            flag = t == pj_name
        if flag:
            return pywinctl.getWindowsWithTitle(t)[0]
    return None


def activate_window(w):
    if not util.IS_MAC:
        w.activate()
    else:
        subprocess.run([
            'osascript',
            '-e',
            'tell application "DaVinci Resolve" to activate',
        ])

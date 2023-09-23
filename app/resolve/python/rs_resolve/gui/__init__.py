import subprocess

from rs.core import util

if util.IS_MAC:
    def get_resolve_window(pj_name):
        return None
else:
    import pywinctl


    def get_resolve_window(pj_name):
        for t in pywinctl.getAllTitles():
            flag = t.startswith('DaVinci Resolve') and t.endswith(pj_name)
            flag = flag or t.startswith('DaVinci Resolve by Blackmagic Design')
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

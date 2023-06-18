import pygetwindow


def get_resolve_window(pj_name):
    for t in pygetwindow.getAllTitles():
        flag = t.startswith('DaVinci Resolve') and t.endswith(pj_name)
        flag = flag or t.startswith('DaVinci Resolve by Blackmagic Design')
        if flag:
            return pygetwindow.getWindowsWithTitle(t)[0]
    return None

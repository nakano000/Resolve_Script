import sys


def get():
    try:
        print('test')
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath = (
                    os.getenv('PROGRAMDATA')
                    + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
            )
        elif sys.platform.startswith("linux"):
            expectedPath = "/opt/resolve/libs/Fusion/Modules/"

        try:
            import imp
            bmd = imp.load_source('DaVinciResolveScript', expectedPath + "DaVinciResolveScript.py")
        except ImportError:
            return None

    return bmd.scriptapp("Resolve")


if __name__ == '__main__':
    resolve = get()
    print(resolve)

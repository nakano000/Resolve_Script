import shutil
from pathlib import Path

from PySide2.QtCore import (
    QMimeData,
)
from PySide2.QtGui import QDrag
from PySide2.QtWidgets import QPushButton

from rs.core import (
    config,
)


class DragButton(QPushButton):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        cmd_dir: Path = config.CONFIG_DIR.joinpath('VoiceBin', 'Scripts')
        cmd_dir.mkdir(parents=True, exist_ok=True)
        self.cmd_file: Path = cmd_dir.joinpath('Import_cmd.lua')
        #
        self.lua_file = None

    def setLuaFile(self, path: Path):
        self.lua_file = path

    def mousePressEvent(self, e):
        lua = self.lua_file
        if lua is None or not lua.is_file():
            return
        shutil.copyfile(lua, self.cmd_file)
        # Drag
        m = QMimeData()
        m.setUrls(['file:' + str(self.cmd_file).replace('\\', '/')])
        drag = QDrag(self)
        drag.setMimeData(m)
        drag.exec_()

import shutil
from pathlib import Path

from PySide2.QtCore import (
    QMimeData,
    QSize,
)
from PySide2.QtGui import (
    QDrag,
    QIcon,
)
from PySide2.QtWidgets import QPushButton

from rs.core import (
    config,
)


class DragButton(QPushButton):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        # icon
        icon_file = config.ROOT_PATH.joinpath('data', 'image', 'icon', 'dad.svg')
        dad_icon = QIcon(str(icon_file))
        self.setIcon(dad_icon)
        self.setIconSize(QSize(40, 40))
        #
        self.lua_file = None

    def setLuaFile(self, path: Path):
        self.lua_file = path

    def mousePressEvent(self, e):
        lua = self.lua_file
        if lua is None or not lua.is_file():
            return
        # Drag
        m = QMimeData()
        m.setUrls(['file:' + str(lua).replace('\\', '/')])
        drag = QDrag(self)
        drag.setMimeData(m)
        drag.exec_()

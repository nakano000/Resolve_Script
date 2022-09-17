import shutil
from pathlib import Path
from typing import (
    List,
    Optional,
)

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
    pipe as p,
)


class DragButton(QPushButton):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        cmd_dir: Path = config.CONFIG_DIR.joinpath('VoiceBin', 'Scripts')
        cmd_dir.mkdir(parents=True, exist_ok=True)
        # icon
        icon_file = config.ROOT_PATH.joinpath('data', 'image', 'icon', 'dad.svg')
        dad_icon = QIcon(str(icon_file))
        self.setIcon(dad_icon)
        self.setIconSize(QSize(40, 40))
        #
        self.cmd_files = [
            cmd_dir.joinpath('VoiceBin_cmd01.lua'),
            cmd_dir.joinpath('VoiceBin_cmd02.lua'),
        ]
        self.lua_files: List[Optional[Path]] = [None, None]

    def setLuaFile(self, path: Path):
        self.lua_files[0] = path

    def setLuaFiles(self, path1: Path, path2: Path, ):
        self.lua_files[0] = path1
        self.lua_files[1] = path2

    def mousePressEvent(self, e):
        urls = p.pipe(
            [0, 1],
            p.filter(lambda i: self.lua_files[i] is not None and self.lua_files[i].is_file()),
            list,  # filter objectと doが相性悪い？
            p.do(
                p.iter(lambda i: shutil.copyfile(self.lua_files[i], self.cmd_files[i])),
            ),
            p.map(lambda i: 'file:' + str(self.cmd_files[i]).replace('\\', '/')),
            list,
        )
        if len(urls) == 0:
            return
        # Drag
        m = QMimeData()
        m.setUrls(urls)
        drag = QDrag(self)
        drag.setMimeData(m)
        drag.exec_()

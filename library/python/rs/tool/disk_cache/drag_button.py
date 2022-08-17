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
        cmd_dir: Path = config.CONFIG_DIR.joinpath('DiskCache', 'Scripts')
        cmd_dir.mkdir(parents=True, exist_ok=True)
        self.cmd_file: Path = cmd_dir.joinpath('cmd.lua')
        script_base_file: Path = config.ROOT_PATH.joinpath('data', 'app', 'DiskCache', 'script_base.txt')
        self.script_base: str = script_base_file.read_text(encoding='utf-8')
        # icon
        icon_file = config.ROOT_PATH.joinpath('data', 'image', 'icon', 'dad.svg')
        dad_icon = QIcon(str(icon_file))
        self.setIcon(dad_icon)
        self.setIconSize(QSize(40, 40))
        #
        self.render = True
        self.color = ''
        self.indexes = []

    def mousePressEvent(self, e):
        self.cmd_file.write_text(
            '\n'.join([
                self.script_base,
                'cache(',
                '\t\t%s,' % str(self.render).lower(),
                '\t\t"%s",' % self.color,
                '\t\t{ % s}' % ', '.join(self.indexes),
                ')\n',
            ]),
            encoding='utf-8',
            newline='\n',
        )
        # Drag
        m = QMimeData()
        m.setUrls(['file:' + str(self.cmd_file).replace('\\', '/')])
        drag = QDrag(self)
        drag.setMimeData(m)
        drag.exec_()

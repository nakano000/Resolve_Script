from pathlib import Path

from PySide2.QtCore import (
    QMimeData, QSize,
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
        cmd_dir: Path = config.CONFIG_DIR.joinpath('ScriptLauncher', 'Scripts')
        cmd_dir.mkdir(parents=True, exist_ok=True)
        self.cmd_file: Path = cmd_dir.joinpath('Apply_cmd.lua')
        script_base_file: Path = config.ROOT_PATH.joinpath('data', 'app', 'ScriptLauncher', 'script_base.txt')
        self.script_base: str = script_base_file.read_text(encoding='utf-8')

        # icon
        icon_file = config.ROOT_PATH.joinpath('data', 'image', 'icon', 'dad.svg')
        dad_icon = QIcon(str(icon_file))
        self.setIcon(dad_icon)
        self.setIconSize(QSize(40, 40))
        #
        self.filter_file = None
        self.setting_file = None
        self.track_index: int = 1

    def setFilterFile(self, path):
        self.filter_file = path

    def setSettingFile(self, path):
        self.setting_file = path

    def setTrackIndex(self, index: int):
        self.track_index = index

    def mousePressEvent(self, e):
        setting = self.setting_file
        if setting is None or not setting.is_file():
            return
        filter_file = self.filter_file
        filter_text = ''
        if filter_file is not None and filter_file.is_file():
            filter_text = p.pipe(
                filter_file.read_text(encoding='utf-8'),
                p.call.split('\n'),
                p.map(p.call.strip()),
                p.filter(lambda s: s != ''),
                p.map(lambda s: '        "' + s + '"'),
                list,
                ',\n'.join,
            )
        r = self.script_base % (str(setting).replace('\\', '\\\\'), filter_text, self.track_index)
        self.cmd_file.write_text(r, encoding='utf-8')
        # Drag
        m = QMimeData()
        m.setUrls(['file:' + str(self.cmd_file).replace('\\', '/')])
        drag = QDrag(self)
        drag.setMimeData(m)
        drag.exec_()

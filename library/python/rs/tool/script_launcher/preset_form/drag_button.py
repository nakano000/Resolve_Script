from pathlib import Path

from PySide2.QtCore import (
    QMimeData,
)
from PySide2.QtGui import QDrag
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
        #
        self.filter_file = None
        self.setting_file = None

    def setFilterFile(self, path):
        self.filter_file = path

    def setSettingFile(self, path):
        self.setting_file = path

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
        r = self.script_base % (str(setting).replace('\\', '\\\\'), filter_text)
        self.cmd_file.write_text(r, encoding='utf-8')
        # Drag
        m = QMimeData()
        m.setUrls(['file:' + str(self.cmd_file).replace('\\', '/')])
        drag = QDrag(self)
        drag.setMimeData(m)
        drag.exec_()

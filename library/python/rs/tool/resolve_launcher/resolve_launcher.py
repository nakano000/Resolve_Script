from functools import partial

import dataclasses
import sys
from pathlib import Path

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QMessageBox,
)

from rs.core import (
    config,
    pipe as p,
    util,
)
from rs.core.app import (
    Fusion,
    Resolve,
)
from rs.gui import (
    appearance,
)
from rs.tool.resolve_launcher.resolve_launcher_ui import Ui_MainWindow

APP_NAME = 'ResolveLauncher'


@dataclasses.dataclass
class ConfigData(config.Data):
    fusion: Fusion = dataclasses.field(default_factory=Fusion)
    resolve: Resolve = dataclasses.field(default_factory=Resolve)
    do_close: bool = False


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(700, 100)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # button
        self.ui.dragButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.resolveButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.fusionButton.setStyleSheet(appearance.other_stylesheet)

        self.ui.dragButton.lua_file = config.DATA_PATH.joinpath('app', 'ResolveLauncher', 'set_pathmap.lua')

        # event
        self.ui.fusionButton.clicked.connect(self.run_fusion)
        self.ui.resolveButton.clicked.connect(self.run_resolve)
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.fusionToolButton.clicked.connect(partial(
            self.toolButton_clicked,
            self.ui.fusionLineEdit,
            'Fusion' + ('.exe' if util.IS_WIN else '')
        ))
        self.ui.resolveToolButton.clicked.connect(partial(
            self.toolButton_clicked,
            self.ui.resolveLineEdit,
            'Resolve' + ('.exe' if util.IS_WIN else '')
        ))

    def run_fusion(self):
        c = self.get_data()
        app = c.fusion
        if not Path(app.exe).is_file():
            QMessageBox.warning(self, 'File Not Found', '%s\nファイルが存在しません。' % app.exe)
            return
        app.execute([])
        if c.do_close:
            self.close()

    def run_resolve(self):
        c = self.get_data()
        app = c.resolve
        if not Path(app.exe).is_file():
            QMessageBox.warning(self, 'File Not Found', '%s\nファイルが存在しません。' % app.exe)
            return
        app.execute([])
        if c.do_close:
            self.close()

    def toolButton_clicked(self, w, name: str) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select %s' % name,
            w.text(),
            '%s(%s)' % (name, name),
        )
        if path != '':
            w.setText(path)

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        self.ui.fusionLineEdit.setText(c.fusion.exe.replace('\\', '/'))
        self.ui.resolveLineEdit.setText(c.resolve.exe.replace('\\', '/'))
        self.ui.checkBox.setChecked(c.do_close)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.fusion.exe = self.ui.fusionLineEdit.text()
        c.resolve.exe = self.ui.resolveLineEdit.text()
        c.do_close = self.ui.checkBox.isChecked()
        return c

    def load_config(self) -> None:
        c = self.new_config()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_data()
        c.save(self.config_file)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

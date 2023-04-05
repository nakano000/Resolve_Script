import functools
import sys
from functools import partial
from pathlib import Path

import dataclasses
from PySide2.QtCore import (
    Qt,
)

from PySide2.QtWidgets import (
    QApplication,
    QMainWindow, QFileDialog,
)

from rs.core import (
    pipe as p, config,
)
from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op
from rs_fusion.tool.paste_tool.paste_tool_ui import Ui_MainWindow
from rs_fusion.tool.paste_tool.node_window import MainWindow as NodeWindow

APP_NAME = 'PasteTool'


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(300, 300)

        self.fusion = fusion

        # config
        self.config_dir: Path = config.CONFIG_DIR.joinpath(APP_NAME)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.default_file: Path = self.config_dir.joinpath('default.txt')
        if not self.default_file.exists():
            self.default_file.write_text('StyledText\nWidth\nHeight\nUseFrameFormatSettings', encoding='utf-8')
        self.ui.plainTextEdit.setPlainText(
            self.default_file.read_text(encoding='utf-8')
        )

        # window
        self.node_window = NodeWindow(parent=self, fusion=fusion)

        # style sheet
        self.ui.pasteButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.nodeButton.setStyleSheet(appearance.other_stylesheet)

        # event
        self.ui.pasteButton.clicked.connect(self.paste)
        self.ui.nodeButton.clicked.connect(self.node_window.show)
        self.node_window.ui.addButton.clicked.connect(self.add)

        self.ui.loadButton.clicked.connect(self.load_txt)
        self.ui.saveButton.clicked.connect(self.save_txt)

        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

    def load_txt(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file', str(self.config_dir), 'Text files (*.txt)')[0]
        if file_name == '':
            return
        self.ui.plainTextEdit.setPlainText(
            Path(file_name).read_text(encoding='utf-8')
        )

    def save_txt(self):
        file_name = QFileDialog.getSaveFileName(self, 'Save file', str(self.config_dir), 'Text files (*.txt)')[0]
        if file_name == '':
            return
        Path(file_name).write_text(
            self.ui.plainTextEdit.toPlainText(),
            encoding='utf-8',
        )

    def add(self):
        lst = self.node_window.get_selection()
        self.ui.plainTextEdit.appendPlainText('\n'.join(lst))

    def paste(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return

        lst = p.pipe(
            self.ui.plainTextEdit.toPlainText().splitlines(),
            p.map(lambda x: x.strip()),
            p.filter(lambda x: x != ''),
            list,
        )

        text = QApplication.clipboard().text()

        op.paste_setting(
            comp,
            text,
            lst,
            self.ui.useRefreshCheckBox.isChecked(),
        )


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run(None)

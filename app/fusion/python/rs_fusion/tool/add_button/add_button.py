import sys
from pathlib import Path
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)

from rs.core import (
    config,
    util,
    pipe as p,
)
from rs.gui import (
    appearance,
)
from rs_fusion.tool.add_button.add_button_ui import Ui_MainWindow

APP_NAME = 'ボタン追加'


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
        self.resize(250, 100)

        self.fusion = fusion
        self.lua_script = config.DATA_PATH.joinpath('lua', 'add_button.lua').read_text(encoding='utf-8')
        # button
        self.ui.addButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.addButton.clicked.connect(self.add)
        self.ui.closeButton.clicked.connect(self.close)

    def add(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            QMessageBox.warning(self, 'Warning', 'Fusion Pageで実行してください。')
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            QMessageBox.warning(self, 'Warning', 'コンポジションが見付かりません。')
            return

        self.fusion.Execute('\n'.join([
            self.lua_script,
            'AddButton(%s, %s, %s)' % (
                str(self.ui.refreshCheckBox.isChecked()).lower(),
                str(self.ui.loadCheckBox.isChecked()).lower(),
                str(self.ui.saveCheckBox.isChecked()).lower(),
            ),
        ]))


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass

import sys
import functools
from PySide2.QtCore import (
    Qt,
    QStringListModel,
    QSortFilterProxyModel,
)
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
)

from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op
from rs_fusion.tool.bg_tool.bg_tool_ui import Ui_MainWindow

APP_NAME = 'BGTool'


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
            | Qt.MSWindowsFixedSizeDialogHint
        )
        self.resize(200, 100)

        self.fusion = fusion

        # padding
        self.ui.paddingXSpinBox.setValue(100)
        self.ui.paddingYSpinBox.setValue(100)

        # button
        self.ui.insertButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.insertButton.clicked.connect(self.insert)
        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        #

    def insert(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return
        op.background(
            comp,
            self.ui.paddingXSpinBox.value(),
            self.ui.paddingYSpinBox.value(),
            self.ui.squareCheckBox.isChecked(),
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
    pass

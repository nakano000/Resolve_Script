import sys
from functools import partial
from pathlib import Path

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtGui import (
    QColor,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QMenu, QAction, QMessageBox,
)

from rs.core import (
    config,
    pipe as p,
    util,
)
from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op

from rs_fusion.tool.comp_utility.comp_utility_ui import Ui_MainWindow
from rs_fusion.tool.set_pivot import MainWindow as PivotWindow
from rs_fusion.tool.insert_tool import MainWindow as InsertWindow

APP_NAME = 'CompUtility'


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowCloseButtonHint
            # | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.MSWindowsFixedSizeDialogHint
        )
        self.resize(140, 60)

        self.fusion = fusion

        # window
        pivot_window = PivotWindow(fusion=self.fusion)
        insert_window = InsertWindow(fusion=self.fusion)

        # menu
        lst = [
            ('STILL IMAGE', self.load),
            ('MERGE', self.merge),
            ('INSERT', insert_window.show),
            ('PIVOT', pivot_window.show),
        ]
        b = self.ui.toolButton
        menu = QMenu(b)
        for x in lst:
            act = QAction(x[0], b)
            act.triggered.connect(x[1])
            menu.addAction(act)
        b.setMenu(menu)

        # style sheet
        b.setStyleSheet(appearance.other_stylesheet)

    def check_page(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return False
        return True

    def get_comp(self):
        if not self.check_page():
            return None
        comp = self.fusion.CurrentComp
        if comp is None:
            return None
        return comp

    def load(self):
        comp = self.get_comp()
        if comp is None:
            return
        op.loader(comp)

    def merge(self):
        comp = self.get_comp()
        if comp is None:
            return
        op.merge(comp)

    def insert(self):
        comp = self.get_comp()
        if comp is None:
            return
        op.insert(comp, 'Transform')


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

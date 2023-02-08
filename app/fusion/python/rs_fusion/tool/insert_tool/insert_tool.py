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
    QMainWindow, QAction,
)

from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op
from rs_fusion.tool.insert_tool.insert_tool_ui import Ui_MainWindow

APP_NAME = 'InsertTool'


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
        self.resize(200, 600)

        self.fusion = fusion

        # list view
        lst = []
        self.dct = {}
        reg = list(self.fusion.GetRegList(self.fusion.CT_Tool).values())
        for r in reg:
            attrs = r.GetAttrs()
            txt = r.Name
            if 'REGS_OpIconString' in attrs:
                txt += '(' + attrs['REGS_OpIconString'] + ')'
            lst.append(txt)
            self.dct[txt] = r.ID
        v = self.ui.listView
        m = QStringListModel(lst)
        pm = QSortFilterProxyModel()
        pm.setFilterCaseSensitivity(Qt.CaseInsensitive)
        pm.setSourceModel(m)
        v.setModel(pm)
        sm = v.selectionModel()
        self.model = m
        self.proxy_model = pm
        self.selection_model = sm

        # shortcut
        up_action = QAction(self)
        up_action.setShortcut(QKeySequence(Qt.Key_Up))
        up_action.setShortcutContext(Qt.ApplicationShortcut)
        up_action.triggered.connect(self.select_up)
        self.addAction(up_action)
        down_action = QAction(self)
        down_action.setShortcut(QKeySequence(Qt.Key_Down))
        down_action.setShortcutContext(Qt.ApplicationShortcut)
        down_action.triggered.connect(self.select_down)
        self.addAction(down_action)

        # button
        self.ui.insertButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.lineEdit.textChanged.connect(pm.setFilterFixedString)
        self.ui.lineEdit.textChanged.connect(self.select_first)
        self.ui.lineEdit.returnPressed.connect(self.insert)
        #
        self.ui.insertButton.clicked.connect(self.insert)
        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        #

    def select_first(self):
        self.selection_model.select(self.proxy_model.index(0, 0), self.selection_model.ClearAndSelect)

    def select_up(self):
        indexes = self.selection_model.selectedIndexes()
        if len(indexes) == 0:
            self.select_first()
            return
        index = indexes[0]
        row = index.row()
        if row > 0:
            self.selection_model.select(self.proxy_model.index(row - 1, 0), self.selection_model.SelectCurrent)

    def select_down(self):
        indexes = self.selection_model.selectedIndexes()
        if len(indexes) == 0:
            self.select_first()
            return
        index = indexes[0]
        row = index.row()
        if row < self.proxy_model.rowCount() - 1:
            self.selection_model.select(self.proxy_model.index(row + 1, 0), self.selection_model.SelectCurrent)

    def insert(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return
        indexes = self.selection_model.selectedIndexes()
        if len(indexes) == 0:
            return
        txt = self.model.data(self.proxy_model.mapToSource(indexes[0]), Qt.DisplayRole)
        op.insert(comp, self.dct[txt])

    def show(self) -> None:
        super().show()
        self.ui.lineEdit.setFocus()


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

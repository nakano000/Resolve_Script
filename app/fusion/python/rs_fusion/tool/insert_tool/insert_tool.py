import sys
import functools
from PySide6.QtCore import (
    Qt,
    QStringListModel,
    QSortFilterProxyModel,
    QEvent, QItemSelectionModel,
)
from PySide6.QtGui import (
    QKeySequence,
    QKeyEvent,
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
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

        return_action = QAction(self)
        return_action.setShortcut(QKeySequence(Qt.Key_Return))
        return_action.setShortcutContext(Qt.ApplicationShortcut)
        return_action.triggered.connect(self.insert)
        self.addAction(return_action)

        # button
        self.ui.insertButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.lineEdit.textChanged.connect(pm.setFilterFixedString)
        self.ui.lineEdit.textChanged.connect(self.select_first)
        #
        self.ui.insertButton.clicked.connect(self.insert)
        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.select_first()

    def select_first(self):
        self.selection_model.clearSelection()
        self.selection_model.select(self.proxy_model.index(0, 0), QItemSelectionModel.SelectionFlag.SelectCurrent)
        self.ui.listView.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier))

    def select_up(self):
        self.ui.listView.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier))

    def select_down(self):
        self.ui.listView.keyPressEvent(QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier))

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

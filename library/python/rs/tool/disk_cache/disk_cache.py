import sys

from PySide2.QtCore import (
    Qt,
    QStringListModel,
    QItemSelectionModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.core import (
    pipe as p,
)
from rs.gui import (
    appearance,
)

from rs.tool.disk_cache.disk_cache_ui import Ui_MainWindow

APP_NAME = 'DiskCache'


def select(v, names):
    m: QStringListModel = v.model()
    sm = v.selectionModel()
    sm.clear()
    ss = m.stringList()
    for name in names:
        if name in ss:
            i = m.match(m.index(0, 0), Qt.DisplayRole, name)[0]
            sm.setCurrentIndex(
                i,
                QItemSelectionModel.SelectCurrent | QItemSelectionModel.Rows
            )


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('%s' % APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(500, 500)

        # list view
        maker_m = QStringListModel()
        maker_m.setStringList([
            'Blue',
            'Cyan',
            'Green',
            'Yellow',
            'Red',
            'Pink',
            'Purple',
            'Fuchsia',
            'Rose',
            'Lavender',
            'Sky',
            'Mint',
            'Lemon',
            'Sand',
            'Cocoa',
            'Cream',
        ])
        self.ui.markerListView.setModel(maker_m)
        index_m = QStringListModel()
        index_m.setStringList(p.pipe(
            range(1, 21),
            p.map(str),
            list,
        ))
        self.ui.videoIndexListView.setModel(index_m)

        # button
        self.ui.cacheDragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.cacheDragButton.render = True
        self.ui.clearDragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.clearDragButton.render = False

        # event
        self.ui.markerListView.selectionModel().selectionChanged.connect(self.set_color)
        self.ui.videoIndexListView.selectionModel().selectionChanged.connect(self.set_indexes)

        #
        select(self.ui.markerListView, ['Blue'])
        select(self.ui.videoIndexListView, ['1'])

    def set_indexes(self):
        v = self.ui.videoIndexListView
        m: QStringListModel = v.model()
        indexes = p.pipe(
            v.selectionModel().selectedIndexes(),
            p.map(m.data),
            p.map(str),
            list,
        )
        self.ui.cacheDragButton.indexes = indexes
        self.ui.clearDragButton.indexes = indexes

    def set_color(self):
        color: str = ''
        v = self.ui.markerListView
        m: QStringListModel = v.model()
        lst = v.selectionModel().selectedIndexes()
        if len(lst) > 0:
            color = m.data(lst[0])
        self.ui.cacheDragButton.color = color
        self.ui.clearDragButton.color = color


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

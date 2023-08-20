import dataclasses
import sys

from typing import Any

from PySide6.QtCore import (
    Qt,
    QModelIndex,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHeaderView,

)

from rs.core import (
    pipe as p,
)

from rs.gui import (
    appearance,
    table,
)
from rs.tool.voice_sync.check_timing_ui import Ui_MainWindow


@dataclasses.dataclass
class Data(table.RowData):
    src_no: str = ''
    src: str = ''
    ref: str = ''


class Model(table.Model):

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                return self.get_value(index.row(), index.column())

            if role == Qt.EditRole:
                return self.get_value(index.row(), index.column())

            if role == Qt.BackgroundRole:
                if index.column() not in [1, 2]:
                    return super().data(index, role)
                if self.get_value(index.row(), 1) == self.get_value(index.row(), 2):
                    return super().data(index, role)
                return QColor(80, 10, 10)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.NoItemFlags


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('チェック')
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
        )
        self.resize(250, 750)

        # table
        v = self.ui.tableView
        v.setModel(Model(Data))
        h = v.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)

    def set_data(self, data_list: list) -> None:
        self.ui.tableView.model().set_data(
            p.pipe(
                data_list,
                p.map(lambda x: Data(src=x[0], ref=x[1], src_no=x[2])),
                list,
            )
        )


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

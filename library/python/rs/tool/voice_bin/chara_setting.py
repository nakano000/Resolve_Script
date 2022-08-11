import shutil

import dataclasses
import sys

from pathlib import Path
from typing import Any

from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QItemSelectionModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QHeaderView,
    QMenu,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.core.config import (
    DataList,
)
from rs.gui import (
    appearance,
    basic_table,
)
from rs.tool.voice_bin.chara_setting_ui import Ui_MainWindow
from rs.tool.voice_bin.chara_data import CharaData


@dataclasses.dataclass
class CharaSetData(config.Data):
    chara_list: DataList = dataclasses.field(default_factory=lambda: DataList(CharaData))


class Model(basic_table.Model):

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                return dataclasses.astuple(self._data[index.row()])[index.column()]

            if role == Qt.EditRole:
                return dataclasses.astuple(self._data[index.row()])[index.column()]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.NoItemFlags


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('キャラクター設定')
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            # | Qt.WindowStaysOnTopHint
        )
        self.resize(850, 300)

        # style sheet
        self.ui.setButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.addButton.setStyleSheet(appearance.in_stylesheet)

        # config
        config_dir = config.CONFIG_DIR.joinpath('VoiceBin')
        config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file: Path = config_dir.joinpath('chara.json')

        self.template_file: Path = config.ROOT_PATH.joinpath('data', 'app', 'VoiceBin', 'chara.json')
        if not self.config_file.is_file():
            shutil.copyfile(self.template_file, self.config_file)

        # table
        v = self.ui.tableView
        v.setModel(Model(CharaData))

        hh = v.horizontalHeader()
        hh.setSectionResizeMode(4, QHeaderView.Stretch)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        # event

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.addButton.clicked.connect(self.add)
        self.ui.setButton.clicked.connect(self.save)

        self.ui.actionCopy.triggered.connect(self.copy)
        self.ui.actionPaste.triggered.connect(self.paste)
        self.ui.actionDelete.triggered.connect(self.delete)
        self.ui.actionUp.triggered.connect(self.up)
        self.ui.actionDown.triggered.connect(self.down)

    def add(self):
        m: Model = self.ui.tableView.model()
        d = CharaData()
        m.add_row_data(d)

    def contextMenu(self, pos):
        v = self.ui.tableView
        menu = QMenu(v)
        menu.addAction(self.ui.actionCopy)
        menu.addAction(self.ui.actionPaste)
        menu.addSeparator()
        menu.addAction(self.ui.actionUp)
        menu.addAction(self.ui.actionDown)
        menu.addSeparator()
        menu.addAction(self.ui.actionDelete)
        menu.exec_(v.mapToGlobal(pos))

    def copy(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        sel_list = sm.selectedIndexes()
        if len(sel_list) != 0:
            i: QModelIndex = sel_list[0]
            s = str(m.get_value(i.row(), i.column()))
            QApplication.clipboard().setText(s)

    def paste(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()

        s = QApplication.clipboard().text()
        for i in sm.selectedIndexes():
            m.setData(i, s, Qt.EditRole)

    def delete(self):
        v = self.ui.tableView
        m = v.model()
        sm = v.selectionModel()
        for row in p.pipe(
                sm.selectedIndexes(),
                p.map(p.call.row()),
                list,
                sorted,
                reversed,
        ):
            m.removeRow(row, QModelIndex())
        sm.clearSelection()

    def up(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        data_list = []
        min_row = None
        for row in p.pipe(
                sm.selectedIndexes(),
                p.map(p.call.row()),
                list,
                sorted,
                reversed,
        ):
            if min_row is None:
                min_row = row
            min_row = min([row, min_row])
            data_list.append(m.get_row_data(row))
            m.removeRow(row, QModelIndex())
        sm.clearSelection()
        if min_row is not None:
            if min_row == 0:
                min_row = 1
            m.insert_rows_data(min_row - 1, list(reversed(data_list)))
            for i in range(len(data_list)):
                index = m.index(min_row - 1 + i, 0, QModelIndex())
                sm.select(index, QItemSelectionModel.Select)
                sm.setCurrentIndex(index, QItemSelectionModel.Select)

    def down(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        data_list = []
        max_row = None
        for row in p.pipe(
                sm.selectedIndexes(),
                p.map(p.call.row()),
                list,
                sorted,
                reversed,
        ):
            if max_row is None:
                max_row = row
            max_row = max([row, max_row])
            data_list.append(m.get_row_data(row))
            m.removeRow(row, QModelIndex())
        sm.clearSelection()
        if max_row is not None:
            m.insert_rows_data(max_row + 2 - len(data_list), list(reversed(data_list)))
            for i in range(len(data_list)):
                if max_row != m.rowCount() - 1:
                    index = m.index(max_row + 2 - len(data_list) + i, 0, QModelIndex())
                else:
                    index = m.index(max_row - i, 0, QModelIndex())
                sm.select(index, QItemSelectionModel.Select)
                sm.setCurrentIndex(index, QItemSelectionModel.Select)

    def set_data(self, a: CharaSetData):
        self.ui.tableView.model().set_data(a.chara_list)

    def get_data(self) -> CharaSetData:
        a = CharaSetData()
        a.chara_list.set_list(self.ui.tableView.model().to_list())
        return a

    def get_chara_list(self):
        if not self.config_file.is_file():
            return []
        a = self.get_data()
        a.load(self.config_file)
        return a.chara_list

    def open(self) -> None:
        if self.config_file.is_file():
            a = self.get_data()
            a.load(self.config_file)
            self.set_data(a)

    def save(self) -> None:
        a = self.get_data()
        a.save(self.config_file)
        self.close()

    def show(self) -> None:
        self.open()
        super().show()


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

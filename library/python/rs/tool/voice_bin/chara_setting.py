import shutil

import dataclasses
import sys

from pathlib import Path
from typing import Any

from PySide2.QtCore import (
    Qt,
    QModelIndex,
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
    chara_data,
)
from rs.core.chara_data import (
    CharaData,
    CharaSetData,
)
from rs.gui import (
    appearance,
    basic_table,
)
from rs.tool.voice_bin.chara_setting_ui import Ui_MainWindow


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
        self.resize(900, 300)

        # style sheet
        self.ui.setButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.addButton.setStyleSheet(appearance.in_stylesheet)

        # config
        chara_data.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.config_file: Path = chara_data.CONFIG_FILE

        self.template_file: Path = chara_data.TEMPLATE_FILE
        if not self.config_file.is_file():
            shutil.copyfile(self.template_file, self.config_file)

        # table
        v = self.ui.tableView
        v.setModel(Model(CharaData))

        hh = v.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(7, QHeaderView.Stretch)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        # event

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.addButton.clicked.connect(self.add)
        self.ui.setButton.clicked.connect(self.save)

        self.ui.actionCopy.triggered.connect(self.ui.tableView.copy)
        self.ui.actionPaste.triggered.connect(self.ui.tableView.paste)
        self.ui.actionDelete.triggered.connect(self.ui.tableView.delete)
        self.ui.actionUp.triggered.connect(self.ui.tableView.up)
        self.ui.actionDown.triggered.connect(self.ui.tableView.down)

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

    def set_data(self, a: CharaSetData):
        self.ui.tableView.model().set_data(a.chara_list)

    def get_data(self) -> CharaSetData:
        a = CharaSetData()
        a.chara_list.set_list(self.ui.tableView.model().to_list())
        return a

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

import shutil

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
    QStyledItemDelegate,
    QComboBox,
    QFileDialog,
)

from rs.core import (
    config,
    pipe as p,
    chara_data,
    anim,
)
from rs.core.chara_data import (
    CharaData,
    CharaSetData,
)
from rs.gui import (
    appearance,
    table,
)
from rs.gui.chara.chara_ui import Ui_MainWindow


class Model(table.Model):

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                return self.get_value(index.row(), index.column())

            if role == Qt.EditRole:
                return self.get_value(index.row(), index.column())

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.NoItemFlags


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.color_list = ['None'] + config.COLOR_LIST
        self.encoding_list = ['auto'] + config.ENCODING_LIST
        self.item_dict = {
            2: self.color_list,
            3: self.encoding_list,
            5: anim.TYPE_LIST,
        }

    def createEditor(self, parent, option, index):
        if index.column() in self.item_dict.keys():
            lst = self.item_dict[index.column()]
            editor = QComboBox(parent)
            editor.addItems(lst)
            return editor
        elif index.column() in [7, 8]:
            editor = QFileDialog(parent)
            editor.setWindowTitle('ファイル選択')
            editor.setFileMode(QFileDialog.ExistingFile)
            editor.setAcceptMode(QFileDialog.AcceptOpen)
            editor.setOptions(QFileDialog.DontUseNativeDialog)
            if index.column() == 7:
                editor.setNameFilter('JSON File (*.json)')
            else:
                editor.setNameFilter('Setting File (*.setting)')
            return editor
        return super().createEditor(parent, option, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.column() in [7, 8]:
            pass
            return
        super().updateEditorGeometry(editor, option, index)

    def setEditorData(self, editor, index):
        if index.column() in self.item_dict.keys():
            lst = self.item_dict[index.column()]
            editor.blockSignals(True)
            value = index.data(Qt.DisplayRole)
            num = lst.index(value) if value in lst else 0
            editor.setCurrentIndex(num)
            editor.blockSignals(False)
            return
        elif index.column() in [7, 8]:
            editor: QFileDialog
            path = Path(index.data(Qt.DisplayRole))
            if not path.is_absolute():
                value = str(config.ROOT_PATH.joinpath(str(path)).parent)
            else:
                value = str(path.parent)

            editor.setDirectory(value)
            return
        super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if index.column() in self.item_dict.keys():
            value: str = editor.currentText()
            model.setData(index, value, Qt.EditRole)
            return
        elif index.column() in [7, 8]:
            editor: QFileDialog
            files = editor.selectedFiles()
            if len(files) != 0:
                path = Path(files[0])
                if str(path).lower().startswith(str(config.ROOT_PATH).lower()):
                    value = str(path.relative_to(config.ROOT_PATH))
                else:
                    value = str(path)
                model.setData(index, value, Qt.EditRole)
            return
        super().setModelData(editor, model, index)


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
        self.resize(1200, 300)

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
        v.setItemDelegate(ItemDelegate(self))

        hh = v.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        hh.setSectionResizeMode(8, QHeaderView.Stretch)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        v.setStyleSheet(
            'QHeaderView {background-color: #333333; color: #cccccc; font-size: 12px;}'
            'QTableView::item::focus '
            '{border: 2px solid white; '
            'border-radius: 0px;border-bottom-right-radius: 0px;border-style: double;}'
        )
        # event

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.addButton.clicked.connect(self.add)
        self.ui.setButton.clicked.connect(self.save)

        self.ui.actionUndo.triggered.connect(self.ui.tableView.undo)
        self.ui.actionRedo.triggered.connect(self.ui.tableView.redo)
        self.ui.actionCopy.triggered.connect(self.ui.tableView.copy)
        self.ui.actionPaste.triggered.connect(self.ui.tableView.paste)
        self.ui.actionClear.triggered.connect(self.ui.tableView.clear)
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
        menu.addAction(self.ui.actionUndo)
        menu.addAction(self.ui.actionRedo)
        menu.addSeparator()
        menu.addAction(self.ui.actionCopy)
        menu.addAction(self.ui.actionPaste)
        menu.addAction(self.ui.actionClear)
        menu.addSeparator()
        menu.addAction(self.ui.actionUp)
        menu.addAction(self.ui.actionDown)
        menu.addSeparator()
        menu.addAction(self.ui.actionDelete)
        menu.exec_(v.mapToGlobal(pos))

    def set_comment(self, comment: str) -> None:
        self.ui.commentLabel.setText(comment)

    def set_data(self, a: CharaSetData) -> None:
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
            self.ui.tableView.model().undo_stack.clear()

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

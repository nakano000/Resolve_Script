from typing import (
    List,
)

import dataclasses
import re
import sys
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QItemSelectionModel,
    QModelIndex, QEvent, QThread,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QMainWindow,
    QPlainTextEdit,
    QMenu,
    QStyledItemDelegate,
)
from shiboken6 import Shiboken

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
    table,
)

from rs.tool.voicevox_sequencer.voicevox_sequencer_ui import Ui_MainWindow

APP_NAME = 'VoicevoxSequencer'


@dataclasses.dataclass
class ConfigData(config.Data):
    chara: str = 'れいむ'
    exe_path: str = ''
    voice_dir: str = ''


@dataclasses.dataclass
class VoiceData(table.RowData):
    note: int = ''
    vel: int = ''
    time: int = ''

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ['キャラ', '字幕', '読み']


@dataclasses.dataclass
class VoiceDataset(config.Data):
    voice_dir: str = ''
    voice_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(VoiceData))


class Model(table.Model):
    pass


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

    def createEditor(self, parent, option, index):
        if index.column() in (1, 2):
            return QPlainTextEdit(parent)
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if index.column() in (1, 2):
            editor: QPlainTextEdit
            value = index.model().data(index, Qt.DisplayRole)
            editor.clear()
            editor.insertPlainText(value)
            return
        super().setEditorData(editor, index)

    def eventFilter(self, editor, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            mod = event.modifiers()
            v = self._parent.ui.tableView
            if (
                    (key == Qt.Key_Escape and mod == Qt.NoModifier)
            ):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor)
                return True
            if (
                    (key in (Qt.Key_Down, Qt.Key_Up) and mod == Qt.NoModifier) or
                    (key in (Qt.Key_Tab, Qt.Key_Backtab) and mod == Qt.NoModifier)
            ):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor)
                v.keyPressEvent(event)
                v.edit(v.currentIndex())
                return True
            if (
                    (key == Qt.Key_Return and mod == Qt.ShiftModifier)
            ):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor)
                self._parent.add()
                v.edit(v.currentIndex())
                return True

        return super().eventFilter(editor, event)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.file = None
        self.set_title()
        self.setWindowFlags(
            Qt.Window
        )
        self.resize(800, 800)
        self.is_playing = False
        # config
        # self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        # self.load_config()

        # style sheet
        self.ui.saveButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.playButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.stopButton.setStyleSheet(appearance.other_stylesheet)

        # table
        v = self.ui.tableView
        v.setModel(Model(VoiceData))
        v.setItemDelegate(ItemDelegate(self))
        self.undo_stack = v.model().undo_stack

        h = v.horizontalHeader()
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        vh = v.verticalHeader()
        vh.setMinimumWidth(40)
        vh.setMinimumSectionSize(55)
        vh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        vh.setDefaultAlignment(Qt.AlignCenter)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        v.setStyleSheet(
            'QTableView::item::focus {'
            ' border: 2px solid white;'
            ' border-radius: 0px;'
            ' border-bottom-right-radius: 0px;'
            ' border-style: double;}'
        )

        self.new_doc()
        # thread
        self.player_thread = None
        self.player = None
        # event
        self.undo_stack.cleanChanged.connect(self.set_title)

        self.ui.folderToolButton.clicked.connect(self.folderToolButton_clicked)
        self.ui.exeToolButton.clicked.connect(self.exeToolButton_clicked)

        self.ui.playButton.clicked.connect(self.play)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.saveButton.clicked.connect(self.wave_save)
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.actionNew.triggered.connect(self.new_doc)
        self.ui.actionOpen.triggered.connect(self.open_doc)
        self.ui.actionSave.triggered.connect(self.save_doc)
        self.ui.actionSave_As.triggered.connect(self.save_as_doc)
        self.ui.actionImport_From_Clipboard.triggered.connect(self.import_from_clipboard)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.actionUndo.triggered.connect(self.undo_stack.undo)
        self.ui.actionRedo.triggered.connect(self.undo_stack.redo)

        self.ui.actionEdit.triggered.connect(self.edit)
        self.ui.actionAdd.triggered.connect(self.add)
        self.ui.actionClear.triggered.connect(self.ui.tableView.clear)
        self.ui.actionCopy.triggered.connect(self.ui.tableView.copy)
        self.ui.actionPaste.triggered.connect(self.ui.tableView.paste)
        self.ui.actionDelete.triggered.connect(self.ui.tableView.delete)
        self.ui.actionUp.triggered.connect(self.ui.tableView.up)
        self.ui.actionDown.triggered.connect(self.ui.tableView.down)

        self.ui.actionPlay.triggered.connect(self.play_or_stop)
        self.ui.actionWav_Save.triggered.connect(self.wave_save)

    def set_title(self):
        if self.file is None:
            self.setWindowTitle('%s' % APP_NAME)
        else:
            star = '*' if self.ui.tableView.model().undo_stack.isClean() is False else ''
            self.setWindowTitle('%s - %s%s' % (APP_NAME, self.file, star))

    def play(self):
        pass

    def play_state_off(self):
        self.is_playing = False

    def play_or_stop(self):
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def stop(self):
        pass

    def wave_save(self):
        pass

    def edit(self):
        v = self.ui.tableView
        v.edit(v.currentIndex())

    def contextMenu(self, pos):
        v = self.ui.tableView
        menu = QMenu(v)
        menu.addAction(self.ui.actionUndo)
        menu.addAction(self.ui.actionRedo)
        menu.addSeparator()
        menu.addAction(self.ui.actionEdit)
        menu.addAction(self.ui.actionClear)
        menu.addSeparator()
        menu.addAction(self.ui.actionCopy)
        menu.addAction(self.ui.actionPaste)
        menu.addSeparator()
        menu.addAction(self.ui.actionAdd)
        menu.addAction(self.ui.actionDelete)
        menu.addSeparator()
        menu.addAction(self.ui.actionUp)
        menu.addAction(self.ui.actionDown)
        menu.exec_(v.mapToGlobal(pos))

    def add(self):
        c = self.get_config()
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        row = v.currentIndex().row()
        col = v.currentIndex().column()
        d = VoiceData()
        if row < 0:
            d.chara = c.chara
            m.add_row_data(d)
        else:
            d.chara = m.get_row_data(row).chara
            m.insert_row_data(row + 1, d)
            index = m.index(row + 1, col, QModelIndex())
            sm.setCurrentIndex(index, QItemSelectionModel.SelectionFlag.ClearAndSelect)

    def folderToolButton_clicked(self) -> None:
        w = self.ui.folderLineEdit
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def set_data(self, a: VoiceDataset):
        self.ui.folderLineEdit.setText(a.voice_dir)
        self.ui.tableView.model().set_data(a.voice_list)

    def get_data(self) -> VoiceDataset:
        a = VoiceDataset()
        a.voice_dir = self.ui.folderLineEdit.text().strip()
        a.voice_list.set_list(self.ui.tableView.model().to_list())
        return a

    def new_doc(self):
        self.file = None
        v = self.ui.tableView
        m: Model = v.model()
        m.clear()
        self.add()
        self.undo_stack.clear()
        self.set_title()

    def open_doc(self):
        dir_path = ''
        if self.file is not None:
            dir_path = Path(self.file).parent
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            str(dir_path),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                a = self.get_data()
                a.load(file_path)
                self.set_data(a)
                # self.add2log('Open: %s' % str(file_path))
                self.file = str(file_path)
                self.undo_stack.clear()
                self.set_title()

    def save_doc(self):
        if self.file is None:
            self.save_as_doc()
            return
        file_path = Path(self.file)
        a = self.get_data()
        a.save(file_path)
        self.undo_stack.setClean()
        self.set_title()

    def save_as_doc(self):
        dir_path = ''
        if self.file is not None:
            dir_path = Path(self.file).parent
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            str(dir_path),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            a = self.get_data()
            a.save(file_path)
            # self.add2log('Save: %s' % str(file_path))
            self.file = str(file_path)
            self.undo_stack.setClean()
            self.set_title()

    def set_config(self, c: ConfigData):
        self.ui.charaLineEdit.setText(c.chara)
        self.ui.exeLineEdit.setText(c.exe_path)
        self.ui.folderLineEdit.setText(c.voice_dir)

    def get_config(self) -> ConfigData:
        c = ConfigData()
        c.chara = self.ui.charaLineEdit.text().strip()
        c.exe_path = self.ui.exeLineEdit.text().strip()
        c.voice_dir = self.ui.folderLineEdit.text().strip()
        return c

    def load_config(self) -> None:
        c = ConfigData()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_config(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_config()
        c.save(self.config_file)

    def closeEvent(self, event):
        self.save_config()
        self.stop()
        super().closeEvent(event)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

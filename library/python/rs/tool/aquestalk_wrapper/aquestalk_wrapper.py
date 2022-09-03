from typing import (
    List,
    Any,
)

import dataclasses
import re
import soundfile
import subprocess
import sys
from functools import partial
from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QDir,
    QItemSelectionModel,
    QModelIndex, QEvent, QThread,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QWidget,
    QHeaderView,
    QMainWindow, QItemDelegate, QLineEdit, QPlainTextEdit, QMenu, QStyledItemDelegate,
)
from shiboken2 import shiboken2

from rs.core import (
    config,
    pipe as p,
    srt,
    lab,
    util,
)
from rs.gui import (
    appearance,
    basic_table,
)

from rs.tool.aquestalk_wrapper import aquestalk
from rs.tool.aquestalk_wrapper.aquestalk_wrapper_ui import Ui_MainWindow

APP_NAME = 'AquestalkWrapper'


@dataclasses.dataclass
class ConfigData(config.Data):
    chara: str = 'れいむ'
    exe_path: str = ''
    voice_dir: str = ''


@dataclasses.dataclass
class VoiceData(basic_table.RowData):
    chara: str = ''
    subtitle: str = ''
    pronunciation: str = ''

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ['キャラ', '字幕', '読み']


@dataclasses.dataclass
class VoiceDataset(config.Data):
    voice_dir: str = ''
    voice_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(VoiceData))


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
            # | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(800, 800)
        self.is_playing = False
        self.exe_name = 'AquesTalkPlayer.exe'
        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # style sheet
        self.ui.saveButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.playButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.stopButton.setStyleSheet(appearance.other_stylesheet)

        # table
        v = self.ui.tableView
        v.setModel(Model(VoiceData))
        v.setItemDelegate(ItemDelegate(self))

        h = v.horizontalHeader()
        h.setSectionResizeMode(1, QHeaderView.Stretch)
        h.setSectionResizeMode(2, QHeaderView.Stretch)
        vh = v.verticalHeader()
        vh.setMinimumWidth(40)
        vh.setMinimumSectionSize(55)
        vh.setSectionResizeMode(QHeaderView.ResizeToContents)
        vh.setDefaultAlignment(Qt.AlignCenter)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        v.setStyleSheet(
            'QTableView::item::focus {border: 2px solid white; border-radius: 0px;border-bottom-right-radius: 0px;border-style: double;}'
        )

        self.new_doc()
        # thread
        self.player_thread = None
        self.player = None
        # event

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

        self.ui.actionCopy.triggered.connect(self.copy)
        self.ui.actionPaste.triggered.connect(self.paste)
        self.ui.actionEdit.triggered.connect(self.edit)
        self.ui.actionClear.triggered.connect(self.clear)
        self.ui.actionAdd.triggered.connect(self.add)
        self.ui.actionDelete.triggered.connect(self.delete)
        self.ui.actionUp.triggered.connect(self.up)
        self.ui.actionDown.triggered.connect(self.down)

        self.ui.actionPlay.triggered.connect(self.play_or_stop)
        self.ui.actionWav_Save.triggered.connect(self.wave_save)

    def set_title(self):
        if self.file is None:
            self.setWindowTitle('%s' % APP_NAME)
        else:
            self.setWindowTitle('%s  %s' % (APP_NAME, str(self.file)))

    def play(self):
        self.stop()

        # get data
        c = self.get_config()
        v = self.ui.tableView
        m: Model = v.model()

        # AquesTalkPlayer
        self.player = aquestalk.Player()
        self.player.exe_path = c.exe_path.strip()
        self.player.data = p.pipe(
            self.selected_rows(),
            p.map(m.get_row_data),
            p.map(lambda d: {
                'chara': d.chara.strip(),
                'text': d.subtitle.strip() if d.pronunciation.strip() == '' else d.pronunciation.strip(),
            }),
            p.filter(lambda d: d['chara'] != '' and d['text'] != ''),
            list,
        )
        if len(self.player.data) == 0:
            return

        # thread
        self.player_thread = QThread()
        self.player.moveToThread(self.player_thread)

        # event
        self.player_thread.started.connect(self.player.play)
        self.player.finished.connect(self.player_thread.quit)
        self.player.finished.connect(self.player.deleteLater)
        self.player.finished.connect(self.play_state_off, type=Qt.DirectConnection)
        self.player_thread.finished.connect(self.player_thread.deleteLater)

        # play
        self.is_playing = True
        self.player_thread.start()

    def play_state_off(self):
        self.is_playing = False

    def play_or_stop(self):
        if self.is_playing:
            self.stop()
        else:
            self.play()

    def stop(self):
        if self.player_thread and shiboken2.isValid(self.player_thread):
            if self.player_thread.isRunning():
                self.player.stop()
                self.player_thread.quit()
                self.player_thread.wait()
                self.is_playing = False

    def wave_save(self):
        # get data
        c = self.get_config()
        v = self.ui.tableView
        m: Model = v.model()

        # AquesTalkPlayer
        a = aquestalk.Player()
        a.exe_path = c.exe_path.strip()
        a.data = []
        for row in self.selected_rows():
            d: VoiceData = m.get_row_data(row)
            chara = d.chara.strip()
            subtitle = d.subtitle.strip()
            text = subtitle if d.pronunciation.strip() == '' else d.pronunciation.strip()
            if chara == '' or text == '':
                continue
            # filename
            name = '%03d_%s_%s' % (
                row + 1,
                chara,
                re.sub(r'[\\|/|:|?|.|"|<|>|\|]', '', text)[:9],
            )
            wav_file = Path(c.voice_dir).joinpath(name + '.wav')
            if wav_file.is_file():
                count = 0
                while True:
                    count += 1
                    wav_file = Path(c.voice_dir).joinpath(name + ('[%d].wav' % count))
                    if not wav_file.is_file():
                        break
            txt_file = Path(c.voice_dir).joinpath(wav_file.stem + '.txt')

            a.data.append({
                'chara': chara,
                'text': text,
                'subtitle': subtitle,
                'wav_file': wav_file,
                'txt_file': txt_file,
            })

        # export
        if len(a.data) == 0:
            return
        a.export()

    def selected_rows(self) -> List[int]:
        v = self.ui.tableView
        sm = v.selectionModel()
        return p.pipe(
            sm.selectedIndexes(),
            p.map(p.call.row()),
            set,
            list,
            sorted,
        )

    def edit(self):
        v = self.ui.tableView
        v.edit(v.currentIndex())

    def clear(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        for i in sm.selectedIndexes():
            m.setData(i, '', Qt.EditRole)
        return

    def contextMenu(self, pos):
        v = self.ui.tableView
        menu = QMenu(v)
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
            sm.setCurrentIndex(index, QItemSelectionModel.ClearAndSelect)

    def import_from_clipboard(self):
        c = self.get_config()
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        lines: list = p.pipe(
            QApplication.clipboard().text().splitlines(),
            list,
        )
        sm.clearSelection()
        for line in lines:
            d = VoiceData()
            d.chara = c.chara
            d.subtitle = line
            m.add_row_data(d)

    def delete(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        for row in reversed(self.selected_rows()):
            m.removeRow(row, QModelIndex())
        sm.clearSelection()

    def up(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        data_list = []
        min_row = None
        for row in reversed(self.selected_rows()):
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
        for row in reversed(self.selected_rows()):
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

    def select_rect(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        rows = p.pipe(
            sm.selectedIndexes(),
            p.map(p.call.row()),
            set,
            list,
            sorted,
        )
        cols = p.pipe(
            sm.selectedIndexes(),
            p.map(p.call.column()),
            set,
            list,
            sorted,
        )
        if len(rows) == 0 or len(cols) == 0:
            return None, None, None, None
        min_row = min(rows)
        min_col = min(cols)
        max_row = max(rows)
        max_col = max(cols)
        # select
        sm.clearSelection()
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                index = m.index(row, col, QModelIndex())
                sm.select(index, QItemSelectionModel.Select)
        return min_row, max_row, min_col, max_col

    def copy(self):
        self.select_rect()
        v = self.ui.tableView
        m: Model = v.model()

        min_row, max_row, min_col, max_col = self.select_rect()
        if min_row is None:
            return
        lines = []
        for row in range(min_row, max_row + 1):
            lst = []
            for col in range(min_col, max_col + 1):
                index = m.index(row, col, QModelIndex())
                s = str(m.get_value(index.row(), index.column())).replace('\n', '\\n')
                lst.append(s)
            lines.append('\t'.join(lst))
        QApplication.clipboard().setText('\n'.join(lines))

    def paste(self):
        v = self.ui.tableView
        m: Model = v.model()
        sm = v.selectionModel()
        ss: list = p.pipe(
            QApplication.clipboard().text().splitlines(),
            p.map(p.call.replace('\\n', '\n')),
            p.map(p.call.split('\t')),
            list,
        )
        if len(ss) == 0:
            ss.append([''])
        if len(ss) == 1 and len(ss[0]) == 1:
            for i in sm.selectedIndexes():
                m.setData(i, ss[0][0], Qt.EditRole)
            return

        c_row = v.currentIndex().row()
        c_col = v.currentIndex().column()
        if c_row < 0 or c_col < 0:
            return
        sm.clearSelection()
        for src_row in range(len(ss)):
            for src_col in range(len(ss[src_row])):
                row = c_row + src_row
                col = c_col + src_col
                if row > m.rowCount() - 1 or col > m.columnCount() - 1:
                    continue
                index = m.index(row, col, QModelIndex())
                m.setData(index, ss[src_row][src_col], Qt.EditRole)
                sm.select(index, QItemSelectionModel.Select)

    def exeToolButton_clicked(self) -> None:
        w = self.ui.exeLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select %s' % self.exe_name,
            w.text(),
            '%s(%s)' % (self.exe_name, self.exe_name),
        )
        if path != '':
            w.setText(path)

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
                self.set_title()

    def save_doc(self):
        if self.file is None:
            self.save_as_doc()
            return
        file_path = Path(self.file)
        a = self.get_data()
        a.save(file_path)

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
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

import dataclasses
from pathlib import Path

from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMenu, QStyledItemDelegate, QFileDialog


from rs.core import (
    pipe as p,
)
from rs.gui import (
    table,
)


@dataclasses.dataclass
class InputData(table.RowData):
    wav: str = ''
    lab: str = ''


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

    def createEditor(self, parent, option, index):
        if index.column() in [0, 1]:
            editor = QFileDialog(parent)
            editor.setWindowTitle('ファイル選択')
            editor.setFileMode(QFileDialog.ExistingFile)
            editor.setAcceptMode(QFileDialog.AcceptOpen)
            editor.setOptions(QFileDialog.DontUseNativeDialog)
            if index.column() == 0:
                editor.setNameFilter('WAV File (*.wav)')
            else:
                editor.setNameFilter('LAB File (*.lab)')
            return editor
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        if index.column() in [0, 1]:
            editor: QFileDialog
            path = Path(index.data(Qt.DisplayRole))
            editor.setDirectory(str(path.parent))
            return
        super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        if index.column() in [0, 1]:
            editor: QFileDialog
            files = editor.selectedFiles()
            if len(files) != 0:
                model.setData(index, files[0], Qt.EditRole)
            return
        super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        if index.column() in [0, 1]:
            pass
            return
        super().updateEditorGeometry(editor, option, index)


class Model(table.Model):
    pass


class View(table.View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(Model(InputData))
        self.setItemDelegate(ItemDelegate(self))
        self.setStyleSheet(
            'QTableView::item::focus '
            '{border: 2px solid white; '
            'border-radius: 0px;border-bottom-right-radius: 0px;border-style: double;}'
        )

        # context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        # action
        self.actionUndo = QAction('Undo', self)
        self.actionUndo.setShortcut(QKeySequence('Ctrl+Z'))
        self.actionRedo = QAction('Redo', self)
        self.actionRedo.setShortcut(QKeySequence('Ctrl+Shift+Z'))
        self.actionCopy = QAction('Copy', self)
        self.actionCopy.setShortcut(QKeySequence('Ctrl+C'))
        self.actionPaste = QAction('Paste', self)
        self.actionPaste.setShortcut(QKeySequence('Ctrl+V'))
        self.actionDelete = QAction('Delete', self)
        self.actionDelete.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Delete))
        self.actionUp = QAction('Up', self)
        self.actionUp.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Up))
        self.actionDown = QAction('Down', self)
        self.actionDown.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Down))
        # event
        self.actionUndo.triggered.connect(self.model().undo_stack.undo)
        self.actionRedo.triggered.connect(self.model().undo_stack.redo)
        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionDelete.triggered.connect(self.delete)
        self.actionUp.triggered.connect(self.up)
        self.actionDown.triggered.connect(self.down)

    def add(self, wav: str, lab: str):
        m: Model = self.model()
        m.add_row_data(InputData(wav=wav, lab=lab))

    def get_wav_list(self):
        m: Model = self.model()
        return p.pipe(
            m.to_list(),
            p.map(lambda row: Path(row.wav)),
            list,
        )

    def get_lab_list(self):
        m: Model = self.model()
        return p.pipe(
            m.to_list(),
            p.map(lambda row: Path(row.lab)),
            list,
        )

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()
        if mod == Qt.ControlModifier and key == Qt.Key_Z:
            self.actionUndo.trigger()
            return
        if mod == Qt.ControlModifier | Qt.ShiftModifier and key == Qt.Key_Z:
            self.actionRedo.trigger()
            return
        if mod == Qt.ControlModifier and key == Qt.Key_C:
            self.actionCopy.trigger()
            return
        if mod == Qt.ControlModifier and key == Qt.Key_V:
            self.actionPaste.trigger()
            return
        if mod == Qt.ControlModifier and key == Qt.Key_Delete:
            self.actionDelete.trigger()
            return
        if mod == Qt.AltModifier and key == Qt.Key_Up:
            self.actionUp.trigger()
            return
        if mod == Qt.AltModifier and key == Qt.Key_Down:
            self.actionDown.trigger()
            return

        super().keyPressEvent(event)

    def contextMenu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.actionUndo)
        menu.addAction(self.actionRedo)
        menu.addSeparator()
        menu.addAction(self.actionCopy)
        menu.addAction(self.actionPaste)
        menu.addSeparator()
        menu.addAction(self.actionUp)
        menu.addAction(self.actionDown)
        menu.addSeparator()
        menu.addAction(self.actionDelete)
        menu.exec_(self.mapToGlobal(pos))

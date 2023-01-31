from typing import List

import dataclasses
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMenu, QStyledItemDelegate

from rs.gui import (
    table,
)


@dataclasses.dataclass
class InputData(table.RowData):
    node: str = ''
    page: str = ''
    id: str = ''
    name: str = ''
    control_group: int = 0
    option01: str = ''
    option02: str = ''
    option03: str = ''

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ['Node', 'Page', 'ID', 'Name', 'CtrlGrp', 'Option01', 'Option02', 'Option03']


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent


class Model(table.Model):
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            if index.column() not in [3, 5, 6, 7]:  # name,option以外は編集不可
                return Qt.ItemIsEnabled | Qt.ItemIsSelectable
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.NoItemFlags


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

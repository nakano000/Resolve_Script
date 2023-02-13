import operator
import re
from typing import List

import dataclasses
from PySide2.QtCore import Qt, QModelIndex
from PySide2.QtGui import QKeySequence, QColor, QBrush, QPen
from PySide2.QtWidgets import QAction, QMenu, QStyledItemDelegate, QHeaderView, QStyle

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    table,
)


@dataclasses.dataclass
class ColorData(table.RowData):
    name: str = ''
    color00: str = '#000000'
    color01: str = '#000000'
    color02: str = '#000000'
    color03: str = '#000000'
    color04: str = '#000000'

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ['Name', 'C00', 'C01', 'C02', 'C03', 'C04', ]


class ItemDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

    def paint(self, painter, option, index):
        color = index.data(Qt.BackgroundRole)
        if color is not None:
            bgBrush = QBrush(color)
            bgPen = QPen(color, 0.5, Qt.SolidLine)
            painter.setPen(bgPen)
            painter.setBrush(bgBrush)
            rect = option.rect
            if option.state & QStyle.State_Selected:
                rect.setX(rect.x() + 1)
                rect.setY(rect.y() + 1)
                rect.setWidth(rect.width() - 2)
                rect.setHeight(rect.height() - 2)
            painter.drawRect(option.rect)
        super().paint(painter, option, index)


class Model(table.Model):
    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if role == Qt.BackgroundRole:
            row = index.row()
            col = index.column()
            if col > 0:
                color = self.get_value(row, col)
                return QColor(color)
        return super().data(index, role)

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            col = index.column()
            if col > 0:
                if re.match(r'^#[0-9a-fA-F]{6}$', value):
                    self.undo_stack.push(table.model.SetDataCommand(self, index, value))
                    return True
        return super().setData(index, value, role)


class View(table.View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(Model(ColorData))
        self.setItemDelegate(ItemDelegate(self))
        self.setStyleSheet(
            'QTableView::item::selected '
            '{border: 2px solid white; '
            'border-radius: 0px;border-bottom-right-radius: 0px;border-style: dashed;}'
            'QTableView::item::focus '
            '{border: 4px solid white; '
            'border-radius: 0px;border-bottom-right-radius: 0px;border-style: solid;}'
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
        self.actionAdd = QAction('Add', self)
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
        self.actionAdd.triggered.connect(self.add_row)
        self.actionDelete.triggered.connect(self.delete)
        self.actionUp.triggered.connect(self.up)
        self.actionDown.triggered.connect(self.down)

    def add_row(self):
        self.model().add_row_data(ColorData())
        self.scrollToBottom()

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
        menu.addAction(self.actionAdd)
        menu.addAction(self.actionDelete)
        menu.exec_(self.mapToGlobal(pos))

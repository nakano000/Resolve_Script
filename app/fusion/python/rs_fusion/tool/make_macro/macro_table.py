from PySide2.QtCore import Qt
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMenu

from rs.gui import (
    basic_table,
)


class View(basic_table.View):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        # action
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
        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionDelete.triggered.connect(self.delete)
        self.actionUp.triggered.connect(self.up)
        self.actionDown.triggered.connect(self.down)

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()
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
        menu.addAction(self.actionCopy)
        menu.addAction(self.actionPaste)
        menu.addSeparator()
        menu.addAction(self.actionUp)
        menu.addAction(self.actionDown)
        menu.addSeparator()
        menu.addAction(self.actionDelete)
        menu.exec_(self.mapToGlobal(pos))

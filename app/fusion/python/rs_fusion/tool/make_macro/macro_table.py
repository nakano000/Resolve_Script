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
        # self.actionCopy.setShortcut(QKeySequence('Ctrl+C'))
        self.actionDelete = QAction('Delete', self)
        self.actionUp = QAction('Up', self)
        self.actionDown = QAction('Down', self)
        # event
        self.actionCopy.triggered.connect(self.copy)
        self.actionDelete.triggered.connect(self.delete)
        self.actionUp.triggered.connect(self.up)
        self.actionDown.triggered.connect(self.down)

    def contextMenu(self, pos):
        menu = QMenu(self)
        menu.addAction(self.actionCopy)
        menu.addSeparator()
        menu.addAction(self.actionUp)
        menu.addAction(self.actionDown)
        menu.addSeparator()
        menu.addAction(self.actionDelete)
        menu.exec_(self.mapToGlobal(pos))

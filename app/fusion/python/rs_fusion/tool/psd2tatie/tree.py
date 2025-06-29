from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QStandardItemModel,
    QKeySequence,
)
from PySide6.QtWidgets import (
    QAction,
    QComboBox,
    QMenu,
    QStyledItemDelegate,
    QTreeView,
)


class TreeModel(QStandardItemModel):
    def data(self, index, role=Qt.DisplayRole):
        if index.column() == 3:
            if role == Qt.TextAlignmentRole:
                return Qt.AlignCenter | Qt.AlignVCenter
        return super(TreeModel, self).data(index, role)


# class TreeDelegate(QStyledItemDelegate):
#     def __init__(self, parent):
#         super(TreeDelegate, self).__init__(parent)
#         self._parent = parent
#
#     def setModelData(self, editor, model, index):
#         super(TreeDelegate, self).setModelData(editor, model, index)


class TreeView(QTreeView):
    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setModel(TreeModel())
        # self.setItemDelegateForColumn(3, TreeDelegate(self))
        self.hideColumn(1)

        # context menu
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.contextMenu)
        # # action
        # self.actionCopyComment = QAction('Copy Comment', self)
        # self.actionCopyComment.setShortcut(QKeySequence('Ctrl+C'))

    # def keyPressEvent(self, event):
    #     key = event.key()
    #     mod = event.modifiers()
    #
    #     if mod == Qt.ControlModifier and key == Qt.Key_C:
    #         self.actionCopyComment.trigger()
    #         return
    #
    #     super(TreeView, self).keyPressEvent(event)
    #
    # def contextMenu(self, pos):
    #     menu = QMenu(self)
    #     menu.addAction(self.actionCopyComment)
    #     menu.exec_(self.mapToGlobal(pos))

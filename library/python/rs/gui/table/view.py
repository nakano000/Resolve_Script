from typing import List

from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QItemSelectionModel,
)

from PySide2.QtWidgets import QTableView, QApplication

from rs.core import (
    pipe as p,
)
from rs.gui.table import Model


class View(QTableView):

    def undo(self):
        self.model().undo_stack.undo()

    def redo(self):
        self.model().undo_stack.redo()

    def selected_rows(self) -> List[int]:
        sm = self.selectionModel()
        return p.pipe(
            sm.selectedIndexes(),
            p.map(p.call.row()),
            set,
            list,
            sorted,
        )

    def clear(self):
        m: Model = self.model()
        sm = self.selectionModel()
        m.undo_stack.beginMacro('Clear')
        for i in sm.selectedIndexes():
            m.setData(i, '', Qt.EditRole)
        m.undo_stack.endMacro()

    def delete(self):
        m: Model = self.model()
        sm = self.selectionModel()
        m.undo_stack.beginMacro('Delete')
        for row in reversed(self.selected_rows()):
            m.removeRow(row, QModelIndex())
        m.undo_stack.endMacro()
        sm.clearSelection()

    def up(self):
        m: Model = self.model()
        sm = self.selectionModel()
        data_list = []
        min_row = None
        m.undo_stack.beginMacro('Up')
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
        m.undo_stack.endMacro()

    def down(self):
        m: Model = self.model()
        sm = self.selectionModel()
        data_list = []
        max_row = None
        m.undo_stack.beginMacro('Down')
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
        m.undo_stack.endMacro()

    def select_rect(self):
        m: Model = self.model()
        sm = self.selectionModel()
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
        m: Model = self.model()

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
        m: Model = self.model()
        sm = self.selectionModel()
        ss: list = p.pipe(
            QApplication.clipboard().text().splitlines(),
            p.map(p.call.replace('\\n', '\n')),
            p.map(p.call.split('\t')),
            list,
        )
        if len(ss) == 0:
            ss.append([''])
        if len(ss) == 1 and len(ss[0]) == 1:
            m.undo_stack.beginMacro('Paste')
            for i in sm.selectedIndexes():
                if i.flags() & Qt.ItemIsEditable:
                    m.setData(i, ss[0][0], Qt.EditRole)
            m.undo_stack.endMacro()
            return

        c_row = self.currentIndex().row()
        c_col = self.currentIndex().column()
        if c_row < 0 or c_col < 0:
            return
        sm.clearSelection()
        m.undo_stack.beginMacro('Paste')
        for src_row in range(len(ss)):
            for src_col in range(len(ss[src_row])):
                row = c_row + src_row
                col = c_col + src_col
                if row > m.rowCount() - 1 or col > m.columnCount() - 1:
                    continue
                index = m.index(row, col, QModelIndex())
                if index.flags() & Qt.ItemIsEditable:
                    m.setData(index, ss[src_row][src_col], Qt.EditRole)
                sm.select(index, QItemSelectionModel.Select)
        m.undo_stack.endMacro()


if __name__ == '__main__':
    pass

import dataclasses
import operator
from typing import List

from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel, QItemSelectionModel,
)

from PySide2.QtWidgets import QTableView, QApplication

from rs.core import (
    config,
    pipe as p,
)


@dataclasses.dataclass
class RowData(config.DataInterface):

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return p.pipe(
            dataclasses.fields(cls),
            p.map(p.get.name),
            list,
        )

    def set_value(self, i: int, value) -> bool:
        attr_name, attr_type = p.pipe(
            dataclasses.fields(self),
            p.map(lambda x: (x.name, x.type)),
            list,
            operator.itemgetter(i),
        )
        if attr_type == int:
            try:
                v = int(value)
                setattr(self, attr_name, v)
                return True
            except ValueError:
                pass
        elif attr_type == float:
            try:
                v = float(value)
                setattr(self, attr_name, v)
                return True
            except ValueError:
                pass
        elif attr_type == str:
            v = str(value)
            setattr(self, attr_name, v)
            return True
        return False

    def get_value(self, i):
        attr_name = p.pipe(
            dataclasses.fields(self),
            p.map(p.get.name),
            list,
            operator.itemgetter(i),
        )
        return getattr(self, attr_name)


class Model(QAbstractTableModel):
    def __init__(self, cls, parent=None):
        super().__init__(parent)
        self._data: config.DataList = config.DataList(cls)

    def add_row_data(self, row_data):
        i = len(self._data)
        self.beginInsertRows(QModelIndex(), i, i)
        self._data.append(row_data)
        self.endInsertRows()
        return False

    def insert_row_data(self, i: int, row_data):
        self.insert_rows_data(i, [row_data])
        return False

    def insert_rows_data(self, i: int, row_data_list):
        count = len(row_data_list)
        self.beginInsertRows(QModelIndex(), i, i + count - 1)
        self._data[i: i] = row_data_list
        self.endInsertRows()
        return False

    def get_row_data(self, row: int):
        return self._data[row]

    def get_value(self, row: int, col: int):
        return self._data[row].get_value(col)

    def to_list(self):
        return self._data.to_list()

    def set_list(self, lst):
        self.beginResetModel()
        self._data.set_list(lst)
        self.endResetModel()

    def set_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()

    def clear(self):
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self._data.new_data().toHeaderList())

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._data.new_data().toHeaderList()[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)

            return ''  # 垂直は表示しない

    def setData(self, index: QModelIndex, value, role: int = Qt.DisplayRole) -> bool:
        if index.isValid() and role == Qt.EditRole:
            r = self._data[index.row()].set_value(index.column(), value)
            self.dataChanged.emit(index, index)
            return r
        return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
        return Qt.NoItemFlags

    def insertRow(self, row: int, parent: QModelIndex = ...) -> bool:
        return self.insert_row_data(row, self._data.new_data())

    def insertRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        return self.insert_rows_data(row, p.pipe(
            range(count),
            p.map(lambda _: self._data.new_data()),
            list,
        ))

    def removeRow(self, row: int, parent: QModelIndex = ...) -> bool:
        r: bool = False
        self.beginRemoveRows(parent, row, row)
        try:
            del self._data[row]
            r = True
        except IndexError:
            pass
        self.endRemoveRows()
        return r

    def removeRows(self, row: int, count: int, parent: QModelIndex = ...) -> bool:
        r: bool = False
        self.beginRemoveRows(parent, row, row + count - 1)
        try:
            del self._data[row: row + count]
            r = True
        except IndexError:
            pass
        self.endRemoveRows()
        return r


class View(QTableView):
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
        for i in sm.selectedIndexes():
            m.setData(i, '', Qt.EditRole)
        return

    def delete(self):
        m: Model = self.model()
        sm = self.selectionModel()
        for row in reversed(self.selected_rows()):
            m.removeRow(row, QModelIndex())
        sm.clearSelection()

    def up(self):
        m: Model = self.model()
        sm = self.selectionModel()
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
        m: Model = self.model()
        sm = self.selectionModel()
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
            for i in sm.selectedIndexes():
                m.setData(i, ss[0][0], Qt.EditRole)
            return

        c_row = self.currentIndex().row()
        c_col = self.currentIndex().column()
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


if __name__ == '__main__':
    pass

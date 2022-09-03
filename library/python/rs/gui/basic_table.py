import dataclasses
import operator

from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel,
)
from typing import List

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


if __name__ == '__main__':
    pass

import copy

import dataclasses
import operator
from typing import List

from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QAbstractTableModel,
)

from PySide2.QtWidgets import (
    QUndoStack,
    QUndoCommand,
)

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


class SetDataCommand(QUndoCommand):
    def __init__(self, model, index: QModelIndex, value):
        super().__init__()
        self.model = model
        self.index = index
        self.row = index.row()
        self.col = index.column()
        self.value = value
        self.old_value = model.get_value(self.row, self.col)

    def redo(self):
        self.setObsolete(
            not self.model.data_list[self.row].set_value(self.col, self.value)
        )
        self.model.dataChanged.emit(self.index, self.index)

    def undo(self):
        self.model.data_list[self.row].set_value(self.col, self.old_value)
        self.model.dataChanged.emit(self.index, self.index)


class InsertRowsCommand(QUndoCommand):
    def __init__(self, model, row, rows_data):
        super().__init__()
        self.model = model
        self.row = row
        self.rows_data = copy.deepcopy(rows_data)
        self.count = len(self.rows_data)

    def redo(self):
        self.model.beginInsertRows(QModelIndex(), self.row, self.row + self.count - 1)
        self.model.data_list[self.row: self.row] = self.rows_data
        self.model.endInsertRows()

    def undo(self):
        self.model.beginRemoveRows(QModelIndex(), self.row, self.row + self.count - 1)
        del self.model.data_list[self.row: self.row + self.count]
        self.model.endRemoveRows()


class RemoveRowsCommand(QUndoCommand):
    def __init__(self, model, row, count):
        super().__init__()
        self.model = model
        self.row = row
        self.count = count
        self.rows_data = copy.deepcopy(model.data_list[row:row + count])

    def redo(self):
        self.model.beginRemoveRows(QModelIndex(), self.row, self.row + self.count - 1)
        del self.model.data_list[self.row: self.row + self.count]
        self.model.endRemoveRows()

    def undo(self):
        self.model.beginInsertRows(QModelIndex(), self.row, self.row + self.count - 1)
        self.model.data_list[self.row: self.row] = self.rows_data
        self.model.endInsertRows()


class SetDataListCommand(QUndoCommand):
    def __init__(self, model, data_list):
        super().__init__()
        self.model = model
        self.data_list = copy.deepcopy(data_list)
        self.old_data_list = copy.deepcopy(model.data_list)

    def redo(self):
        self.model.beginResetModel()
        self.model.data_list = self.data_list
        self.model.endResetModel()

    def undo(self):
        self.model.beginResetModel()
        self.model.data_list = self.old_data_list
        self.model.endResetModel()


class Model(QAbstractTableModel):
    def __init__(self, cls, parent=None):
        super().__init__(parent)
        self.data_list: config.DataList = config.DataList(cls)
        self.header_list: List[str] = cls.toHeaderList()
        self.row_cls = cls
        self.undo_stack = QUndoStack()
        self.undo_stack.setUndoLimit(400)

    def get_value(self, row: int, col: int):
        return self.data_list[row].get_value(col)

    def to_list(self):
        return self.data_list.to_list()

    def clear(self):
        self.undo_stack.push(SetDataListCommand(self, config.DataList(self.row_cls)))

    def set_data(self, data_list: config.DataList):
        self.undo_stack.push(SetDataListCommand(self, data_list))

    def get_row_data(self, row: int):
        return self.data_list[row]

    def insert_row_data(self, row: int, row_data):
        self.insert_rows_data(row, [row_data])

    def insert_rows_data(self, row: int, rows_data):
        self.undo_stack.push(InsertRowsCommand(self, row, rows_data))

    def add_row_data(self, row_data):
        self.insert_row_data(len(self.data_list), row_data)

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.data_list)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.header_list)

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            return self.get_value(row, col)
        return None

    def setData(self, index: QModelIndex, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            self.undo_stack.push(SetDataCommand(self, index, value))
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.header_list[section]
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def flags(self, index: QModelIndex):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def insertRow(self, row: int, parent=QModelIndex()):
        self.insert_row_data(row, self.row_cls())
        return True

    def insertRows(self, row: int, count: int, parent=QModelIndex()):
        self.undo_stack.push(InsertRowsCommand(self, row, [self.row_cls()] * count))
        return True

    def removeRow(self, row: int, parent=QModelIndex()):
        self.undo_stack.push(RemoveRowsCommand(self, row, 1))
        return True

    def removeRows(self, row: int, count: int, parent=QModelIndex()):
        self.undo_stack.push(RemoveRowsCommand(self, row, count))
        return True

    def appendRow(self, parent=QModelIndex()):
        self.insertRow(self.rowCount(), parent)


if __name__ == '__main__':
    pass

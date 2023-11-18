import dataclasses
from enum import Enum
from typing import Optional, List

import pykakasi

from PySide6.QtCore import (
    QModelIndex,
    QItemSelectionModel,
    Qt,
    QEvent,
    QSize, QSignalBlocker,
)
from PySide6.QtGui import QIcon, QColor, QKeyEvent
from PySide6.QtWidgets import (
    QAbstractItemDelegate,
    QLineEdit,
    QStyledItemDelegate, QHeaderView,
)

from rs.core import (
    config,
    note,
    pipe as p,
)
from rs.gui import table

LENGTH_LIST = [
    2880,
    1920,
    1440,
    960,
    720,
    480,
    360,
    240,
    180,
    120,
    90,
    60,
    45,
    30,
    0,
]


@dataclasses.dataclass
class NoteData(table.RowData):
    note: int = 60
    length: int = 480
    max_time: float = 0.5
    kana: str = 'ラ'

    def get_sec(self, tempo: int) -> float:
        # 480 = 1拍
        return self.length / (tempo * 480 / 60)

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return [
            'Note',
            'Length',
            'Limit(sec)',
            'Kana',
        ]


class Model(table.Model):
    def __init__(self, cls, parent=None):
        super().__init__(cls, parent)
        icon_dir = config.ROOT_PATH.joinpath('data', 'image', 'icon', 'notes')
        # note icon
        self.note_default_icon = QIcon(str(icon_dir.joinpath('question.png')))
        self.note_icon_dict = {
            2880: QIcon(str(icon_dir.joinpath('2880.png'))),
            1920: QIcon(str(icon_dir.joinpath('1920.png'))),
            1440: QIcon(str(icon_dir.joinpath('1440.png'))),
            960: QIcon(str(icon_dir.joinpath('960.png'))),
            720: QIcon(str(icon_dir.joinpath('720.png'))),
            480: QIcon(str(icon_dir.joinpath('480.png'))),
            360: QIcon(str(icon_dir.joinpath('360.png'))),
            240: QIcon(str(icon_dir.joinpath('240.png'))),
            180: QIcon(str(icon_dir.joinpath('180.png'))),
            120: QIcon(str(icon_dir.joinpath('120.png'))),
            90: QIcon(str(icon_dir.joinpath('90.png'))),
            60: QIcon(str(icon_dir.joinpath('60.png'))),
            45: QIcon(str(icon_dir.joinpath('45.png'))),
            30: QIcon(str(icon_dir.joinpath('30.png'))),
        }

        # rest icon
        self.rest_default_icon = QIcon(str(icon_dir.joinpath('empty.png')))
        self.rest_icon_dict = {
            2880: QIcon(str(icon_dir.joinpath('r2880.png'))),
            1920: QIcon(str(icon_dir.joinpath('r1920.png'))),
            1440: QIcon(str(icon_dir.joinpath('r1440.png'))),
            960: QIcon(str(icon_dir.joinpath('r960.png'))),
            720: QIcon(str(icon_dir.joinpath('r720.png'))),
            480: QIcon(str(icon_dir.joinpath('r480.png'))),
            360: QIcon(str(icon_dir.joinpath('r360.png'))),
            240: QIcon(str(icon_dir.joinpath('r240.png'))),
            180: QIcon(str(icon_dir.joinpath('r180.png'))),
            120: QIcon(str(icon_dir.joinpath('r120.png'))),
            90: QIcon(str(icon_dir.joinpath('r90.png'))),
            60: QIcon(str(icon_dir.joinpath('r60.png'))),
        }

    def data(self, index: QModelIndex, role: int = ...) -> Optional[str]:
        if role == Qt.DisplayRole:
            if index.column() == 0:
                note_index = self.get_value(index.row(), 0)
                if note_index < 0:
                    return '----  ----'
                return f'{note.index2name(note_index): <4}  {str(note_index): <4}'
            elif index.column() == 2:
                return f'  {self.get_value(index.row(), 2)}'
            elif index.column() == 3:
                note_index = self.get_value(index.row(), 0)
                if note_index < 0:
                    return f'----  {self.get_value(index.row(), 3)}'

        elif role == Qt.BackgroundRole:
            note_index = self.get_value(index.row(), 0)
            length = self.get_value(index.row(), 1)
            if note_index < 0 and length == 0:
                return QColor(100, 100, 100)

        elif role == Qt.DecorationRole:
            if index.column() == 1:
                is_rest = self.get_value(index.row(), 0) < 0
                length = self.get_value(index.row(), 1)
                if is_rest:
                    if length in self.rest_icon_dict:
                        return self.rest_icon_dict[length]
                    return self.rest_default_icon
                else:
                    if length in self.note_icon_dict:
                        return self.note_icon_dict[length]
                    return self.note_default_icon

        return super().data(index, role)


class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.org_text = None


class ItemDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        editor = LineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        v = self.parent()
        m: Model = v.model()
        text = str(m.get_value(index.row(), index.column())).strip()
        editor.setText(text)
        editor.org_text = text

    def setModelData(self, editor, model, index):
        col = index.column()
        _value = editor.text().strip()
        # noteの文字を数値に変換
        if col == 0:
            try:
                _value = str(int(_value))
            except ValueError:
                v = self.parent()
                if _value[-1] not in '0123456789':
                    _value = _value + str(v.octave)
                _value = str(note.name2index(_value))
        # kanaの文字をカタカナに変換
        elif col == 3:
            kks = pykakasi.kakasi()
            _value = kks.convert(_value)[0]['kana']
        # 変更が場合は何もしない
        if editor.org_text == _value:
            editor.org_text = None
            return

        # 値を反映
        if col in [0, 1]:
            try:
                value = int(_value)
                model.setData(index, value)
                editor.org_text = None
                return
            except ValueError:
                return
        elif col in [2]:
            try:
                value = float(_value)
                model.setData(index, value)
                editor.org_text = None
                return
            except ValueError:
                return
        elif col == 3:
            try:
                model.setData(index, _value)
                editor.org_text = None
                return
            except ValueError:
                return
        model.setData(index, editor.text())

    def eventFilter(self, editor, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            mod = event.modifiers()
            v = self.parent()
            m: Model = v.model()
            sm = v.selectionModel()
            if (
                    (key == Qt.Key_Escape and mod == Qt.NoModifier)
            ):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor)
                return True
            if (
                    (key in (Qt.Key_Down, Qt.Key_Up) and mod == Qt.NoModifier) or
                    (key in (Qt.Key_Tab, Qt.Key_Backtab) and mod == Qt.NoModifier)
            ):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor)
                v.keyPressEvent(event)
                v.edit(v.currentIndex())
                return True
            if (
                    (key == Qt.Key_Return and mod == Qt.NoModifier)
            ):
                self.commitData.emit(editor)
                self.closeEditor.emit(editor)
                current_index: QModelIndex = v.currentIndex()
                row = current_index.row()

                if row == m.rowCount() - 1:
                    d = NoteData()
                    m.insert_row_data(row + 1, d)
                sm.setCurrentIndex(
                    current_index.siblingAtRow(row + 1),
                    QItemSelectionModel.SelectionFlag.ClearAndSelect
                )
                v.edit(v.currentIndex())
                return True
            if (
                    (key == Qt.Key_Return and mod == Qt.ShiftModifier)
            ):
                m.undo_stack.beginMacro('Commit')
                m.undo_stack.endMacro()
                v.keyPressEvent(event)
                v.edit(v.currentIndex())
                return True

        return super().eventFilter(editor, event)

    def commitAndCloseEditor(self):
        print('commitAndCloseEditor', flush=True)
        editor = self.sender()
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, QAbstractItemDelegate.NoHint)


@dataclasses.dataclass
class Paragraph:
    start: int = 0
    end: int = 0
    note_list: List[NoteData] = dataclasses.field(default_factory=list)
    rest_length: int = 0

    def in_paragraph(self, row: int):
        return self.start <= row < self.end

    def get_text(self):
        return ''.join([x.kana for x in self.note_list])

    def get_rest_sec(self, tempo: int) -> float:
        return self.rest_length / (tempo * 480 / 60)


class View(table.View):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModel(Model(NoteData))
        self.setItemDelegate(ItemDelegate(self))
        self.undo_stack = self.model().undo_stack

        self.setIconSize(QSize(32, 32))

        self.setStyleSheet(
            'QTableView::item::focus {'
            ' border: 2px solid white;'
            ' border-radius: 0px;'
            ' border-bottom-right-radius: 0px;'
            ' border-style: double;}'
        )

        # h = self.horizontalHeader()
        # h.setSectionHidden(0, True)
        # h.setSectionHidden(1, True)
        # h.setSectionHidden(2, True)
        # h.setSectionHidden(3, True)
        # h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # h.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        vh = self.verticalHeader()
        vh.setMinimumWidth(40)
        vh.setMinimumSectionSize(55)
        vh.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        vh.setDefaultAlignment(Qt.AlignCenter)

        # ---------------------
        self.octave = 4

    def undo(self):
        m = self.model()
        with QSignalBlocker(m):
            self.undo_stack.undo()
        self.viewport().update()

    def redo(self):
        m = self.model()
        with QSignalBlocker(m):
            self.undo_stack.redo()
        self.viewport().update()

    def paste(self):
        m: Model = self.model()
        with QSignalBlocker(m):
            super().paste()
        self.viewport().update()

    def set_octave(self, octave: int):
        self.octave = octave

    def decrement(self):
        m: Model = self.model()
        sm = self.selectionModel()
        with QSignalBlocker(m):
            m.undo_stack.beginMacro('Decrement')
            for i in sm.selectedIndexes():
                col = i.column()
                if col == 0:
                    v = m.get_value(i.row(), i.column())
                    if v < 0:
                        continue
                    if v > 0:
                        m.setData(i, v - 1, Qt.EditRole)
                elif col == 1:
                    v = m.get_value(i.row(), i.column())
                    for length in LENGTH_LIST:
                        if length < v:
                            m.setData(i, length, Qt.EditRole)
                            break
                elif col == 2:
                    v = m.get_value(i.row(), i.column())
                    if v > 0.1:
                        m.setData(i, v - 0.1, Qt.EditRole)
            m.undo_stack.endMacro()
        self.viewport().update()

    def decrement_plus(self):
        m: Model = self.model()
        sm = self.selectionModel()
        with QSignalBlocker(m):
            m.undo_stack.beginMacro('DecrementPlus')
            for i in sm.selectedIndexes():
                col = i.column()
                if col == 0:
                    v = m.get_value(i.row(), i.column())
                    if v < 0:
                        continue
                    if v >= 12:
                        m.setData(i, v - 12, Qt.EditRole)
                elif col == 1:
                    v = m.get_value(i.row(), i.column())
                    for length in LENGTH_LIST:
                        if length < v:
                            v = length
                            break
                    for length in LENGTH_LIST:
                        if length < v:
                            m.setData(i, length, Qt.EditRole)
                            break
                elif col == 2:
                    v = m.get_value(i.row(), i.column())
                    if v > 0.5:
                        m.setData(i, v - 0.5, Qt.EditRole)
            m.undo_stack.endMacro()
        self.viewport().update()

    def increment(self):
        m: Model = self.model()
        sm = self.selectionModel()
        with QSignalBlocker(m):
            m.undo_stack.beginMacro('Increment')
            for i in sm.selectedIndexes():
                col = i.column()
                if col == 0:
                    v = m.get_value(i.row(), i.column())
                    if v < 0:
                        continue
                    m.setData(i, v + 1, Qt.EditRole)
                elif col == 1:
                    v = m.get_value(i.row(), i.column())
                    for length in reversed(LENGTH_LIST):
                        if length > v:
                            m.setData(i, length, Qt.EditRole)
                            break
                elif col == 2:
                    v = m.get_value(i.row(), i.column())
                    m.setData(i, v + 0.1, Qt.EditRole)
            m.undo_stack.endMacro()
        self.viewport().update()

    def increment_plus(self):
        m: Model = self.model()
        sm = self.selectionModel()
        with QSignalBlocker(m):
            m.undo_stack.beginMacro('IncrementPlus')
            for i in sm.selectedIndexes():
                col = i.column()
                if col == 0:
                    v = m.get_value(i.row(), i.column())
                    if v < 0:
                        continue
                    m.setData(i, v + 12, Qt.EditRole)
                elif col == 1:
                    v = m.get_value(i.row(), i.column())
                    for length in reversed(LENGTH_LIST):
                        if length > v:
                            v = length
                            break
                    for length in reversed(LENGTH_LIST):
                        if length > v:
                            m.setData(i, length, Qt.EditRole)
                            break
                elif col == 2:
                    v = m.get_value(i.row(), i.column())
                    m.setData(i, v + 0.5, Qt.EditRole)
            m.undo_stack.endMacro()
        self.viewport().update()

    def get_paragraph_list(self):
        m: Model = self.model()
        row_count = m.rowCount()
        lst = m.to_list()

        # ブロックの先頭の行番号のリストを作成
        starting_points = []

        class State(Enum):
            rest = 0
            note = 1

        def get_state(row: int):
            note_index = m.get_value(row, 0)
            if note_index < 0:
                return State.rest
            else:
                return State.note

        if row_count == 0:
            pass
        else:
            pre_state = get_state(0)
            starting_points.append(0)
            for i in range(1, row_count):
                if pre_state == State.rest and get_state(i) == State.note:
                    starting_points.append(i)
                pre_state = get_state(i)

        # ブロックの先頭の行番号のリストからパラグラフのリストを作成
        paragraph_list = []
        for i in range(len(starting_points)):
            start_index = starting_points[i]
            if i == len(starting_points) - 1:
                end_index = row_count
            else:
                end_index = starting_points[i + 1]
            note_list = lst[start_index:end_index]
            paragraph = Paragraph()
            paragraph.start = start_index
            paragraph.end = end_index
            paragraph.note_list = p.pipe(
                note_list,
                p.filter(lambda x: x.note >= 0),
                list,
            )
            paragraph.rest_length = p.pipe(
                note_list,
                p.filter(lambda x: x.note < 0),
                p.map(lambda x: x.length),
                sum,
            )
            paragraph_list.append(paragraph)

        #
        return paragraph_list

    def get_paragraph(self, row: int):
        paragraph_list = self.get_paragraph_list()

        paragraph = None
        for _paragraph in paragraph_list:
            if _paragraph.in_paragraph(row):
                paragraph = _paragraph
                break
        return paragraph

    def get_current_paragraph(self):
        return self.get_paragraph(self.currentIndex().row())

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        mod = event.modifiers()

        if key == Qt.Key_Return and mod == Qt.NoModifier:
            self.edit(self.currentIndex())
            return
        # Shift_A Sift_I
        if key == Qt.Key_A and mod == Qt.ShiftModifier:
            self.setCurrentIndex(self.currentIndex().siblingAtColumn(2))
            self.edit(self.currentIndex())
            return
        if key == Qt.Key_I and mod == Qt.ShiftModifier:
            self.setCurrentIndex(self.currentIndex().siblingAtColumn(0))
            self.edit(self.currentIndex())
            return

        # h j k l
        if key == Qt.Key_J and mod == Qt.NoModifier:
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier)
        elif key == Qt.Key_K and mod == Qt.NoModifier:
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier)
        elif key == Qt.Key_H and mod == Qt.NoModifier:
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Left, Qt.NoModifier)
        elif key == Qt.Key_L and mod == Qt.NoModifier:
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Right, Qt.NoModifier)
        super().keyPressEvent(event)

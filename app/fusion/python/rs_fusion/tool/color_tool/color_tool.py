import datetime
import sys
from functools import partial
from pathlib import Path

import dataclasses
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QUndoStack,
)

from rs.core import (
    config,
    colormind,
    pipe as p,
    util,
)
from rs.gui import (
    appearance,
)
from rs_fusion.core import operator as op
from rs_fusion.tool.color_tool.color_table import ColorData, Model
from rs_fusion.tool.color_tool.color_tool_ui import Ui_MainWindow

APP_NAME = 'ColorTool'


@dataclasses.dataclass
class DocData(config.Data):
    color_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(ColorData))


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(600, 700)

        self.fusion = fusion

        self.def_dir = config.CONFIG_DIR.joinpath('color_tool')
        self.def_dir.mkdir(parents=True, exist_ok=True)

        # table
        v = self.ui.tableView
        m: Model = v.model()
        h = v.horizontalHeader()
        h.setDefaultSectionSize(80)
        hv = v.verticalHeader()
        hv.setMinimumWidth(30)
        hv.setDefaultSectionSize(50)
        hv.setDefaultAlignment(Qt.AlignCenter)
        m.add_row_data(ColorData())
        self.model = m
        self.undo_stack: QUndoStack = v.model().undo_stack

        # config
        self.file = None
        self.new_doc()

        # style sheet
        self.ui.currentRowButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.selectedButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.colormindDefButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.colormindUiButton.setStyleSheet(appearance.other_stylesheet)

        # event
        self.ui.tableView.model().undo_stack.cleanChanged.connect(self.set_title)
        self.ui.openUrlButton.clicked.connect(partial(
            util.open_url,
            colormind.URL,
        ))

        # add row
        self.ui.colormindDefButton.clicked.connect(partial(self.colormind, 'default'))
        self.ui.colormindUiButton.clicked.connect(partial(self.colormind, 'ui'))

        # apply
        self.ui.currentRowButton.clicked.connect(self.apply_color_from_current_row)
        self.ui.selectedButton.clicked.connect(self.apply_color_from_selected)

        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.actionNew.triggered.connect(self.new_doc)
        self.ui.actionOpen.triggered.connect(self.open_doc)
        self.ui.actionSave.triggered.connect(self.save_doc)
        self.ui.actionSave_As.triggered.connect(self.save_as_doc)

    def apply_color(self, color_list):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return
        op.apply_color(comp, color_list, self.ui.randomRadioButton.isChecked())

    def apply_color_from_current_row(self):
        row = self.ui.tableView.currentIndex().row()
        if row < 0:
            return
        row_data = self.model.get_row_data(row)
        color_list = p.pipe(
            [row_data.color00, row_data.color01, row_data.color02, row_data.color03, row_data.color04],
            p.map(QColor),
            p.map(lambda c: [c.red() / 255, c.green() / 255, c.blue() / 255]),
            list,
        )
        self.apply_color(color_list)

    def apply_color_from_selected(self):
        v = self.ui.tableView
        m: Model = self.model
        sm = v.selectionModel()
        color_list = p.pipe(
            sm.selectedIndexes(),
            p.filter(lambda i: i.column() != 0),
            p.map(lambda i: m.get_value(i.row(), i.column())),
            p.map(QColor),
            p.map(lambda c: [c.red() / 255, c.green() / 255, c.blue() / 255]),
            list,
        )
        if len(color_list) == 0:
            return

        self.apply_color(color_list)

    def colormind(self, color_model='default'):
        v = self.ui.tableView
        m: Model = self.model
        sm = v.selectionModel()

        color_data = ColorData()
        dt_now = datetime.datetime.now()
        color_data.name = dt_now.strftime('%y%m%d_%H%M%S')
        input_list = None
        if self.ui.useSelectionCheckBox.isChecked():
            input_list = ['N', 'N', 'N', 'N', 'N']
            row = self.ui.tableView.currentIndex().row()
            for index in p.pipe(
                    sm.selectedIndexes(),
                    p.filter(lambda i: i.column() != 0),
                    p.filter(lambda i: i.row() == row),
                    list,
            ):
                c = QColor(m.get_value(index.row(), index.column()))
                input_list[index.column() - 1] = [c.red(), c.green(), c.blue()]
        dct = colormind.get_color(model=color_model, input_list=input_list)
        if 'error' in dct.keys():
            print(dct['error'])
            return
        if 'result' in dct.keys():
            lst = dct['result']
            if len(lst) >= 5:
                color_data.color00 = QColor(lst[0][0], lst[0][1], lst[0][2]).name()
                color_data.color01 = QColor(lst[1][0], lst[1][1], lst[1][2]).name()
                color_data.color02 = QColor(lst[2][0], lst[2][1], lst[2][2]).name()
                color_data.color03 = QColor(lst[3][0], lst[3][1], lst[3][2]).name()
                color_data.color04 = QColor(lst[4][0], lst[4][1], lst[4][2]).name()
                if input_list is not None:
                    if input_list[0] != 'N':
                        color_data.color00 = QColor(input_list[0][0], input_list[0][1], input_list[0][2]).name()
                    if input_list[1] != 'N':
                        color_data.color01 = QColor(input_list[1][0], input_list[1][1], input_list[1][2]).name()
                    if input_list[2] != 'N':
                        color_data.color02 = QColor(input_list[2][0], input_list[2][1], input_list[2][2]).name()
                    if input_list[3] != 'N':
                        color_data.color03 = QColor(input_list[3][0], input_list[3][1], input_list[3][2]).name()
                    if input_list[4] != 'N':
                        color_data.color04 = QColor(input_list[4][0], input_list[4][1], input_list[4][2]).name()
        self.model.add_row_data(color_data)
        self.ui.tableView.scrollToBottom()

    def set_title(self):
        if self.file is None:
            self.setWindowTitle('%s' % APP_NAME)
        else:
            star = '*' if self.undo_stack.isClean() is False else ''
            self.setWindowTitle('%s - %s%s' % (APP_NAME, self.file, star))

    def new_doc(self):
        self.file = None
        self.model.clear()
        self.undo_stack.clear()
        self.set_title()

    def file_update(self, path: Path):
        self.file = path
        self.set_title()

    def open_doc(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            str(self.def_dir) if self.file is None else str(self.file.parent),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                d = DocData()
                d.load(file_path)
                self.set_data(d)
                self.undo_stack.clear()
                self.file_update(file_path)

    def save_doc(self):
        if self.file is None:
            self.save_as_doc()
            return
        d = self.get_data()
        d.save(self.file)
        self.undo_stack.setClean()
        self.set_title()

    def save_as_doc(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            str(self.def_dir.joinpath('color.json')) if self.file is None else str(self.file),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            d = self.get_data()
            d.save(file_path)
            self.undo_stack.setClean()
            self.file_update(file_path)

    def set_data(self, c: DocData):
        self.ui.tableView.model().set_data(c.color_list)

    def get_data(self) -> DocData:
        d = DocData()
        d.color_list.set_list(self.ui.tableView.model().to_list())
        return d


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run(None)

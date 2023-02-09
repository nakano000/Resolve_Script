import sys
import functools
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtGui import (
    QKeySequence,
    QStandardItemModel,
    QStandardItem, QIntValidator,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
)

from rs.core import util
from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op
from rs_fusion.tool.copy_tool.copy_tool_ui import Ui_MainWindow

APP_NAME = 'CopyTool'


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
        self.resize(200, 600)

        self.fusion = fusion
        self.tool_name = None
        #
        self.ui.stepLineEdit.setText(str(0))
        self.ui.jitterInfLineEdit.setText(str(0))
        self.ui.jitterSupLineEdit.setText(str(0))
        self.ui.stepLineEdit.setValidator(QIntValidator())
        self.ui.jitterInfLineEdit.setValidator(QIntValidator())
        self.ui.jitterSupLineEdit.setValidator(QIntValidator())

        # tree
        v = self.ui.treeView
        v.setHeaderHidden(True)

        v.setModel(QStandardItemModel())

        # button
        self.ui.setButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.sourceButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        #
        self.ui.sourceButton.clicked.connect(self.read_node)
        self.ui.setButton.clicked.connect(self.copy_prams)
        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        #

    def read_node(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            return

        # setup
        v = self.ui.treeView
        m = QStandardItemModel()
        v.setModel(m)
        tools: dict = comp.GetToolList(True)
        if tools is None:
            return
        if len(tools) == 0:
            return
        tool = tools[1]
        self.tool_name = tool.Name

        def make_row(_id, _name, _type):
            size = 20 + len(_name) - util.get_str_width(_name)
            display = '%s <%s> %s' % (_name.ljust(size), _type, _id)
            return [
                QStandardItem(display),
                QStandardItem(_id),
                QStandardItem(_type),
            ]

        # main
        node = QStandardItem(tool.Name)
        node.setSelectable(False)
        m.appendRow(node)
        # in
        i = 1
        while True:
            inp = tool.FindMainInput(i)
            if inp is None:
                break
            attrs = inp.GetAttrs()
            name = inp.Name
            if 'INPS_IC_Name' in attrs:
                name = attrs['INPS_IC_Name']
            i += 1
            # page
            page_names: dict = tool.GetControlPageNames()
            inp_dict: dict = tool.GetInputList()
            for page_name in page_names.values():
                page = QStandardItem(page_name)
                page.setSelectable(False)
                node.appendRow(page)
                for inp in inp_dict.values():
                    attrs = inp.GetAttrs()
                    name = inp.Name
                    if 'INPS_IC_Name' in attrs:
                        name = attrs['INPS_IC_Name']
                    if attrs['INPI_IC_ControlPage'] not in page_names.keys():
                        continue
                    if page_name != page_names[attrs['INPI_IC_ControlPage']]:
                        continue
                    page.appendRow(make_row(
                        inp.ID,
                        name,
                        attrs['INPS_DataType'],
                    ))
        #
        v.expandAll()

    def copy_prams(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            return

        # tool check
        if self.tool_name is None:
            return
        src_v = self.ui.treeView
        src_m = src_v.model()
        src_sm = src_v.selectionModel()
        param_list = []
        for i in src_sm.selectedRows(0):
            param = src_m.data(i.siblingAtColumn(1))
            if param is None:
                continue
            param_list.append(param)
        if len(param_list) == 0:
            param_list = None

        def to_int(_str):
            if _str in ['', '+', '-']:
                return 0
            return int(_str)

        step = to_int(self.ui.stepLineEdit.text())
        jitter_inf = to_int(self.ui.jitterInfLineEdit.text())
        jitter_sup = to_int(self.ui.jitterSupLineEdit.text())

        op.copy(comp, self.tool_name, param_list, step, jitter_inf, jitter_sup)

    def show(self) -> None:
        super().show()
        self.ui.treeView.setModel(QStandardItemModel())
        self.tool_name = None


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass

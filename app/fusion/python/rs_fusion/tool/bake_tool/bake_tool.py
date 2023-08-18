import sys
import functools
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.core import util
from rs.gui import (
    appearance,
)

from rs_fusion.core import get_modifiers
from rs_fusion.core import bake

from rs_fusion.tool.bake_tool.bake_tool_ui import Ui_MainWindow

APP_NAME = 'BakeTool'


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
        self.resize(200, 500)

        self.fusion = fusion

        # tree
        v = self.ui.treeView
        v.setHeaderHidden(True)

        v.setModel(QStandardItemModel())

        #
        self.ui.sfSpinBox.setValue(0)
        self.ui.efSpinBox.setValue(200)
        self.ui.connectedCheckBox.setChecked(True)
        self.ui.expressionCheckBox.setChecked(True)

        # button
        self.ui.bakeButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.readButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.globalRangeButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.renderRangeButton.setStyleSheet(appearance.other_stylesheet)

        # event
        #
        self.ui.readButton.clicked.connect(self.read_node)
        self.ui.bakeButton.clicked.connect(self.bake_prams)

        self.ui.globalRangeButton.clicked.connect(self.set_global_range)
        self.ui.renderRangeButton.clicked.connect(self.set_render_range)

        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        #

    def get_comp(self):
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            return None

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            return None

        return comp

    def read_node(self) -> None:
        # comp check
        comp = self.get_comp()
        if comp is None:
            return
        # setup
        v = self.ui.treeView
        m = QStandardItemModel()
        v.setModel(m)
        tools = comp.GetToolList(True)
        src = []
        for tool in tools.values():
            src.append(tool)
            modifiers = get_modifiers([tool])
            for mod in modifiers.values():
                src.append(mod)

        def make_row(_node, _id, _name):
            size = 20 + len(_name) - util.get_str_width(_name)
            display = '%s %s' % (_name.ljust(size), _id)
            return [
                QStandardItem(display),
                QStandardItem(_node),
                QStandardItem(_id),
            ]

        # main
        for tool in src:
            node = QStandardItem(tool.Name)
            node.setSelectable(False)
            m.appendRow(node)

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
                    if attrs['INPS_DataType'] != 'Number':
                        continue
                    if not attrs['INPB_External']:
                        continue
                    if self.ui.connectedCheckBox.isChecked() or self.ui.expressionCheckBox.isChecked():
                        is_connected = attrs['INPB_Connected'] and self.ui.connectedCheckBox.isChecked()
                        use_expression = inp.GetExpression() is not None and self.ui.expressionCheckBox.isChecked()
                        if not (is_connected or use_expression):
                            continue
                    page.appendRow(make_row(
                        tool.Name,
                        inp.ID,
                        name,
                    ))
        #
        v.expandAll()

    def set_render_range(self) -> None:
        # comp check
        comp = self.get_comp()
        if comp is None:
            return
        attrs = comp.GetAttrs()
        self.ui.sfSpinBox.setValue(attrs['COMPN_RenderStart'])
        self.ui.efSpinBox.setValue(attrs['COMPN_RenderEnd'])

    def set_global_range(self) -> None:
        # comp check
        comp = self.get_comp()
        if comp is None:
            return
        attrs = comp.GetAttrs()
        self.ui.sfSpinBox.setValue(attrs['COMPN_GlobalStart'])
        self.ui.efSpinBox.setValue(attrs['COMPN_GlobalEnd'])

    def bake_prams(self) -> None:
        # comp check
        comp = self.get_comp()
        if comp is None:
            return

        v = self.ui.treeView
        m = v.model()
        sm = v.selectionModel()
        param_dict = {}
        for i in sm.selectedRows(0):
            tool_name = m.data(i.siblingAtColumn(1))
            if tool_name is None:
                continue
            param = m.data(i.siblingAtColumn(2))
            if param is None:
                continue
            if tool_name not in param_dict.keys():
                param_dict[tool_name] = []
            param_dict[tool_name].append(param)
        bake.apply(comp, param_dict, self.ui.sfSpinBox.value(), self.ui.efSpinBox.value())

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

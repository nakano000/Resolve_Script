import sys

from pathlib import Path
from typing import List
import dataclasses
from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QStringListModel,
)
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QAction,
)

from rs.core import (
    config,
    pipe as p, util,
)
from rs.gui import (
    appearance,
)
from rs_fusion.tool.paste_tool.node_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Favorites')
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            # | Qt.WindowStaysOnTopHint
        )
        self.resize(500, 200)
        self.fusion = fusion

        # tree
        v = self.ui.treeView
        v.setHeaderHidden(True)
        m = QStandardItemModel()
        v.setModel(m)

        # style sheet
        self.ui.addButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.readButton.setStyleSheet(appearance.other_stylesheet)

        # event
        self.ui.readButton.clicked.connect(self.read_node)

        self.ui.closeButton.clicked.connect(self.close)

    def get_selection(self) -> List[str]:
        v = self.ui.treeView
        m = v.model()
        sm = v.selectionModel()
        return p.pipe(
            sm.selectedRows(1),
            p.map(lambda i: m.data(i)),
            list,
        )

    def read_node(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            return

        # setup
        tools = list(comp.GetToolList(True).values())
        if len(tools) < 1:
            return
        tool = tools[0]

        v = self.ui.treeView
        m = v.model()
        m.clear()

        def make_row(_id, _name, _type):
            size = 20 + len(_name) - util.get_str_width(_name)
            display = '%s <%s> %s' % (_name.ljust(size), _type, _id)
            return [
                QStandardItem(display),
                QStandardItem(_id),
            ]

        # main
        node = QStandardItem(tool.Name)
        node.setSelectable(False)
        m.appendRow(node)
        # out
        i = 1
        while True:
            outp = tool.FindMainOutput(i)
            if outp is None:
                break
            node.appendRow(make_row(
                outp.ID,
                outp.Name,
                outp.GetAttrs()['OUTS_DataType'],
            ))
            i += 1
        # in
        inp_id_list = []
        i = 1
        while True:
            inp = tool.FindMainInput(i)
            if inp is None:
                break
            attrs = inp.GetAttrs()
            name = inp.Name
            if 'INPS_IC_Name' in attrs:
                name = attrs['INPS_IC_Name']
            if tool.GetAttrs()['TOOLB_Visible']:
                node.appendRow(make_row(
                    inp.ID,
                    name,
                    attrs['INPS_DataType'],
                ))
                inp_id_list.append(inp.ID)
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
                control_group = 0
                if 'INPI_IC_ControlGroup' in attrs:
                    control_group = int(attrs['INPI_IC_ControlGroup'])
                if attrs['INPI_IC_ControlPage'] not in page_names.keys():
                    continue
                if page_name != page_names[attrs['INPI_IC_ControlPage']]:
                    continue
                if inp.ID in inp_id_list:  # Main Inputは追加しない
                    continue
                page.appendRow(make_row(
                    inp.ID,
                    name,
                    attrs['INPS_DataType'],
                ))
        #
        v.expandAll()


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())

import json
import sys
from functools import partial
from pathlib import Path
from typing import List, Any

import dataclasses
from PySide2.QtCore import (
    Qt,
    QModelIndex,
)
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from rs.core import (
    config,
    pipe as p,
    util,
)
from rs.gui import (
    appearance,
    basic_table,
)
from rs_fusion.tool.make_macro import macro
from rs_fusion.tool.make_macro.make_macro_ui import Ui_MainWindow

APP_NAME = 'MakeMacro'


@dataclasses.dataclass
class InputData(basic_table.RowData):
    node: str = ''
    page: str = ''
    id: str = ''
    name: str = ''

    @classmethod
    def toHeaderList(cls) -> List[str]:
        return ['Node', 'Page', 'ID', 'Name']


@dataclasses.dataclass
class ConfigData(config.Data):
    macro_name: str = 'MacroTool'
    use_group: bool = True
    main_output_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))
    main_input_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))
    input_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))


def get_new_model():
    m = QStandardItemModel()
    return m


class Model(basic_table.Model):

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        if index.isValid():
            if role == Qt.DisplayRole:
                return dataclasses.astuple(self._data[index.row()])[index.column()]

            if role == Qt.EditRole:
                return dataclasses.astuple(self._data[index.row()])[index.column()]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        return Qt.NoItemFlags


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
        self.resize(1100, 800)

        self.fusion = fusion

        # table
        for table_v in [
            self.ui.inputTableView,
            self.ui.mainInputTableView,
            self.ui.mainOutputTableView,
        ]:
            table_v.setModel(Model(InputData))

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # tree
        v = self.ui.treeView
        v.setHeaderHidden(True)

        v.setModel(get_new_model())

        # style sheet
        self.ui.saveMacroButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.readButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.addNodeToolButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.addNodeToolButton.clicked.connect(self.add_row)

        self.ui.readButton.clicked.connect(self.read_node)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.saveMacroButton.clicked.connect(self.save_macro, Qt.QueuedConnection)

        self.ui.actionOpen.triggered.connect(self.open_doc)
        self.ui.actionSave_As.triggered.connect(self.save_as_doc)

    def read_node(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print('Fusion Pageで実行してください。')
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print('コンポジションが見付かりません。')
            return

        # setup
        v = self.ui.treeView
        m = get_new_model()
        v.setModel(m)
        tools: dict = comp.GetToolList(True)

        def make_row(_node, _page, _id, _name, _type):
            size = 20 + len(_name) - util.get_str_width(_name)
            display = '%s <%s> %s' % (_name.ljust(size), _type, _id)
            return [
                QStandardItem(display),
                QStandardItem(_node),
                QStandardItem(_page),
                QStandardItem(_id),
                QStandardItem(_name),
            ]

        # main
        for tool in tools.values():
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
                    tool.Name,
                    '<Output>',
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
                inp_id_list.append(inp.ID)
                node.appendRow(make_row(
                    tool.Name,
                    '<Input>',
                    inp.ID,
                    inp.Name,
                    inp.GetAttrs()['INPS_DataType'],
                ))
                i += 1
            # page
            page_names: dict = tool.GetControlPageNames()
            inp_dict: dict = tool.GetInputList()
            for page_name in page_names.values():
                page = QStandardItem(page_name)
                page.setSelectable(False)
                node.appendRow(page)
                for inp in inp_dict.values():
                    if inp.GetAttrs()['INPI_IC_ControlPage'] not in page_names.keys():
                        continue
                    if page_name != page_names[inp.GetAttrs()['INPI_IC_ControlPage']]:
                        continue
                    if inp.ID in inp_id_list:  # Main Inputは追加しない
                        continue
                    page.appendRow(make_row(
                        tool.Name,
                        page_name,
                        inp.ID,
                        inp.Name,
                        inp.GetAttrs()['INPS_DataType'],
                    ))
        #
        v.expandAll()

    def add_row(self) -> None:
        # tree
        src_v = self.ui.treeView
        src_m = src_v.model()
        src_sm = src_v.selectionModel()
        # table
        v = self.ui.inputTableView
        m: Model = v.model()
        in_v = self.ui.mainInputTableView
        in_m = in_v.model()
        out_v = self.ui.mainOutputTableView
        out_m = out_v.model()
        for i in src_sm.selectedRows(0):
            i: QModelIndex
            r = InputData()
            r.node = src_m.data(i.siblingAtColumn(1))
            r.page = src_m.data(i.siblingAtColumn(2))
            r.id = src_m.data(i.siblingAtColumn(3))
            r.name = src_m.data(i.siblingAtColumn(4))
            if r.node is None or r.id is None:
                continue
            if r.page == '<Output>':
                out_m.add_row_data(r)
            elif r.page == '<Input>':
                in_m.add_row_data(r)
            else:
                m.add_row_data(r)

    def save_macro(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print('Fusion Pageで実行してください。')
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print('コンポジションが見付かりません。')
            return
        # table
        v = self.ui.inputTableView
        m: Model = v.model()
        in_v = self.ui.mainInputTableView
        in_m: Model = in_v.model()
        out_v = self.ui.mainOutputTableView
        out_m: Model = out_v.model()

        # get data
        data = self.get_data()
        output_list = []
        for row in out_m.to_list():
            output_list.append({
                'id': row.id,
                'node': row.node,
            })
        main_in_list = []
        for row in in_m.to_list():
            main_in_list.append({
                'id': row.id,
                'node': row.node,
            })
        in_list = []
        for row in m.to_list():
            row: InputData
            value = None
            tool = comp.FindTool(row.node)
            if tool is not None:
                _v = tool.GetInput(row.id)
                if type(_v) == float:
                    value = _v
            in_list.append({
                'id': row.id,
                'node': row.node,
                'value': value,
            })

        # save macro
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            str(config.RESOLVE_USER_PATH.joinpath(
                'Templates',
                'Edit',
                'Generators',
                data.macro_name + '.setting',
            )),
            'Setting File (*.setting);;All File (*.*)'
        )
        if path != '':
            comp.Execute(macro.get_save_script(
                path,
                data.macro_name,
                '\n'.join([
                    macro.get_header(data.macro_name, data.use_group),
                    macro.get_input(main_in_list, in_list),
                    macro.get_output(output_list),
                    macro.get_footer(),
                ]),
            ))

    def open_doc(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            None,
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                a = self.get_data()
                a.load(file_path)
                self.set_data(a)

    def save_as_doc(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            None,
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            a = self.get_data()
            a.save(file_path)

    def set_data(self, c: ConfigData):
        self.ui.nameLineEdit.setText(c.macro_name)
        self.ui.useGroupCheckBox.setChecked(c.use_group)
        self.ui.mainOutputTableView.model().set_data(c.main_output_list)
        self.ui.mainInputTableView.model().set_data(c.main_input_list)
        self.ui.inputTableView.model().set_data(c.input_list)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.macro_name = self.ui.nameLineEdit.text()
        c.use_group = self.ui.useGroupCheckBox.isChecked()
        c.main_output_list.set_list(self.ui.mainOutputTableView.model().to_list())
        c.main_input_list.set_list(self.ui.mainInputTableView.model().to_list())
        c.input_list.set_list(self.ui.inputTableView.model().to_list())
        return c

    def load_config(self) -> None:
        c = ConfigData()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_data()
        c.macro_name = 'MacroTool'
        c.main_output_list = config.DataList(InputData)
        c.main_input_list = config.DataList(InputData)
        c.input_list = config.DataList(InputData)
        c.save(self.config_file)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)


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

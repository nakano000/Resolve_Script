import sys
from functools import partial
from pathlib import Path

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
    QHeaderView,
)

from rs.core import (
    config,
    pipe as p,
    util,
)
from rs.gui import (
    appearance,
)
from rs_fusion.tool.make_macro.macro_table import InputData, Model
from rs_fusion.tool.make_macro import macro
from rs_fusion.tool.make_macro.make_macro_ui import Ui_MainWindow

APP_NAME = 'MakeMacro'


@dataclasses.dataclass
class ConfigData(config.Data):
    macro_name: str = 'MacroTool'
    use_group: bool = True
    main_output_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))
    main_input_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))
    input_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))


def get_modifiers(tools):
    modifiers = {}
    for tool in tools:
        for inp in tool.GetInputList().values():
            outp = inp.GetConnectedOutput()
            if outp is None:
                continue
            x = outp.GetTool()
            if x.GetAttrs()['TOOLB_Visible']:
                continue
            modifiers[x.Name] = x
            modifiers.update(get_modifiers([x]))
    return modifiers


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
        self.resize(900, 700)

        self.fusion = fusion

        # table
        for v in [
            self.ui.inputTableView,
            self.ui.mainInputTableView,
            self.ui.mainOutputTableView,
        ]:
            h = v.horizontalHeader()
            h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            h.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        for v in [
            self.ui.mainInputTableView,
            self.ui.mainOutputTableView,
        ]:
            v.hideColumn(4)
            v.hideColumn(5)
            v.hideColumn(6)
            v.hideColumn(7)

        # config
        self.file = None
        self.new_doc()

        # splitter
        # self.ui.splitter.setStretchFactor(1, 1)
        self.ui.splitter.setSizes([200, 300])

        # tree
        v = self.ui.treeView
        v.setHeaderHidden(True)

        v.setModel(QStandardItemModel())

        # style sheet
        self.ui.saveMacroButton.setStyleSheet(appearance.ex_stylesheet)

        self.ui.readButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.clearButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.addNodeToolButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.inputTableView.model().undo_stack.cleanChanged.connect(self.set_title)
        self.ui.mainInputTableView.model().undo_stack.cleanChanged.connect(self.set_title)
        self.ui.mainOutputTableView.model().undo_stack.cleanChanged.connect(self.set_title)

        self.ui.addNodeToolButton.clicked.connect(self.add_row)

        self.ui.readButton.clicked.connect(self.read_node)
        self.ui.clearButton.clicked.connect(self.clear_tree)

        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.saveMacroButton.clicked.connect(partial(self.save_macro, False), Qt.QueuedConnection)
        self.ui.saveMacroFromJSONButton.clicked.connect(partial(self.save_macro, True), Qt.QueuedConnection)

        self.ui.actionNew.triggered.connect(self.new_doc)
        self.ui.actionOpen.triggered.connect(self.open_doc)
        self.ui.actionSave.triggered.connect(self.save_doc)
        self.ui.actionSave_As.triggered.connect(self.save_as_doc)

    def undo_stack_clear(self):
        self.ui.inputTableView.model().undo_stack.clear()
        self.ui.mainInputTableView.model().undo_stack.clear()
        self.ui.mainOutputTableView.model().undo_stack.clear()

    def undo_stack_set_clean(self):
        self.ui.inputTableView.model().undo_stack.setClean()
        self.ui.mainInputTableView.model().undo_stack.setClean()
        self.ui.mainOutputTableView.model().undo_stack.setClean()

    def undo_stack_is_clean(self) -> bool:
        return (
                self.ui.inputTableView.model().undo_stack.isClean()
                and self.ui.mainInputTableView.model().undo_stack.isClean()
                and self.ui.mainOutputTableView.model().undo_stack.isClean()
        )

    def clear_tree(self) -> None:
        self.ui.treeView.setModel(QStandardItemModel())

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
        m = QStandardItemModel()
        v.setModel(m)
        tools = comp.GetToolList(True)
        src = []
        for tool in tools.values():
            src.append(tool)
            modifiers = get_modifiers([tool])
            for mod in modifiers.values():
                src.append(mod)

        def make_row(_node, _page, _id, _name, _type, _control_group=0):
            size = 20 + len(_name) - util.get_str_width(_name)
            display = '%s <%s> %s' % (_name.ljust(size), _type, _id)
            return [
                QStandardItem(display),
                QStandardItem(_node),
                QStandardItem(_page),
                QStandardItem(_id),
                QStandardItem(_name),
                QStandardItem(str(_control_group)),
            ]

        # main
        for tool in src:
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
                attrs = inp.GetAttrs()
                name = inp.Name
                if 'INPS_IC_Name' in attrs:
                    name = attrs['INPS_IC_Name']
                if tool.GetAttrs()['TOOLB_Visible']:
                    node.appendRow(make_row(
                        tool.Name,
                        '<Input>',
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
                        tool.Name,
                        page_name,
                        inp.ID,
                        name,
                        attrs['INPS_DataType'],
                        control_group,
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
        # main
        rows = []
        in_rows = []
        out_rows = []
        # get selected rows
        for i in src_sm.selectedRows(0):
            i: QModelIndex
            r = InputData()
            r.node = src_m.data(i.siblingAtColumn(1))
            r.page = src_m.data(i.siblingAtColumn(2))
            r.id = src_m.data(i.siblingAtColumn(3))
            r.name = src_m.data(i.siblingAtColumn(4))
            if src_m.data(i.siblingAtColumn(5)) is not None:
                r.control_group = int(src_m.data(i.siblingAtColumn(5)))
            if r.node is None or r.id is None:
                continue
            if r.page == '<Output>':
                out_rows.append(r)
            elif r.page == '<Input>':
                in_rows.append(r)
            else:
                rows.append(r)
        # add row
        if len(rows) > 0:
            m.undo_stack.beginMacro('Add Row')
            for r in rows:
                m.add_row_data(r)
            m.undo_stack.endMacro()
            v.scrollToBottom()
        if len(in_rows) > 0:
            in_m.undo_stack.beginMacro('Add Row')
            for r in in_rows:
                in_m.add_row_data(r)
            in_m.undo_stack.endMacro()
            in_v.scrollToBottom()
        if len(out_rows) > 0:
            out_m.undo_stack.beginMacro('Add Row')
            for r in out_rows:
                out_m.add_row_data(r)
            out_m.undo_stack.endMacro()
            out_v.scrollToBottom()

    def save_macro(self, use_json_path: bool) -> None:
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

        # control groupの数字が被らないようにNode毎にoffsetを設定
        cg_offset_dict = {}
        for row in m.to_list():
            if row.node in cg_offset_dict:
                if cg_offset_dict[row.node] >= row.control_group:
                    continue
            cg_offset_dict[row.node] = row.control_group
        _pre_max = 0
        for key in cg_offset_dict.keys():
            _tmp = cg_offset_dict[key]
            cg_offset_dict[key] = _pre_max
            _pre_max += _tmp

        # get input
        in_list = []
        for row in m.to_list():
            row: InputData
            name = None
            value = None
            control_group = None

            tool = comp.FindTool(row.node)
            if tool is not None:
                _v = tool.GetInput(row.id, comp.CurrentTime)
                if type(_v) == float:
                    value = _v
            if row.id != row.name:
                name = row.name
            if row.control_group != 0:
                control_group = row.control_group + cg_offset_dict[row.node]
            in_list.append({
                'id': row.id,
                'node': row.node,
                'name': name,
                'value': value,
                'control_group': control_group,
                'option01': row.option01.strip(),
                'option02': row.option02.strip(),
                'option03': row.option03.strip(),
            })

        # save macro
        if use_json_path and self.file is not None:
            _tmp_path = str(self.file.parent.joinpath(
                self.file.stem + '.setting',
            ))
        else:
            _tmp_name = data.macro_name if self.file is None else self.file.stem
            _tmp_path = str(config.RESOLVE_USER_PATH.joinpath(
                'Templates',
                'Edit',
                'Generators',
                _tmp_name + '.setting',
            ))
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            _tmp_path,
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

    def set_title(self):
        if self.file is None:
            self.setWindowTitle('%s' % APP_NAME)
        else:
            star = '*' if self.undo_stack_is_clean() is False else ''
            self.setWindowTitle('%s - %s%s' % (APP_NAME, self.file, star))

    def new_doc(self):
        self.set_data(ConfigData())
        self.ui.saveMacroFromJSONButton.setEnabled(False)
        self.ui.saveMacroFromJSONButton.setStyleSheet(None)
        self.undo_stack_clear()
        self.set_title()

    def file_update(self, path: Path):
        self.file = path
        self.ui.saveMacroFromJSONButton.setEnabled(True)
        self.ui.saveMacroFromJSONButton.setStyleSheet(appearance.ex_stylesheet)
        self.set_title()

    def open_doc(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            None if self.file is None else str(self.file.parent),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                a = self.get_data()
                a.load(file_path)
                self.set_data(a)
                self.undo_stack_clear()
                self.file_update(file_path)

    def save_doc(self):
        if self.file is None:
            self.save_as_doc()
        else:
            a = self.get_data()
            a.save(self.file)
            self.undo_stack_set_clean()
            self.set_title()

    def save_as_doc(self):
        data = self.get_data()
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            data.macro_name + '.json' if self.file is None else str(self.file),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            a = self.get_data()
            a.save(file_path)
            self.undo_stack_set_clean()
            self.file_update(file_path)

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

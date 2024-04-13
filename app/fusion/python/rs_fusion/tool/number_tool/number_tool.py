import sys
from functools import partial
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QDoubleValidator,
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

from rs_fusion.core import (
    operator as op,
)
from rs_fusion.tool.number_tool.number_tool_ui import Ui_MainWindow

APP_NAME = 'NumberTool'


def make_row(_id, _name):
    size = 20 + len(_name) - util.get_str_width(_name)
    display = '%s %s' % (_name.ljust(size), _id)
    return [
        QStandardItem(display),
        QStandardItem(_id),
    ]


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
        self.resize(100, 700)

        self.fusion = fusion
        self.tool_name = None

        # tree
        for v in [self.ui.toolTreeView, self.ui.toolBTreeView, self.ui.modifierTreeView]:
            v.setHeaderHidden(True)
            v.setModel(QStandardItemModel())

        #
        for w in [
            self.ui.valueLineEdit, self.ui.stepLineEdit, self.ui.infLineEdit, self.ui.supLineEdit,
        ]:
            w.setText(str(0.0))
            w.setValidator(QDoubleValidator())
        self.ui.valueLineEdit.setText(str(0.5))
        self.ui.supLineEdit.setText(str(1.0))

        # button
        self.ui.setButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.randomButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.sourceButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.loadButton.setStyleSheet(appearance.ex_stylesheet)

        # event

        # align
        self.ui.alignLButton.clicked.connect(
            partial(self.align_value, op.AlignType.L)
        )
        self.ui.alignCButton.clicked.connect(
            partial(self.align_value, op.AlignType.C)
        )
        self.ui.alignRButton.clicked.connect(
            partial(self.align_value, op.AlignType.R)
        )
        # distribute
        self.ui.distributeButton.clicked.connect(self.distribute_value)
        # set
        self.ui.setButton.clicked.connect(self.set_value)
        # random
        self.ui.randomButton.clicked.connect(self.random_value)
        # ui
        self.ui.tabWidget.currentChanged.connect(self.tab_index_changed)
        #
        self.ui.sourceButton.clicked.connect(self.read_node)
        self.ui.loadButton.clicked.connect(self.read_modifier)
        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

        #
        self.tab_index_changed()

    def tab_index_changed(self):
        self.ui.alignGroupBox.setEnabled(self.ui.tabWidget.currentIndex() == 0)

    def get_comp(self):
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print('Fusion Pageで実行してください。')
            return None

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print('コンポジションが見付かりません。')
            return None
        return comp

    def get_attr_id(self, tree_view=None):
        if tree_view is None:
            tree_view = self.ui.toolTreeView
        idx = tree_view.currentIndex()
        if idx is None:
            return None
        return idx.sibling(idx.row(), 1).data()

    def get_modifier(self, comp):
        if self.tool_name is None:
            return None
        tool = comp.FindTool(self.tool_name)
        if tool is None:
            return None

        # attr id
        attr_id = self.get_attr_id(tree_view=self.ui.toolBTreeView)
        if attr_id is None:
            return None

        # modifier
        modifier = None
        for inp in tool.GetInputList().values():
            if inp.ID != attr_id:
                continue
            outp = inp.GetConnectedOutput()
            if outp is None:
                continue
            modifier = outp.GetTool()

        return modifier

    def read_modifier(self):
        comp = self.get_comp()
        if comp is None:
            return

        # setup
        v = self.ui.modifierTreeView
        m = QStandardItemModel()
        v.setModel(m)

        # modifier
        tool = self.get_modifier(comp)
        if tool is None:
            return

        # main
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
                if (
                        'INPID_InputControl' in attrs.keys()
                        and attrs['INPID_InputControl'] in ('LabelControl', 'ButtonControl', 'NestControl')
                ):
                    continue
                page.appendRow(make_row(
                    inp.ID,
                    name,
                ))
        #
        v.expandAll()

    def read_node(self) -> None:
        comp = self.get_comp()
        if comp is None:
            return

        # setup
        v = self.ui.toolTreeView
        m = QStandardItemModel()
        v.setModel(m)

        v_b = self.ui.toolBTreeView
        m_b = QStandardItemModel()
        v_b.setModel(m_b)

        v_mod = self.ui.modifierTreeView
        m_mod = QStandardItemModel()
        v_mod.setModel(m_mod)

        tools: dict = comp.GetToolList(True)
        if tools is None:
            return
        if len(tools) == 0:
            return
        tool = tools[1]
        self.tool_name = tool.Name

        # main
        node = QStandardItem(tool.Name)
        node.setSelectable(False)
        m.appendRow(node)

        node_b = QStandardItem(tool.Name)
        node_b.setSelectable(False)
        m_b.appendRow(node_b)

        # page
        page_names: dict = tool.GetControlPageNames()
        inp_dict: dict = tool.GetInputList()
        for page_name in page_names.values():

            page = QStandardItem(page_name)
            page.setSelectable(False)
            node.appendRow(page)

            page_b = QStandardItem(page_name)
            page_b.setSelectable(False)
            node_b.appendRow(page_b)

            for inp in inp_dict.values():
                attrs = inp.GetAttrs()
                name = inp.Name
                if 'INPS_IC_Name' in attrs:
                    name = attrs['INPS_IC_Name']
                if attrs['INPI_IC_ControlPage'] not in page_names.keys():
                    continue
                if page_name != page_names[attrs['INPI_IC_ControlPage']]:
                    continue

                # modifier
                outp = inp.GetConnectedOutput()
                if outp is not None:
                    x = outp.GetTool()
                    if not x.GetAttrs()['TOOLB_Visible']:
                        page_b.appendRow(make_row(
                            inp.ID,
                            name,
                        ))
                # tool
                if (
                        'INPID_InputControl' in attrs.keys()
                        and attrs['INPID_InputControl'] in ('LabelControl', 'ButtonControl', 'NestControl')
                ):
                    continue
                if attrs['INPS_DataType'] != 'Number':
                    continue
                page.appendRow(make_row(
                    inp.ID,
                    name,
                ))
        #
        v.expandAll()
        v_b.expandAll()

    def align_value(self, align_type: op.AlignType) -> None:
        comp = self.get_comp()
        if comp is None:
            return
        attr_id = self.get_attr_id()
        if attr_id is None:
            return

        op.align(comp, attr_id, align_type)

    def distribute_value(self) -> None:
        comp = self.get_comp()
        if comp is None:
            return
        attr_id = self.get_attr_id()
        if attr_id is None:
            return

        op.distribute(
            comp,
            attr_id,
            is_random=self.ui.randomRadioButton.isChecked(),
            is_reverse=self.ui.r2lRadioButton.isChecked(),
        )

    def set_value(self) -> None:
        comp = self.get_comp()
        if comp is None:
            return
        # attr id
        if self.ui.tabWidget.currentIndex() == 0:
            attr_id = self.get_attr_id(tree_view=self.ui.toolTreeView)
        else:
            attr_id = self.get_attr_id(tree_view=self.ui.toolBTreeView)
        if attr_id is None:
            return

        # modifier attr id
        if self.ui.tabWidget.currentIndex() == 0:
            modi_attr_id = None
        else:
            modi_attr_id = self.get_attr_id(tree_view=self.ui.modifierTreeView)
            if modi_attr_id is None:
                return

        op.set_value(
            comp,
            attr_id,
            float(self.ui.valueLineEdit.text()),
            float(self.ui.stepLineEdit.text()),
            modi_attr_id=modi_attr_id,
            is_abs=self.ui.absoluteRadioButton.isChecked(),
            is_random=self.ui.randomRadioButton.isChecked(),
            is_reverse=self.ui.r2lRadioButton.isChecked(),
            use_key=self.ui.keyFrameRadioButton.isChecked(),
            key_index=self.ui.keyFrameIndexSpinBox.value(),
        )

    def random_value(self) -> None:
        comp = self.get_comp()
        if comp is None:
            return
        # attr id
        if self.ui.tabWidget.currentIndex() == 0:
            attr_id = self.get_attr_id(tree_view=self.ui.toolTreeView)
        else:
            attr_id = self.get_attr_id(tree_view=self.ui.toolBTreeView)
        if attr_id is None:
            return

        # modifier attr id
        if self.ui.tabWidget.currentIndex() == 0:
            modi_attr_id = None
        else:
            modi_attr_id = self.get_attr_id(tree_view=self.ui.modifierTreeView)
            if modi_attr_id is None:
                return

        op.random_value(
            comp,
            attr_id,
            float(self.ui.infLineEdit.text()),
            float(self.ui.supLineEdit.text()),
            modi_attr_id=modi_attr_id,
            is_abs=self.ui.absoluteRadioButton.isChecked(),
            is_random=self.ui.randomRadioButton.isChecked(),
            use_key=self.ui.keyFrameRadioButton.isChecked(),
            key_index=self.ui.keyFrameIndexSpinBox.value(),
        )


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

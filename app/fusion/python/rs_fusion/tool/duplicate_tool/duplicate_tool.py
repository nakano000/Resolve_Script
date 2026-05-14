import sys
import functools
from PySide6.QtCore import (
    Qt,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.core import util
from rs.gui import (
    appearance,
)

from rs_fusion.core.operator import to_int, get_main_input
from rs_fusion.tool.duplicate_tool.duplicate_tool_ui import Ui_MainWindow

APP_NAME = 'DuplicateTool'


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
        self.resize(200, 100)

        self.fusion = fusion

        self.ui.duplicateButton.setStyleSheet(appearance.in_stylesheet)

        # set data
        self.ui.spinBox.setValue(1)

        # event
        #
        self.ui.duplicateButton.clicked.connect(self.duplicate_node)
        self.ui.spinBox.lineEdit().returnPressed.connect(self.duplicate_node)
        self.ui.closeButton.clicked.connect(self.close)

        #

    def duplicate_node(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            return
        # tools
        tools = list(comp.GetToolList(True).values())
        if len(tools) == 0:
            tool = comp.ActiveTool
        else:
            tool = tools[0]
        if tool is None:
            return

        flow = comp.CurrentFrame.FlowView
        _x, _y = flow.GetPosTable(tool).values()
        _x = to_int(_x)
        _y = to_int(_y)

        # get data
        num = self.ui.spinBox.value()

        # start
        comp.Lock()
        comp.StartUndo('RS Duplicate Tool')

        flow.Select()
        settings = tool.SaveSettings()
        input_connections = []
        for _name, inp in tool.GetInputList().items():
            outp = inp.GetConnectedOutput()
            if outp is None:
                continue

            inp_attrs = inp.GetAttrs()
            outp_attrs = outp.GetAttrs()

            input_id = inp_attrs.get('INPS_ID')
            src_tool = outp.GetTool()
            src_output = outp_attrs.get('OUTS_ID')

            if input_id is None or src_tool is None:
                continue

            input_connections.append((input_id, src_tool, src_output))

        for i in range(num):
            node = comp.AddTool(tool.ID, _x + i + 1, _y)
            node.LoadSettings(settings)
            for input_id, src_tool, src_output in input_connections:
                if src_output is None:
                    node.ConnectInput(input_id, src_tool)
                else:
                    try:
                        node.ConnectInput(input_id, src_tool, src_output)
                    except TypeError:
                        node.ConnectInput(input_id, src_tool)
            # flow.SetPos(node, _x + i + 1, _y)
            flow.Select(node)

        # end
        comp.EndUndo(True)
        comp.Unlock()

        # tool check


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

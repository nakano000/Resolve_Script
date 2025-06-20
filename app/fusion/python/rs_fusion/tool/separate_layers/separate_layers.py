import sys
import functools
from PySide6.QtCore import (
    Qt,
    QStringListModel,
    QSortFilterProxyModel,
    QEvent, QItemSelectionModel,
)
from PySide6.QtGui import (
    QKeySequence,
    QKeyEvent,
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.gui import (
    appearance,
)

from rs_fusion.core.operator import to_int, get_main_input
from rs_fusion.tool.separate_layers.separate_layers_ui import Ui_MainWindow

APP_NAME = 'Separate Layers'


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
            | Qt.MSWindowsFixedSizeDialogHint
        )
        self.resize(180, 50)

        self.fusion = fusion

        # button
        self.ui.layerMuxerButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.wirelessLinkButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.layerMuxerButton.clicked.connect(functools.partial(self.separate, 'LayerMuxer'))
        self.ui.wirelessLinkButton.clicked.connect(functools.partial(self.separate, 'Fuse.Wireless'))
        self.ui.closeButton.clicked.connect(self.close)

        #

    def separate(self, tool_type: str = 'LayerMuxer') -> None:
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return
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
        # output
        outp = tool.FindMainOutput(1)
        if outp is None:
            return

        # layer
        layer_list = list(outp.GetLayerList().values())

        # flow
        flow = comp.CurrentFrame.FlowView
        _x, _y = flow.GetPosTable(tool).values()
        _x = to_int(_x)
        _y = to_int(_y)

        # start
        comp.Lock()
        comp.StartUndo('RS Separate Layers')

        for i, layer_name in enumerate(layer_list):
            if layer_name == '':
                continue
            node = comp.AddTool(tool_type, _x + i - 1, _y + 4)
            node.SetAttrs({'TOOLS_Name': layer_name})
            # LayerMuxer
            if tool_type == 'LayerMuxer':
                node.Image2.ConnectTo(outp)
                node.Layer = layer_name
            # Wireless Link
            elif tool_type == 'Fuse.Wireless':
                node.Input.ConnectTo(outp)
                node.Input_LayerSelect = layer_name

        # end
        comp.EndUndo(True)
        comp.Unlock()

    def show(self) -> None:
        super().show()


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

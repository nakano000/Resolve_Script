import enum
import sys
import functools
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.gui import (
    appearance,
)
from rs_fusion.core import (
    operator as op,
)
from rs_fusion.tool.pivot_tool.pivot_tool_ui import Ui_MainWindow

APP_NAME = 'PivotTool'


class V(enum.Enum):
    N = 0
    C = 1
    S = 2


class H(enum.Enum):
    W = 0
    C = 1
    E = 2


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
        self.resize(100, 100)

        self.fusion = fusion

        #
        self.ui.xLineEdit.setText(str(0.5))
        self.ui.yLineEdit.setText(str(0.5))
        self.ui.xLineEdit.setValidator(QDoubleValidator())
        self.ui.yLineEdit.setValidator(QDoubleValidator())

        # button
        self.ui.setButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.neButton.clicked.connect(
            functools.partial(self.set_pivot, V.N, H.E)
        )
        self.ui.nButton.clicked.connect(
            functools.partial(self.set_pivot, V.N, H.C)
        )
        self.ui.nwButton.clicked.connect(
            functools.partial(self.set_pivot, V.N, H.W)
        )
        self.ui.eButton.clicked.connect(
            functools.partial(self.set_pivot, V.C, H.E)
        )
        self.ui.centerButton.clicked.connect(
            functools.partial(self.set_pivot, V.C, H.C)
        )
        self.ui.wButton.clicked.connect(
            functools.partial(self.set_pivot, V.C, H.W)
        )
        self.ui.seButton.clicked.connect(
            functools.partial(self.set_pivot, V.S, H.E)
        )
        self.ui.sButton.clicked.connect(
            functools.partial(self.set_pivot, V.S, H.C)
        )
        self.ui.swButton.clicked.connect(
            functools.partial(self.set_pivot, V.S, H.W)
        )
        self.ui.setButton.clicked.connect(
            functools.partial(self.set_pivot, None, None)
        )
        # align
        self.ui.alignLButton.clicked.connect(
            functools.partial(self.align_pivot, op.AlignType2D.L)
        )
        self.ui.alignVCButton.clicked.connect(
            functools.partial(self.align_pivot, op.AlignType2D.VC)
        )
        self.ui.alignRButton.clicked.connect(
            functools.partial(self.align_pivot, op.AlignType2D.R)
        )
        self.ui.alignTButton.clicked.connect(
            functools.partial(self.align_pivot, op.AlignType2D.T)
        )
        self.ui.alignHCButton.clicked.connect(
            functools.partial(self.align_pivot, op.AlignType2D.HC)
        )
        self.ui.alignBButton.clicked.connect(
            functools.partial(self.align_pivot, op.AlignType2D.B)
        )
        # ui
        self.ui.xIsLockCheckBox.stateChanged.connect(self.x_lock_changed)
        self.ui.yIsLockCheckBox.stateChanged.connect(self.y_lock_changed)
        #
        self.ui.minimizeButton.clicked.connect(functools.partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

    def x_lock_changed(self):
        self.ui.xLineEdit.setEnabled(not self.ui.xIsLockCheckBox.isChecked())
        self.ui.alignRButton.setEnabled(not self.ui.xIsLockCheckBox.isChecked())
        self.ui.alignVCButton.setEnabled(not self.ui.xIsLockCheckBox.isChecked())
        self.ui.alignLButton.setEnabled(not self.ui.xIsLockCheckBox.isChecked())

    def y_lock_changed(self):
        self.ui.yLineEdit.setEnabled(not self.ui.yIsLockCheckBox.isChecked())
        self.ui.alignTButton.setEnabled(not self.ui.yIsLockCheckBox.isChecked())
        self.ui.alignHCButton.setEnabled(not self.ui.yIsLockCheckBox.isChecked())
        self.ui.alignBButton.setEnabled(not self.ui.yIsLockCheckBox.isChecked())

    def set_pivot(self, v: V, h: H) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print('Fusion Pageで実行してください。')
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print('コンポジションが見付かりません。')
            return

        x_attr = 'TOOLI_ImageWidth'
        y_attr = 'TOOLI_ImageHeight'

        tools = comp.GetToolList(True)

        comp.Lock()
        comp.StartUndo('RS Set Pivot')
        for tool in tools.values():
            pvt = tool.GetInput('Pivot', comp.CurrentTime)
            if pvt is None:
                continue

            # input number
            if None in [v, h]:
                tool.Pivot[comp.CurrentTime] = {
                    1: pvt[1] if self.ui.xIsLockCheckBox.isChecked() else float(self.ui.xLineEdit.text()),
                    2: pvt[2] if self.ui.yIsLockCheckBox.isChecked() else float(self.ui.yLineEdit.text()),
                }
                continue

            # input
            inp = tool.FindMainInput(1)
            if inp is None:
                continue
            attr = tool.GetAttrs()
            if x_attr not in attr.keys() or y_attr not in attr.keys():
                continue

            x_size = tool.GetAttrs()[x_attr]
            y_size = tool.GetAttrs()[y_attr]
            outp = inp.GetConnectedOutput()
            if None in (outp, x_size, y_size):
                continue
            dod = outp.GetDoD()
            if dod is None:
                dod = {1: 0, 2: 0, 3: x_size, 4: y_size}
            x, y = 0, 0
            if h == H.W:
                x = dod[1] / x_size
            elif h == H.C:
                x = (dod[1] + dod[3]) / (2 * x_size)
            elif h == H.E:
                x = dod[3] / x_size
            if v == V.S:
                y = dod[2] / y_size
            elif v == V.C:
                y = (dod[2] + dod[4]) / (2 * y_size)
            elif v == V.N:
                y = dod[4] / y_size

            tool.Pivot[comp.CurrentTime] = {
                1: pvt[1] if self.ui.xIsLockCheckBox.isChecked() else x,
                2: pvt[2] if self.ui.yIsLockCheckBox.isChecked() else y,
            }

        comp.EndUndo(True)
        comp.Unlock()

    def align_pivot(self, align_type: op.AlignType2D) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print('Fusion Pageで実行してください。')
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print('コンポジションが見付かりません。')
            return
        op.align2d(comp, 'Pivot', align_type)


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

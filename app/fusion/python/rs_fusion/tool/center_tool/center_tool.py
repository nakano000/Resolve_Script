import sys
from functools import partial
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
from rs_fusion.tool.center_tool.center_tool_ui import Ui_MainWindow

APP_NAME = 'CenterTool'


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
        for w in [
            self.ui.xLineEdit, self.ui.xStepLineEdit, self.ui.xInfLineEdit, self.ui.xSupLineEdit,
            self.ui.yLineEdit, self.ui.yStepLineEdit, self.ui.yInfLineEdit, self.ui.ySupLineEdit,
        ]:
            w.setText(str(0.0))
            w.setValidator(QDoubleValidator())
        self.ui.xLineEdit.setText(str(0.5))
        self.ui.yLineEdit.setText(str(0.5))
        self.ui.xSupLineEdit.setText(str(1.0))
        self.ui.ySupLineEdit.setText(str(1.0))

        # button
        self.ui.setXButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.setYButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.setButton.setStyleSheet(appearance.in_stylesheet)

        self.ui.randomXButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.randomYButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.randomButton.setStyleSheet(appearance.in_stylesheet)

        # event

        # align
        self.ui.alignLButton.clicked.connect(
            partial(self.align_center, op.AlignType2D.L)
        )
        self.ui.alignVCButton.clicked.connect(
            partial(self.align_center, op.AlignType2D.VC)
        )
        self.ui.alignRButton.clicked.connect(
            partial(self.align_center, op.AlignType2D.R)
        )
        self.ui.alignTButton.clicked.connect(
            partial(self.align_center, op.AlignType2D.T)
        )
        self.ui.alignHCButton.clicked.connect(
            partial(self.align_center, op.AlignType2D.HC)
        )
        self.ui.alignBButton.clicked.connect(
            partial(self.align_center, op.AlignType2D.B)
        )
        # distribute
        self.ui.distributeVButton.clicked.connect(
            partial(self.distribute_center, True)
        )
        self.ui.distributeHButton.clicked.connect(
            partial(self.distribute_center, False)
        )
        # set
        self.ui.setXButton.clicked.connect(
            partial(self.set_center, False, True)
        )
        self.ui.setYButton.clicked.connect(
            partial(self.set_center, True, False)
        )
        self.ui.setButton.clicked.connect(
            partial(self.set_center, False, False)
        )
        # random
        self.ui.randomXButton.clicked.connect(
            partial(self.random_center, False, True)
        )
        self.ui.randomYButton.clicked.connect(
            partial(self.random_center, True, False)
        )
        self.ui.randomButton.clicked.connect(
            partial(self.random_center, False, False)
        )
        # ui

        #
        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.ui.closeButton.clicked.connect(self.close)

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

    def align_center(self, align_type: op.AlignType2D) -> None:
        comp = self.get_comp()
        if comp is None:
            return
        if self.ui.useDodCheckBox.isChecked():
            op.align_dod(self.fusion, comp, 'Center', align_type, self.ui.useCanvasCheckBox.isChecked())
        else:
            op.align2d(comp, 'Center', align_type, self.ui.useCanvasCheckBox.isChecked())

    def distribute_center(self, is_x) -> None:
        comp = self.get_comp()
        if comp is None:
            return
        if self.ui.useDodCheckBox.isChecked():
            op.distribute_dod(
                self.fusion, comp, 'Center', is_x,
                self.ui.randomRadioButton.isChecked(),
                self.ui.useCanvasCheckBox.isChecked(),
            )
        else:
            op.distribute2d(
                comp, 'Center', is_x,
                self.ui.randomRadioButton.isChecked(),
                self.ui.useCanvasCheckBox.isChecked(),
            )

    def set_center(self, lock_x, lock_y) -> None:
        comp = self.get_comp()
        if comp is None:
            return

        op.set_value2d(
            comp,
            'Center',
            x=float(self.ui.xLineEdit.text()),
            y=float(self.ui.yLineEdit.text()),
            x_step=float(self.ui.xStepLineEdit.text()),
            y_step=float(self.ui.yStepLineEdit.text()),
            lock_x=lock_x,
            lock_y=lock_y,
            is_abs=self.ui.absoluteRadioButton.isChecked(),
            is_random=self.ui.randomRadioButton.isChecked(),
        )

    def random_center(self, lock_x, lock_y) -> None:
        comp = self.get_comp()
        if comp is None:
            return

        op.random_value2d(
            comp,
            'Center',
            x_inf=float(self.ui.xInfLineEdit.text()),
            y_inf=float(self.ui.yInfLineEdit.text()),
            x_suo=float(self.ui.xSupLineEdit.text()),
            y_sup=float(self.ui.ySupLineEdit.text()),
            lock_x=lock_x,
            lock_y=lock_y,
            is_abs=self.ui.absoluteRadioButton.isChecked(),
            is_random=self.ui.randomRadioButton.isChecked(),
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

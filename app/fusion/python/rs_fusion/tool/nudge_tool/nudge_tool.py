import sys
import functools
from PySide6.QtCore import (
    Qt,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op
from rs_fusion.tool.nudge_tool.nudge_tool_ui import Ui_MainWindow

APP_NAME = 'NudgeTool'


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
        self.resize(150, 150)

        self.fusion = fusion

        # button
        self.ui.upButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.downButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.leftButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.rightButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.num01Button.clicked.connect(functools.partial(self.set_value, 1))
        self.ui.num02Button.clicked.connect(functools.partial(self.set_value, 2))
        self.ui.num03Button.clicked.connect(functools.partial(self.set_value, 3))
        self.ui.num04Button.clicked.connect(functools.partial(self.set_value, 4))
        self.ui.num05Button.clicked.connect(functools.partial(self.set_value, 5))
        self.ui.num06Button.clicked.connect(functools.partial(self.set_value, 6))
        self.ui.num07Button.clicked.connect(functools.partial(self.set_value, 7))
        self.ui.num08Button.clicked.connect(functools.partial(self.set_value, 8))
        self.ui.num09Button.clicked.connect(functools.partial(self.set_value, 9))
        self.ui.num10Button.clicked.connect(functools.partial(self.set_value, 10))

        self.ui.upButton.clicked.connect(self.up)
        self.ui.downButton.clicked.connect(self.down)
        self.ui.leftButton.clicked.connect(self.left)
        self.ui.rightButton.clicked.connect(self.right)

        self.ui.closeButton.clicked.connect(self.close)

    def get_comp(self):
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print('Please run on Fusion Page.')
            return None

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print('Composition not found.')
            return None
        return comp

    def set_value(self, value):
        scale = 0.01
        if not self.ui.zero2RadioButton.isChecked():
            scale = 0.001

        self.ui.doubleSpinBox.setValue(value * scale)

    def up(self):
        self.move_center(0, 1)

    def down(self):
        self.move_center(0, -1)

    def left(self):
        self.move_center(-1, 0)

    def right(self):
        self.move_center(1, 0)

    def move_center(self, x, y):
        comp = self.get_comp()
        if comp is None:
            return
        value = self.ui.doubleSpinBox.value()
        op.set_value2d(
            comp,
            'Center',
            x=x * value,
            y=y * value,
            x_step=0.0,
            y_step=0.0,
            lock_x=False,
            lock_y=False,
            is_abs=False,
            is_random=False,
            use_key=False,
            key_index=1,
        )

    def show(self) -> None:
        super().show()
        self.ui.doubleSpinBox.setValue(0.01)
        self.ui.doubleSpinBox.setFocus()


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

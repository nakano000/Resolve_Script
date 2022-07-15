import sys
from functools import partial
from pathlib import Path
from typing import List

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from rs.core import (
    pipe as p,
)
from rs.gui import appearance

from rs_fusion.tool.tatie import run as tatie_run

APP_NAME = 'RS Launcher'


class MainWindow(QWidget):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(200, 10)

        self.fusion = fusion

        # button

        self.close_button = QPushButton('close', self)
        self.close_button.setMinimumHeight(40)

        # layout
        lo = QVBoxLayout()
        lo.setContentsMargins(5, 5, 5, 5)

        # launcher btn
        lst: List[dict] = [
            {
                'name': '立ち絵アシスタント',
                'ss': appearance.other_stylesheet,
                'f': partial(tatie_run, self.fusion),
            },
        ]
        for i in lst:
            btn = QPushButton()
            btn.setText(i['name'])
            btn.setMinimumHeight(40)
            btn.setStyleSheet(i['ss'])
            btn.clicked.connect(i['f'])
            lo.addWidget(btn)

        lo.addItem(
            QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        lo.addWidget(self.close_button)
        self.setLayout(lo)

        # event
        self.close_button.clicked.connect(self.close)


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

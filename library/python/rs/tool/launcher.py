import sys
import json
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
    config,
    pipe as p,
)
from rs.gui import appearance
from rs.gui.script_button import ScriptButton

APP_NAME = 'りぞりぷと'
__version__ = '0.10.0'

MENU_JSON = config.ROOT_PATH.joinpath('data', 'app', 'launcher_menu.json')


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('%s  其ノ%s' % (APP_NAME, __version__))
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(200, 10)

        # button

        self.close_button = QPushButton('close', self)
        self.close_button.setMinimumHeight(40)

        # layout
        lo = QVBoxLayout()
        lo.setContentsMargins(5, 5, 5, 5)
        # import json
        lst: List[dict] = p.pipe(
            MENU_JSON.read_text(),
            json.loads,
            list,
        )
        for i in lst:
            btn = ScriptButton(i['name'], script_path=Path(config.ROOT_PATH.joinpath(i['path'])))
            btn.setMinimumHeight(40)
            ss = '\n'.join([
                'background-color: %s;' % i['color'],
                'color: rgb(255, 255, 255);',
            ])
            btn.setStyleSheet(ss)
            lo.addWidget(btn)

        lo.addItem(
            QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        lo.addWidget(self.close_button)
        self.setLayout(lo)

        # event
        self.close_button.clicked.connect(self.close)


def run() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.setStyle("Fusion")

    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

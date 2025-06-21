import json
import re
import sys
from functools import partial
from pathlib import Path

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QToolButton,
    QMenu,
    QMessageBox,
)

from rs.core import (
    config,
    lang,
    pipe as p,
    util,
)
from rs.gui import appearance
from rs.gui.lang.lang import MainWindow as LangWindow
from rs.gui.script_button import ScriptButton

APP_NAME = 'りぞりぷと'
APP_NAME_EN = 'RIZORIPUTO'
__version__ = '2.7.0'

MENU_JSON = config.ROOT_PATH.joinpath('data', 'app', 'launcher_menu.json')

SS_DICT = {
    'picture': appearance.ex_stylesheet,
    'sound': appearance.in_stylesheet,
    'utility': appearance.other_stylesheet,
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.set_title()
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(180, 10)

        # lang window
        self.lang_window = LangWindow(self)

        # button
        self.option_button = QToolButton(self)
        self.option_button.setText('⁝')
        self.option_button.setToolTip('option')
        self.option_button.setMinimumHeight(30)
        self.option_button.setMinimumWidth(30)
        self.option_button.setPopupMode(QToolButton.InstantPopup)
        self.close_button = QPushButton('close', self)
        self.close_button.setMinimumHeight(30)
        self.close_button.setToolTip('close')
        self.minimize_button = QToolButton(self)
        self.minimize_button.setArrowType(Qt.DownArrow)
        self.minimize_button.setMinimumHeight(30)
        self.minimize_button.setMinimumWidth(30)
        self.minimize_button.setToolTip('minimize')

        # menu
        lst = [
            ('Lang', self.lang_window.show),
        ]
        menu = QMenu(self.option_button)
        for x in lst:
            act = QAction(x[0], self.option_button)
            act.triggered.connect(x[1])
            menu.addAction(act)
        self.option_button.setMenu(menu)

        # layout
        lo = QVBoxLayout()
        lo.setContentsMargins(5, 5, 5, 5)
        # import json
        for i in p.pipe(
                MENU_JSON.read_text(encoding='utf-8'),
                json.loads,
                list,
        ):
            if util.IS_WIN:
                if i['win'] is False:
                    continue
            elif util.IS_MAC:
                if i['mac'] is False:
                    continue
            else:
                if i['linux'] is False:
                    continue
            btn = ScriptButton(i['name'], script_path=Path(config.ROOT_PATH.joinpath(i['path'])))
            btn.setMinimumHeight(40)
            btn.setStyleSheet(SS_DICT[i['ss']])
            lo.addWidget(btn)

        lo.addItem(
            QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        lo2 = QHBoxLayout()
        lo2.addWidget(self.option_button)
        lo2.addWidget(self.minimize_button)
        lo2.addWidget(self.close_button)
        lo.addLayout(lo2)
        self.setLayout(lo)
        # event
        self.close_button.clicked.connect(self.close)
        self.minimize_button.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))
        self.lang_window.ui.setButton.clicked.connect(self.set_title)

        # check
        if re.search(r'[ぁ-ん]+|[ァ-ヴー]+|[一-龠]+', str(config.ROOT_PATH)):
            lang_code: lang.Code = lang.load()
            comment = 'パスに日本語が含まれています。\nツールを別の場所に移動してください。'
            if lang_code == lang.Code.en:
                comment = 'The path contains Japanese.\nPlease move the tool to another location.'
            QMessageBox.warning(
                self,
                'Warning',
                f'{str(config.ROOT_PATH)}\n\n{comment}'
            )

    def set_title(self):
        lang_code: lang.Code = lang.load()
        title = '%s  其ノ%s' % (APP_NAME, __version__)
        if lang_code == lang.Code.en:
            title = '%s  %s' % (APP_NAME_EN, __version__)
        self.setWindowTitle(title)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

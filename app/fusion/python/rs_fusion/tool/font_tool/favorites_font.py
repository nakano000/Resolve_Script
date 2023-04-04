import sys

from pathlib import Path
from typing import List
import dataclasses
from PySide2.QtCore import (
    Qt,
    QModelIndex,
    QStringListModel,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QAction,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
)
from rs_fusion.tool.font_tool.favorites_font_ui import Ui_MainWindow


@dataclasses.dataclass
class ConfigData(config.Data):
    favorites: List[str] = dataclasses.field(default_factory=list)


class Model(QStringListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.favorites = []

    def data(self, index: QModelIndex, role: int = ...) -> str:
        if role == Qt.DisplayRole:
            text = super().data(index, role)
            if text in self.favorites:
                text = f'●{text}'
            return text
        return super().data(index, role)


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Favorites')
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            # | Qt.WindowStaysOnTopHint
        )
        self.resize(300, 500)
        self.fusion = fusion

        # config
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.config_file: Path = config.CONFIG_DIR.joinpath('favorite_font.json')
        self.favorites = []

        # action
        self.check_action = QAction('check', self)
        self.check_action.triggered.connect(self.check)
        self.addAction(self.check_action)
        self.uncheck_action = QAction('uncheck', self)
        self.uncheck_action.triggered.connect(self.uncheck)
        self.addAction(self.uncheck_action)

        # listView
        lst = list(self.fusion.FontManager.GetFontList().keys())
        v = self.ui.listView
        m = Model(lst)
        m.favorites = self.favorites
        v.setModel(m)

        v.setContextMenuPolicy(Qt.CustomContextMenu)
        v.customContextMenuRequested.connect(self.contextMenu)

        # style sheet
        self.ui.setButton.setStyleSheet(appearance.ex_stylesheet)

        # event

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.setButton.clicked.connect(self.save)

    def contextMenu(self, pos):
        v = self.ui.listView
        menu = QMenu(v)
        menu.addAction(self.check_action)
        menu.addAction(self.uncheck_action)
        menu.exec_(v.mapToGlobal(pos))

    def favorites_update(self):
        v = self.ui.listView
        m = v.model()
        m.favorites = self.favorites
        v.viewport().update()

    def check(self):
        v = self.ui.listView
        indexes = v.selectedIndexes()
        fav = set(self.favorites)
        for index in indexes:
            fav.add(index.data(Qt.EditRole))
        self.favorites = sorted(list(fav))
        self.favorites_update()

    def uncheck(self):
        v = self.ui.listView
        indexes = v.selectedIndexes()
        fav = set(self.favorites)
        for index in indexes:
            fav.discard(index.data(Qt.EditRole))
        self.favorites = sorted(list(fav))
        self.favorites_update()

    def open(self) -> None:
        if self.config_file.is_file():
            c = ConfigData()
            c.load(self.config_file)
            self.favorites = c.favorites
        else:
            self.favorites = []
        self.favorites_update()

    def save(self) -> None:
        c = ConfigData()
        c.favorites = self.favorites
        c.save(self.config_file)
        self.close()

    def show(self) -> None:
        self.open()
        super().show()


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())

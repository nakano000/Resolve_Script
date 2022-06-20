import subprocess
import sys
from functools import partial

from PySide2.QtCore import (
    QDir,
    QFileSystemWatcher,
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileSystemModel,
    QHeaderView,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from rs.core import (
    config,
)
from rs.gui import appearance
from rs.gui.frame_layout import Form as FrameLayout
from rs.tool.script_launcher.preset_form.preset_form import Form as PresetForm

APP_NAME = 'ScriptLauncher'


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('%s' % APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(300, 300)

        self.comp_path = config.ROOT_PATH.joinpath('Scripts', 'Comp')

        # sub window
        self.preset_window = PresetForm()
        # button
        self.open_button = QPushButton('open', self)
        self.open_button.setMinimumHeight(30)
        self.open_button.setStyleSheet(appearance.in_stylesheet)
        self.close_button = QPushButton('close', self)
        self.close_button.setMinimumHeight(40)

        # tree view
        self.compTreeView = QTreeView()
        self.compTreeView.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        for v in [self.compTreeView]:
            model = QFileSystemModel()
            model.setOption(QFileSystemModel.DontWatchForChanges)
            model.setFilter(QDir.Files)
            model.setNameFilters(['*.py', '*.py2', '*.py3', '*.lua'])
            model.setNameFilterDisables(False)
            v.setDragEnabled(True)
            v.setModel(model)
            v.setSortingEnabled(True)
            v.sortByColumn(0, Qt.AscendingOrder)
            v.setItemsExpandable(False)
            v.setRootIsDecorated(False)
            v.hideColumn(1)
            v.hideColumn(2)
            v.hideColumn(3)

            # header
            h = v.header()
            h.setStretchLastSection(False)
            h.setSectionResizeMode(0, QHeaderView.Stretch)
            h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            # h.setSortIndicator(0, Qt.SortOrder.DescendingOrder)

        # watcher
        self.comp_watcher = QFileSystemWatcher(self)
        self.comp_watcher.directoryChanged.connect(self.comp_directory_changed)
        self.set_tree_root(self.compTreeView, self.comp_watcher, self.comp_path)

        # FrameLayout
        preset_fl = FrameLayout()
        preset_fl.setText('Preset')
        preset_fl.setStyleSheetToTitle(appearance.other_stylesheet)
        preset_lo = QVBoxLayout()
        preset_lo.addWidget(self.open_button)
        preset_fl.setLayout(preset_lo)

        comp_fl = FrameLayout()

        comp_fl.setText('Comp')
        comp_fl.setStyleSheetToTitle(appearance.ex_stylesheet)
        comp_lo = QVBoxLayout()
        comp_lo.addWidget(self.compTreeView)
        comp_fl.setLayout(comp_lo)

        # layout
        lo = QVBoxLayout()
        lo.setContentsMargins(5, 5, 5, 5)
        lo.addWidget(preset_fl)
        lo.addWidget(comp_fl)

        lo.addItem(
            QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )
        lo.addWidget(self.close_button)
        self.setLayout(lo)

        # event
        self.compTreeView.doubleClicked.connect(partial(self.open_dir, self.comp_path))
        self.open_button.clicked.connect(self.preset_window.show)
        self.close_button.clicked.connect(self.close)

    def comp_directory_changed(self, s):
        self.reset_tree(self.compTreeView, self.comp_path)

    @staticmethod
    def set_tree_root(v, w, path):
        flag = path.is_dir()
        v.setEnabled(flag)
        if flag:
            m = v.model()
            _index = m.setRootPath(str(path))
            v.setRootIndex(_index)
            w.removePaths(w.directories())
            w.removePaths(w.files())
            w.addPath(str(path))

    @staticmethod
    def reset_tree(v, path):
        model = v.model()
        model.setRootPath("")
        model.setRootPath(str(path))

    @staticmethod
    def open_dir(path, _):
        subprocess.Popen(['explorer', str(path)])


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

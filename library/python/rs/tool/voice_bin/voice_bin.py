import dataclasses
import os
import json
import re
import sys
import soundfile
import subprocess

from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QDir,
    QItemSelectionModel,
    QFileSystemWatcher,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QWidget,
    QHeaderView,
)
from PySide2.QtGui import (
    QColor,
)

from rs.core import (
    config,
    pipe as p,
    read_aloud_cmd,
    srt,
)
from rs.gui import (
    appearance,
    log,
)
from rs.tool.voice_bin.voice_bin_ui import Ui_Form

APP_NAME = 'VoiceBin'


@dataclasses.dataclass
class ConfigData(config.Data):
    voice_dir: str = ''


class Form(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(400, 600)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # tree view
        model = QFileSystemModel()
        model.setOption(QFileSystemModel.DontWatchForChanges)
        model.setFilter(QDir.Files)
        model.setNameFilters(['*.wav', '*.srt'])
        model.setNameFilterDisables(False)
        v = self.ui.treeView
        v.setModel(model)
        v.setSortingEnabled(True)
        v.sortByColumn(0, Qt.AscendingOrder)
        v.setItemsExpandable(False)
        v.setRootIsDecorated(False)
        v.hideColumn(1)
        v.hideColumn(2)

        # header
        h = v.header()
        h.setStretchLastSection(False)
        h.setSectionResizeMode(0, QHeaderView.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        h.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        h.setSortIndicator(3, Qt.SortOrder.DescendingOrder)

        # watcher
        self.watcher = QFileSystemWatcher(self)
        self.watcher.directoryChanged.connect(self.directory_changed)

        self.set_tree_root()

        # event
        self.ui.treeView.doubleClicked.connect(self.open_dir)
        self.ui.folderLineEdit.textChanged.connect(self.set_tree_root)

        self.ui.closeButton.clicked.connect(self.close)

        self.ui.folderToolButton.clicked.connect(self.folderToolButton_clicked)

    def directory_changed(self, s):
        d = Path(s)
        tree = self.ui.treeView
        model = tree.model()
        sel = tree.selectionModel()

        for f in p.pipe(
                d.iterdir(),
                p.filter(p.call.is_file()),
                p.filter(lambda x: x.suffix in ['.wav']),
        ):
            f: Path
            txt_file = d.joinpath(f.stem + '.txt')
            srt_file = d.joinpath(f.stem + '.srt')
            if txt_file.is_file() and not srt_file.is_file():
                wave_data, samplerate = soundfile.read(str(f))
                _d: float = float(wave_data.shape[0]) / samplerate

                srt_data = srt.Srt()
                try:
                    t = txt_file.read_text(encoding='utf-8')
                except:
                    t = txt_file.read_text(encoding='shift_jis')

                srt_data.subtitles.append(srt.Subtitle(0, _d, t))

                wasBlocked = self.watcher.blockSignals(True)
                srt_data.save(srt_file)
                self.watcher.blockSignals(wasBlocked)
                wav_index = model.index(str(f))
                srt_index = model.index(str(srt_file))
                sel.clearSelection()
                sel.select(wav_index, QItemSelectionModel.Select)
                sel.select(srt_index, QItemSelectionModel.Select)

        self.reset_tree()

    def set_tree_root(self):
        path = Path(self.ui.folderLineEdit.text())
        flag = path.is_dir()
        v = self.ui.treeView
        v.setEnabled(flag)
        if flag:
            m = v.model()
            _index = m.setRootPath(str(path))
            v.setRootIndex(_index)
            self.watcher.removePaths(self.watcher.directories())
            self.watcher.removePaths(self.watcher.files())
            self.watcher.addPath(str(path))

    def reset_tree(self):
        model = self.ui.treeView.model()
        model.setRootPath("")
        model.setRootPath(str(Path(self.ui.folderLineEdit.text())))

    def open_dir(self):
        subprocess.Popen(['explorer', self.ui.folderLineEdit.text().strip().replace('/', '\\')])

    def folderToolButton_clicked(self) -> None:
        w = self.ui.folderLineEdit
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        self.ui.folderLineEdit.setText(c.voice_dir)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.voice_dir = self.ui.folderLineEdit.text()
        return c

    def load_config(self) -> None:
        c = self.new_config()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_data()
        c.save(self.config_file)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = Form()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

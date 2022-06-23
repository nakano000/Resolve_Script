import re

import dataclasses
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

from rs.core import (
    config,
    pipe as p,
    srt,
    ffmpeg,
)
from rs.gui import (
    appearance,
)
from rs.tool.voice_bin.chara_data import CharaData
from rs.tool.voice_bin.voice_bin_ui import Ui_Form
from rs.tool.voice_bin.chara_setting import MainWindow as CharaWindow

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

        script_base_file: Path = config.ROOT_PATH.joinpath('data', 'app', APP_NAME, 'script_base.txt')
        self.script_base: str = script_base_file.read_text(encoding='utf-8')

        # window
        self.chara_window = CharaWindow(self)

        # button
        self.ui.dragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.charaButton.setStyleSheet(appearance.in_stylesheet)

        # tree view
        for v in [self.ui.treeView, self.ui.movTreeView]:
            model = QFileSystemModel()
            model.setOption(QFileSystemModel.DontWatchForChanges)
            model.setFilter(QDir.Files)
            model.setNameFilterDisables(False)
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
        self.ui.treeView.model().setNameFilters(['*.wav', '*.srt'])
        self.ui.movTreeView.model().setNameFilters(['*.mov'])

        # watcher
        self.watcher = QFileSystemWatcher(self)
        self.watcher.directoryChanged.connect(self.directory_changed)

        self.set_tree_root()

        # event
        self.ui.charaButton.clicked.connect(self.chara_window.show)

        self.ui.treeView.doubleClicked.connect(self.open_dir)
        self.ui.movTreeView.doubleClicked.connect(self.open_dir)
        self.ui.movTreeView.selectionModel().selectionChanged.connect(self.set_lua)

        self.ui.folderLineEdit.textChanged.connect(self.set_tree_root)

        self.ui.closeButton.clicked.connect(self.close)

        self.ui.folderToolButton.clicked.connect(self.folderToolButton_clicked)

    def set_lua(self):
        v = self.ui.movTreeView
        m: QFileSystemModel = v.model()
        sel = v.selectionModel()
        lst = sel.selectedIndexes()
        if len(lst) > 0:
            mov_path = Path(m.filePath(lst[0]))
            path = mov_path.parent.joinpath(mov_path.stem + '.lua')
            self.ui.dragButton.setLuaFile(path)

    def directory_changed(self, s):
        d = Path(s)
        tree = self.ui.treeView
        model = tree.model()
        sel = tree.selectionModel()

        mov_tree = self.ui.movTreeView
        mov_model = mov_tree.model()
        mov_sel = mov_tree.selectionModel()

        for f in p.pipe(
                d.iterdir(),
                p.filter(p.call.is_file()),
                p.filter(lambda x: x.suffix in ['.wav']),
        ):
            f: Path
            txt_file = d.joinpath(f.stem + '.txt')
            srt_file = d.joinpath(f.stem + '.srt')
            lua_file = d.joinpath(f.stem + '.lua')
            mov_file = d.joinpath(f.stem + '.mov')
            srt_flag = not srt_file.is_file()
            lua_flag = not lua_file.is_file()
            if txt_file.is_file() and (srt_flag or lua_flag):
                try:
                    t = txt_file.read_text(encoding='utf-8')
                except:
                    t = txt_file.read_text(encoding='shift_jis')

                if srt_flag:
                    wave_data, samplerate = soundfile.read(str(f))
                    _d: float = float(wave_data.shape[0]) / samplerate

                    srt_data = srt.Srt()

                    srt_data.subtitles.append(srt.Subtitle(0, _d, t))

                    wasBlocked = self.watcher.blockSignals(True)
                    srt_data.save(srt_file)
                    self.watcher.blockSignals(wasBlocked)
                    wav_index = model.index(str(f))
                    srt_index = model.index(str(srt_file))
                    sel.clearSelection()
                    sel.select(wav_index, QItemSelectionModel.Select)
                    sel.select(srt_index, QItemSelectionModel.Select)
                if lua_flag and self.ui.tabWidget.currentIndex() == 1:
                    chara_data = CharaData()
                    for cd in self.chara_window.get_chara_list():
                        cd: CharaData
                        m = re.fullmatch(cd.reg_exp, f.stem)
                        if m is not None:
                            chara_data = cd
                            break
                    lua = self.script_base % (t, chara_data.color, str(chara_data.setting_file))
                    wasBlocked = self.watcher.blockSignals(True)
                    lua_file.write_text(lua, encoding='utf-8')
                    ffmpeg.execute(ffmpeg.make_args(f, mov_file))
                    self.watcher.blockSignals(wasBlocked)
                    index = mov_model.index(str(mov_file))
                    mov_sel.clearSelection()
                    mov_sel.select(index, QItemSelectionModel.Select)

        self.reset_tree()

    def set_tree_root(self):
        path = Path(self.ui.folderLineEdit.text())
        flag = path.is_dir()
        for v in [self.ui.treeView, self.ui.movTreeView]:
            v.setEnabled(flag)
            if flag:
                m = v.model()
                _index = m.setRootPath(str(path))
                v.setRootIndex(_index)
        if flag:
            self.watcher.removePaths(self.watcher.directories())
            self.watcher.removePaths(self.watcher.files())
            self.watcher.addPath(str(path))

    def reset_tree(self):
        for v in [self.ui.treeView, self.ui.movTreeView]:
            model = v.model()
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

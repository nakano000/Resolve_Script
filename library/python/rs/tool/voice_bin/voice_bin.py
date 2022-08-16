import chardet
import dataclasses
import re
import soundfile
import subprocess
import sys
from functools import partial
from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QDir,
    QItemSelectionModel,
    Signal,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QWidget,
    QHeaderView,
)

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from rs.core import (
    config,
    pipe as p,
    srt,
    lab,
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
    fps: float = 30.0


class WatchdogEvent(FileSystemEventHandler):
    def __init__(self, sig):
        super(WatchdogEvent, self).__init__()
        self.modified: Signal = sig
        self.created_lst = []
        self.moved_lst = []
        self.deleted_lst = []

    def on_created(self, event):
        src_path = Path(event.src_path)
        # print('created', src_path)
        if src_path.suffix.lower() in ['.wav', '.txt', '.lab']:
            self.created_lst.append(src_path)

    def on_modified(self, event):
        src_path = Path(event.src_path)
        # print('modified', src_path)
        if src_path.is_dir():
            flag = False
            for lst in [self.created_lst, self.moved_lst, self.deleted_lst]:
                if len(lst) > 0:
                    flag = True
                    lst.clear()
            if flag:
                self.modified.emit(str(src_path))

    def on_moved(self, event):
        src_path = Path(event.src_path)
        # print('moved', src_path)
        self.moved_lst.append(src_path)

    def on_deleted(self, event):
        src_path = Path(event.src_path)
        # print('deleted', src_path)
        if src_path.suffix.lower() in ['.wav', '.srt']:
            self.deleted_lst.append(src_path)


def read_text(f: Path, c_code: str):
    # 文字コード
    _code = c_code.strip().lower()

    if _code in ['auto', '']:
        with open(f, 'rb') as _f:
            content = _f.read()
            char_code = chardet.detect(content)
        enc: str = char_code['encoding']

        if enc is None or enc.lower() not in [
            'utf-8',
            'utf-8-sig',
            'utf-16',
            'utf-16be',
            'utf-16le',
            'utf-32',
            'utf-32be',
            'utf-32le',
            'cp932',
            'shift_jis',
        ]:
            try:
                t = content.decode(encoding='utf-8')
            except:
                t = content.decode(encoding='cp932')
        else:
            if enc.lower() == 'shift_jis':
                enc = 'cp932'
            t = content.decode(encoding=enc)
    else:
        t = f.read_text(encoding=_code)

    # 改行コード
    t = t.replace('\r\n', '\n')
    return t


class Form(QWidget):
    modified = Signal(str)

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

        text_script_base_file: Path = config.ROOT_PATH.joinpath('data', 'app', APP_NAME, 'text_script_base.txt')
        self.text_script_base: str = text_script_base_file.read_text(encoding='utf-8')
        tatie_script_base_file: Path = config.ROOT_PATH.joinpath('data', 'app', APP_NAME, 'tatie_script_base.txt')
        self.tatie_script_base: str = tatie_script_base_file.read_text(encoding='utf-8')
        tatie_setting_base_file: Path = config.ROOT_PATH.joinpath('data', 'app', APP_NAME, 'tatie_setting_base.txt')
        self.tatie_setting_base: str = tatie_setting_base_file.read_text(encoding='utf-8')

        # window
        self.chara_window = CharaWindow(self)

        # button
        self.ui.dragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.tatieDragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.charaButton.setStyleSheet(appearance.in_stylesheet)

        # tree view
        for v in [self.ui.treeView, self.ui.wavTreeView]:
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
        self.ui.wavTreeView.model().setNameFilters(['*.wav'])
        self.sel_wav = ''
        self.sel_srt = ''
        # watcher
        self.modified.connect(self.directory_changed)
        self.__observer = PollingObserver()
        self.set_tree_root()

        # event
        self.ui.charaButton.clicked.connect(self.chara_window.show)
        self.ui.minimizeButton.clicked.connect(partial(self.setWindowState, Qt.WindowMinimized))

        self.ui.treeView.doubleClicked.connect(self.open_dir)
        self.ui.wavTreeView.doubleClicked.connect(self.open_dir)
        self.ui.wavTreeView.selectionModel().selectionChanged.connect(self.set_lua)

        self.ui.folderLineEdit.textChanged.connect(self.set_tree_root)

        self.ui.closeButton.clicked.connect(self.close)

        self.ui.folderToolButton.clicked.connect(self.folderToolButton_clicked)

    def start(self):
        path = Path(self.ui.folderLineEdit.text())
        if path.is_dir():
            if self.__observer.is_alive():
                self.__observer.stop()
                self.__observer.join()
            self.__observer = PollingObserver()
            self.__observer.schedule(WatchdogEvent(self.modified), str(path), True)
            self.__observer.start()

    def stop(self):
        if self.__observer.is_alive():
            self.__observer.stop()
            self.__observer.join()

    def set_lua(self):
        v = self.ui.wavTreeView
        m: QFileSystemModel = v.model()
        sel = v.selectionModel()
        lst = sel.selectedIndexes()
        if len(lst) > 0:
            wav_path = Path(m.filePath(lst[0]))
            path = wav_path.parent.joinpath(wav_path.stem + '.lua')
            tatie_path = wav_path.parent.joinpath(wav_path.stem + '.tatie.lua')
            self.ui.dragButton.setLuaFile(path)
            self.ui.tatieDragButton.setLuaFile(tatie_path)

    def directory_changed(self, s):
        d = Path(s)
        tree = self.ui.treeView
        model = tree.model()
        sel = tree.selectionModel()

        txt_tree = self.ui.wavTreeView
        txt_model = txt_tree.model()
        txt_sel = txt_tree.selectionModel()

        for f in p.pipe(
                d.iterdir(),
                p.filter(p.call.is_file()),
                p.filter(lambda x: x.suffix in ['.wav']),
        ):
            f: Path
            txt_file = d.joinpath(f.stem + '.txt')
            srt_file = d.joinpath(f.stem + '.srt')
            lab_file = d.joinpath(f.stem + '.lab')

            lua_file = d.joinpath(f.stem + '.lua')
            tatie_lua_file = d.joinpath(f.stem + '.tatie.lua')
            setting_file = d.joinpath(f.stem + '.setting')

            # flag
            srt_flag = not srt_file.is_file()
            lua_flag = not lua_file.is_file()
            setting_flag = lab_file.is_file() and not setting_file.is_file()
            if txt_file.is_file() and (srt_flag or lua_flag or setting_file):
                chara_data = CharaData()
                for cd in self.chara_window.get_chara_list():
                    cd: CharaData
                    m = re.fullmatch(cd.reg_exp, f.stem)
                    if m is not None:
                        chara_data = cd
                        break

                t = read_text(txt_file, chara_data.c_code)

                if srt_flag:
                    wave_data, samplerate = soundfile.read(str(f))
                    _d: float = float(wave_data.shape[0]) / samplerate

                    srt_data = srt.Srt()

                    srt_data.subtitles.append(srt.Subtitle(0, _d, t))

                    srt_data.save(srt_file)
                    self.sel_wav = str(f)
                    self.sel_srt = str(srt_file)
                if lua_flag:
                    lua = self.text_script_base % (
                        t,
                        chara_data.color,
                        chara_data.track_name,
                        str(chara_data.setting_file)
                    )
                    lua_file.write_text(lua, encoding='utf-8')
                if setting_flag:
                    data = self.get_data()
                    setting = self.tatie_setting_base % (
                        t.replace('\n', '\\n').replace('"', '\\"'),
                        lab.lab2anim(lab_file, data.fps)
                    )
                    setting_file.write_text(setting, encoding='utf-8')
                    tatie_lua = self.tatie_script_base % (
                        chara_data.color,
                        chara_data.track_name,
                        str(setting_file)
                    )
                    tatie_lua_file.write_text(tatie_lua, encoding='utf-8')
        self.reset_tree()
        if self.sel_wav != '':
            sel.clearSelection()
            sel.select(model.index(self.sel_srt.replace('\\', '/')), QItemSelectionModel.Select)
            sel.select(model.index(self.sel_wav.replace('\\', '/')), QItemSelectionModel.Select)
        if self.sel_wav != '':
            txt_sel.clearSelection()
            txt_sel.select(txt_model.index(self.sel_wav), QItemSelectionModel.Select)

    def set_tree_root(self):
        path = Path(self.ui.folderLineEdit.text())
        flag = path.is_dir()
        for v in [self.ui.treeView, self.ui.wavTreeView]:
            v.setEnabled(flag)
            if flag:
                m = v.model()
                _index = m.setRootPath(str(path))
                v.setRootIndex(_index)

        self.stop()
        self.start()

    def _reset_tree(self, v):
        model: QFileSystemModel = v.model()
        model.setRootPath("")
        model.setRootPath(str(Path(self.ui.folderLineEdit.text())))

    def reset_tree(self):
        for v in [self.ui.treeView, self.ui.wavTreeView]:
            self._reset_tree(v)

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
        self.ui.fpsSpinBox.setValue(c.fps)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.voice_dir = self.ui.folderLineEdit.text()
        c.fps = self.ui.fpsSpinBox.value()
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

    def show(self) -> None:
        self.start()
        super().show()

    def closeEvent(self, event):
        self.stop()
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

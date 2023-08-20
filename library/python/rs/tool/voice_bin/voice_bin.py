import dataclasses
import subprocess
import sys
from functools import partial
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QDir,
    QItemSelectionModel,
    Signal,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QWidget,
    QHeaderView,
    QProgressDialog,
)

from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler

from rs.core import (
    config,
    pipe as p,
    voice_bin_process,
)
from rs.gui import (
    appearance,
)
from rs.tool.voice_bin.voice_bin_ui import Ui_Form
from rs.gui.chara.chara import MainWindow as CharaWindow

APP_NAME = 'VoiceBin'


@dataclasses.dataclass
class ConfigData(config.Data):
    voice_dir: str = ''
    fps: float = 30.0
    tab_index: int = 0


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
            self.created_lst.append(str(src_path))

    def on_modified(self, event):
        src_path = Path(event.src_path)
        # print('modified', src_path)
        if src_path.is_dir():
            if len(self.created_lst) + len(self.moved_lst) + len(self.deleted_lst) > 0:
                self.modified.emit(str(src_path), self.created_lst.copy())
                self.created_lst.clear()
                self.moved_lst.clear()
                self.deleted_lst.clear()

    def on_moved(self, event):
        src_path = Path(event.src_path)
        # print('moved', src_path)
        self.moved_lst.append(str(src_path))

    def on_deleted(self, event):
        src_path = Path(event.src_path)
        # print('deleted', src_path)
        if src_path.suffix.lower() in ['.wav', '.srt']:
            self.deleted_lst.append(str(src_path))


class Form(QWidget):
    modified = Signal(str, list)

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

        # window
        self.chara_window = CharaWindow(self)
        self.chara_window.set_comment('※出力済みの音声に適応するには、スクリプトのRebuildが必要です。')

        # button
        self.ui.dragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.tatieDragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.wDragButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.charaButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.rebuildButton.setStyleSheet(appearance.other_stylesheet)

        # tree view
        for v in [self.ui.treeView, self.ui.wavTreeView]:
            model = QFileSystemModel()
            model.setOption(QFileSystemModel.Option.DontWatchForChanges)
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
            h.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            h.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            h.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            h.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
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
        self.ui.rebuildButton.clicked.connect(self.rebuild_all, Qt.QueuedConnection)
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
            self.ui.wDragButton.setLuaFiles(path, tatie_path)

    def directory_changed(self, s, created_lst):
        d = Path(s)
        tree = self.ui.treeView
        model = tree.model()
        sel = tree.selectionModel()

        txt_tree = self.ui.wavTreeView
        txt_model = txt_tree.model()
        txt_sel = txt_tree.selectionModel()
        file_list = p.pipe(
            d.iterdir(),
            p.filter(p.call.is_file()),
            p.filter(lambda x: x.suffix in ['.wav']),
            list,
        ) if len(created_lst) == 0 else p.pipe(
            created_lst,
            p.map(lambda x: Path(x).parent.joinpath(Path(x).stem + '.wav')),
            p.filter(p.call.is_file()),
            dict.fromkeys,
            list,
        )

        # main
        for f in file_list:
            QApplication.processEvents()
            data = self.get_data()
            if voice_bin_process.run(f, data.fps):
                self.sel_wav = str(f)
                self.sel_srt = str(d.joinpath(f.stem + '.srt'))

        # update TreeView
        self.reset_tree()
        if self.sel_wav != '':
            sel.clearSelection()
            sel.select(model.index(self.sel_srt.replace('\\', '/')), QItemSelectionModel.SelectionFlag.Select)
            sel.select(model.index(self.sel_wav.replace('\\', '/')), QItemSelectionModel.SelectionFlag.Select)
        if self.sel_wav != '':
            txt_sel.clearSelection()
            txt_sel.select(txt_model.index(self.sel_wav), QItemSelectionModel.SelectionFlag.Select)

    def rebuild_all(self):
        c = self.get_data()
        d = Path(c.voice_dir)

        progress_dialog = QProgressDialog(
            'processing....', None, 0, 0, None,
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        progress_dialog.setWindowTitle("rebuild")
        progress_dialog.show()
        QApplication.processEvents()
        for f in p.pipe(
                d.iterdir(),
                p.filter(p.call.is_file()),
                p.filter(lambda x: x.suffix in ['.srt', '.lua', '.setting']),
        ):
            f.unlink()
            QApplication.processEvents()
        self.directory_changed(c.voice_dir, [])

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

    @staticmethod
    def new_config():
        return ConfigData()

    def set_data(self, c: ConfigData):
        self.ui.folderLineEdit.setText(c.voice_dir)
        self.ui.fpsSpinBox.setValue(c.fps)
        self.ui.tabWidget.setCurrentIndex(c.tab_index)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.voice_dir = self.ui.folderLineEdit.text()
        c.fps = self.ui.fpsSpinBox.value()
        c.tab_index = self.ui.tabWidget.currentIndex()
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
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

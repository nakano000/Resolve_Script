import dataclasses
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
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QMainWindow,
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
from rs.tool.text2wave.base.base_ui import Ui_MainWindow


@dataclasses.dataclass
class ConfigData(config.Data):
    out_dir: str = ''
    cmd: read_aloud_cmd.Data = dataclasses.field(default_factory=read_aloud_cmd.Data)

    def save_voice_template(self, path: Path) -> None:
        dct = dataclasses.asdict(self)
        del dct['out_dir']
        cmd_data = dct['cmd']
        for key in ['exe_path', 'text']:
            del cmd_data[key]
        path.write_text(
            json.dumps(dct, indent=2),
            encoding='utf-8',
        )


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        # exe_name
        self.exe_name = '*.exe'
        self.template_dir = config.ROOT_PATH.joinpath('data', 'template')

        # tree view
        model = QFileSystemModel()
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

        self.set_tree_root()

        # style sheet
        self.ui.exportButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        self.ui.treeView.doubleClicked.connect(self.open_out_dir)

        self.ui.exeToolButton.clicked.connect(self.exeToolButton_clicked)
        self.ui.outToolButton.clicked.connect(self.outToolButton_clicked)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.exportButton.clicked.connect(self.export, Qt.QueuedConnection)

        self.ui.outLineEdit.textChanged.connect(self.set_tree_root)

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_Voice_Template.triggered.connect(self.save_voice_template)
        self.ui.actionExit.triggered.connect(self.close)

    def open_out_dir(self):
        subprocess.Popen(['explorer', self.ui.outLineEdit.text().strip().replace('/', '\\')])

    def set_tree_root(self):
        path = Path(self.ui.outLineEdit.text())
        f = path.is_dir()
        v = self.ui.treeView
        v.setEnabled(f)
        if f:
            m = v.model()
            _index = m.setRootPath(str(path))
            v.setRootIndex(_index)

    def reset_tree(self):
        model = self.ui.treeView.model()
        model.setRootPath("");
        model.setRootPath(str(Path(self.ui.outLineEdit.text())));

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        self.ui.outLineEdit.setText(c.out_dir)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.out_dir = self.ui.outLineEdit.text()
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

    def open(self, is_template=False) -> None:
        dir_path = str(self.template_dir) if is_template else self.ui.outLineEdit.text().strip()
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            dir_path,
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                c = self.get_data()
                c.load(file_path)
                self.set_data(c)

    def save(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            self.ui.outLineEdit.text().strip(),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            c = self.get_data()
            c.save(file_path)

    def save_voice_template(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save Voice Template',
            str(self.template_dir),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            c = self.get_data()
            c.save_voice_template(file_path)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def exeToolButton_clicked(self) -> None:
        w = self.ui.exeLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select %s' % self.exe_name,
            w.text(),
            '%s(%s)' % (self.exe_name, self.exe_name),
        )
        if path != '':
            w.setText(path)

    def outToolButton_clicked(self) -> None:
        w = self.ui.outLineEdit
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def export_wave(self, path: Path) -> bool:
        data = self.get_data()
        cmd_data = data.cmd
        cmd_data.export(path)
        if path.is_file():
            self.add2log('Export: %s' % str(path))
            return True
        else:
            self.add2log('[ERROR]wav fileの書き出しに失敗しました。', log.ERROR_COLOR)
        return False

    def export(self) -> None:
        self.ui.logTextEdit.clear()

        data = self.get_data()
        cmd_data = data.cmd

        # exe check
        exe: Path = Path(cmd_data.exe_path)
        if exe.is_file():
            self.add2log('%s: %s' % (self.exe_name, str(exe)))
        else:
            self.add2log('[ERROR]%sの設定に失敗しました。' % self.exe_name, log.ERROR_COLOR)
            return

        # out directory check
        out_text = data.out_dir.strip()
        out_dir: Path = Path(out_text)
        if out_dir.is_dir() and out_text != '':
            self.add2log('保存先: %s' % str(out_dir))
        else:
            self.add2log('[ERROR]保存先が存在しません。', log.ERROR_COLOR)
            return

        self.add2log('')  # new line

        # name
        name = p.pipe(
            out_dir.iterdir(),
            p.filter(p.call.is_file()),
            p.map(lambda s: s.name.split('.')),
            p.filter(lambda l: len(l) > 1 and l[0].isdigit()),
            p.map(lambda l: int(l[0])),
            list,
            lambda xs: str(1 if len(xs) == 0 else max(xs) + 1).zfill(4),
            lambda s: '%s.%s' % (s, cmd_data.cid) if hasattr(cmd_data, 'cid') else s,
            lambda s: '%s.%s' % (s, re.sub(r'[\\/:*?"<>|]+', '', cmd_data.text[:5])),
            p.call.replace('\n', ' '),
        )

        # export wav
        wav_file = out_dir.joinpath(name + '.wav')

        self.add2log('処理中(wav file)')
        if not self.export_wave(wav_file):
            return

        self.add2log('')  # new line

        # subtitles
        self.add2log('処理中(srt file)')
        srt_file = out_dir.joinpath(name + '.srt')

        wave_data, samplerate = soundfile.read(str(wav_file))
        _d: float = float(wave_data.shape[0]) / samplerate

        srt_data = srt.Srt()
        srt_data.subtitles.append(srt.Subtitle(0, _d, cmd_data.text))
        srt_data.save(srt_file)
        self.add2log('Export: %s' % str(srt_file))

        self.add2log('')  # new line

        # config file
        self.add2log('設定保存(json file)')
        json_file: Path = out_dir.joinpath(name + '.json')
        data.save(json_file)
        self.add2log('Export: %s' % str(json_file))

        self.add2log('')  # new line
        # end
        self.add2log('Done!')

        self.reset_tree()
        tree = self.ui.treeView
        model = tree.model()
        wav_index = model.index(str(wav_file))
        srt_index = model.index(str(srt_file))
        sel = tree.selectionModel()
        sel.clearSelection()
        sel.select(wav_index, QItemSelectionModel.Select)
        sel.select(srt_index, QItemSelectionModel.Select)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

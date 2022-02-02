import dataclasses
import json
import re
import sys
import wave

from pathlib import Path

from PySide2.QtCore import (
    Qt,
    QDir,
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

from yr.core import (
    config,
    pipe as p,
    softalk,
    srt,
)
from yr.gui import appearance
from yr.tool.softalk2resolve.softalk2resolve_ui import Ui_MainWindow

TEXT_COLOR = QColor(210, 210, 210)
ERROR_COLOR = QColor(210, 0, 0)

APP_NAME = 'softalk2resolve'


@dataclasses.dataclass
class ConfigData(config.Data):
    from yr.core import (
        softalk as st,
    )
    out_dir: str = ''
    softalk: st.Data = dataclasses.field(default_factory=st.Data)

    def save_voice_template(self, path: Path) -> None:
        dct = dataclasses.asdict(self)
        del dct['out_dir']
        st = dct['softalk']
        for key in ['softalkw_path', 'text']:
            del st[key]
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
        self.setWindowTitle(APP_NAME)

        # combobox
        self.ui.voiceComboBox.addItems(softalk.VOICE_LIST)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

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

        self.set_tree_root()

        # event
        self.ui.softalkwToolButton.clicked.connect(self.softalkwToolButton_clicked)
        self.ui.outToolButton.clicked.connect(self.outToolButton_clicked)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.exportButton.clicked.connect(self.export)

        self.ui.outLineEdit.textChanged.connect(self.set_tree_root)

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_Voice_Template.triggered.connect(self.save_voice_template)
        self.ui.actionExit.triggered.connect(self.close)

    def set_tree_root(self):
        path = Path(self.ui.outLineEdit.text())
        f = path.is_dir()
        v = self.ui.treeView
        v.setEnabled(f)
        if f:
            m = v.model()
            _index = m.setRootPath(str(path))
            v.setRootIndex(_index)

    def set_data(self, c: ConfigData):
        st = c.softalk

        self.ui.softalkwLineEdit.setText(st.softalkw_path)

        self.ui.outLineEdit.setText(c.out_dir)

        self.ui.voiceComboBox.setCurrentText(st.voice)
        self.ui.volumeSpinBox.setValue(st.volume)
        self.ui.speedSpinBox.setValue(st.speed)
        self.ui.pitchSpinBox.setValue(st.pitch)
        self.ui.plainTextEdit.setPlainText(st.text)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        st = c.softalk

        st.softalkw_path = self.ui.softalkwLineEdit.text()

        c.out_dir = self.ui.outLineEdit.text()

        st.voice = self.ui.voiceComboBox.currentText()
        st.volume = self.ui.volumeSpinBox.value()
        st.speed = self.ui.speedSpinBox.value()
        st.pitch = self.ui.pitchSpinBox.value()
        st.text = self.ui.plainTextEdit.toPlainText()

        return c

    def load_config(self) -> None:
        c = ConfigData()
        if self.config_file.is_file():
            c.load(self.config_file)
        self.set_data(c)

    def save_config(self) -> None:
        config.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        c = self.get_data()
        c.save(self.config_file)

    def open(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            '',
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
            '',
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
            '',
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            c = self.get_data()
            c.save_voice_template(file_path)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)

    def add2log(self, text: str, color: QColor = TEXT_COLOR) -> None:
        log = self.ui.logTextEdit
        log.setTextColor(color)
        log.append(text)
        log.setTextColor(TEXT_COLOR)
        log.repaint()

    def softalkwToolButton_clicked(self) -> None:
        w = self.ui.softalkwLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select softalkw.exe',
            w.text(),
            'softalkw.exe(softalkw.exe)'
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

    def export(self) -> None:
        self.ui.logTextEdit.clear()

        data = self.get_data()
        st = data.softalk

        # softalkw check
        softalkw: Path = Path(st.softalkw_path)
        if softalkw.is_file():
            self.add2log('softalkw: %s' % str(softalkw))
        else:
            self.add2log('[ERROR]softalkw.exeの設定に失敗しました。', ERROR_COLOR)
            return

        # out directory check
        out_text = data.out_dir.strip()
        out_dir: Path = Path(out_text)
        if out_dir.is_dir() and out_text != '':
            self.add2log('保存先: %s' % str(out_dir))
        else:
            self.add2log('[ERROR]保存先が存在しません。', ERROR_COLOR)
            return

        self.add2log('')  # new line

        # name
        _name = p.pipe(
            out_dir.iterdir(),
            p.filter(p.call.is_file()),
            p.map(lambda s: s.name.split('.')),
            p.filter(lambda l: len(l) > 1 and l[0].isdigit()),
            p.map(lambda l: int(l[0])),
            list,
            lambda xs: str(1 if len(xs) == 0 else max(xs) + 1).zfill(4),
            lambda s: '%s.%s' % (s, re.sub(r'[\\/:*?"<>|]+', '', st.text[:5])),
            p.call.replace('\n', ' '),
        )

        # export wav
        _wav_file = out_dir.joinpath(_name + '.wav')

        self.add2log('処理中(wav file)')
        st.export(_wav_file)
        if _wav_file.is_file():
            self.add2log('Export: %s' % str(_wav_file))
        else:
            self.add2log('[ERROR]wav fileの書き出しに失敗しました。', ERROR_COLOR)
            return

        self.add2log('')  # new line

        # subtitles
        self.add2log('処理中(srt file)')
        _srt_file = out_dir.joinpath(_name + '.srt')
        _d: float = 0.0
        with wave.open(str(_wav_file), 'rb') as f:
            _d = float(f.getnframes()) / f.getframerate()
        _srt = srt.Srt()
        _srt.subtitles.append(srt.Subtitle(0, _d, st.text))
        _srt.save(_srt_file)
        self.add2log('Export: %s' % str(_srt_file))

        self.add2log('')  # new line

        # config file
        self.add2log('設定保存(json file)')
        _json_file = out_dir.joinpath(_name + '.json')
        data.save(_json_file)
        self.add2log('Export: %s' % str(_json_file))

        self.add2log('')  # new line
        # end
        self.add2log('Done!')


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

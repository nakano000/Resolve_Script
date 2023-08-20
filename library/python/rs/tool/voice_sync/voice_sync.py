import dataclasses
import os
import sys
import shutil
from functools import partial
from itertools import zip_longest
from pathlib import Path

import numpy as np
import scipy.signal as signal
import soundfile as sf
import pyworld as pw
import pytsmod as tsm

from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QHeaderView,
)

from rs.core import (
    config,
    lab,
    lab_romaji,
    pipe as p,
)
from rs.gui import (
    appearance,
    log,
)
from rs.tool.voice_sync.voice_sync_ui import Ui_MainWindow
from rs.tool.voice_sync.check_timing import MainWindow as CheckWindow

from rs.tool.voice_sync.wav_table import InputData

APP_NAME = 'VoiceSync'


@dataclasses.dataclass
class ConfigData(config.Data):
    # talk tab
    src_file: str = ''
    use_auto_set: bool = True
    src_lab_file: str = ''

    # tab
    tab_index: int = 0

    # dst
    dst_file: str = ''

    # ref
    ref_lab_file: str = ''
    use_pau_comp: bool = True
    repeat: int = 0
    exclude_end: bool = True

    # replace
    use_replace: bool = False
    replaced_wav_file: str = ''
    pitch_wav_file: str = ''
    ap_value: float = 1.0

    # table
    src_list: config.DataList = dataclasses.field(default_factory=lambda: config.DataList(InputData))


class MainWindow(QMainWindow):
    modified = Signal(str, list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            # | Qt.WindowCloseButtonHint
            # | Qt.WindowStaysOnTopHint
        )
        self.resize(800, 900)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.set_data(ConfigData())
        self.sampling_rate = 48000

        # window
        self.check_window = CheckWindow(self)

        # table
        v = self.ui.wavTableView
        h = v.horizontalHeader()
        h.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        h.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # button
        self.ui.syncButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.checkButton.setStyleSheet(appearance.other_stylesheet)

        self.ui.addButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.readButton.setStyleSheet(appearance.other_stylesheet)
        self.ui.copyButton.setStyleSheet(appearance.ex_stylesheet)

        # event
        self.ui.srcToolButton.clicked.connect(self.get_wav_name)
        self.ui.srcLabToolButton.clicked.connect(partial(self.get_open_file_name, self.ui.srcLabLineEdit, 'lab'))
        self.ui.refLabToolButton.clicked.connect(partial(self.get_open_file_name, self.ui.refLabLineEdit, 'lab'))

        self.ui.pitchWavToolButton.clicked.connect(partial(self.get_open_file_name, self.ui.pitchWavLineEdit, 'wav'))

        self.ui.replacedWavToolButton.clicked.connect(
            partial(self.get_save_file_name, self.ui.replacedWavLineEdit, 'wav')
        )
        self.ui.dstToolButton.clicked.connect(partial(self.get_save_file_name, self.ui.dstLineEdit, 'wav'))

        self.ui.readButton.clicked.connect(self.read_lyrics)
        self.ui.copyButton.clicked.connect(self.copy_lyrics)

        self.ui.addButton.clicked.connect(self.add_table)
        self.ui.clearButton.clicked.connect(self.clear_table)

        self.ui.checkButton.clicked.connect(self.check)
        self.ui.syncButton.clicked.connect(self.sync_voice)
        self.ui.closeButton.clicked.connect(self.close)

        # menu
        self.ui.actionNew.triggered.connect(self.new_file)
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionExit.triggered.connect(self.close)

    @staticmethod
    def pau_comp(lab_data):
        """pau、sil、brを一つにまとめる"""
        r = []
        _sub_list = None
        for d in lab_data:
            if d['sign'] in ['sil', 'pau', 'br']:
                if _sub_list is None:
                    _sub_list = []
                    r.append(_sub_list)
                _sub_list.append(d)
            else:
                _sub_list = None
                r.append(d)
        for i, d in enumerate(r):
            if isinstance(d, list):
                if len(d) == 1:
                    r[i] = d[0]
                else:
                    r[i] = {
                        's': d[0]['s'],
                        'e': d[-1]['e'],
                        'sign': 'pau'
                    }
        return r

    @staticmethod
    def repeat_vowel(lab_data, repeat: int, exclude_end: bool):
        """母音を繰り返す"""
        if repeat == 0:
            return lab_data
        r = []
        for j, d in enumerate(lab_data):
            exclude_flag = (
                    j != len(lab_data) - 1
                    and lab_data[j + 1]['sign'] not in ['sil', 'pau', 'br']
            ) if exclude_end else True

            if d['sign'] in ['a', 'i', 'u', 'e', 'o'] and exclude_flag:
                _l = int((d['e'] - d['s']) / (repeat + 1.0))
                for i in range(repeat + 1):
                    _d = {
                        's': d['s'] + _l * i,
                        'e': d['s'] + _l * (i + 1),
                        'sign': d['sign']
                    }
                    if i == repeat:
                        _d['e'] = d['e']
                    r.append(_d)
            else:
                r.append(d)
        return r

    def _pitch_replace_process(self):
        SR = self.sampling_rate

        def read_wav(path: Path):
            wav_data, _sr = sf.read(str(path))
            wav_data = signal.resample(
                wav_data,
                round(len(wav_data) * float(SR) / _sr),
            )
            temp_file = path.with_suffix('.tmp.wav')
            for i in range(1000):
                if temp_file.is_file():
                    temp_file = temp_file.with_suffix('.tmp%d.wav' % i)
                else:
                    break
            sf.write(str(temp_file), wav_data, SR)
            result, _ = sf.read(str(temp_file))
            temp_file.unlink()
            return result

        # get data
        config_data = self.get_data()
        src_file = Path(config_data.dst_file)
        ref_file = Path(config_data.pitch_wav_file)
        ap_value = config_data.ap_value

        # read wav
        src_data = read_wav(src_file)
        ref_data = read_wav(ref_file)
        # mono
        if len(src_data.shape) > 1:
            src_data = src_data[:, 0].copy(order='c')
        if len(ref_data.shape) > 1:
            ref_data = np.asarray(ref_data[:, 0]).copy(order='c')
        # 長さを合わせる
        if len(src_data) > len(ref_data):
            src_data = src_data[:len(ref_data)]
        if len(ref_data) > len(src_data):
            ref_data = ref_data[:len(src_data)]
        # normalize
        src_data = src_data / (np.nanmax(np.abs(src_data)))
        ref_data = ref_data / (np.nanmax(np.abs(ref_data)))

        # pitch replace
        _f0, _t = pw.harvest(ref_data, SR, f0_floor=110.0, f0_ceil=783.991)
        f0 = pw.stonemask(ref_data, _f0, _t, SR)

        sp = pw.cheaptrick(src_data, f0, _t, SR)
        ap = pw.d4c(src_data, f0, _t, SR)

        y = pw.synthesize(f0, sp, ap * ap_value, SR)
        return y / (np.nanmax(np.abs(y)))

    def _sync_voice_process(self):
        N = 10000000
        SR = self.sampling_rate

        def resample(_f: Path):
            _clip, _sr = sf.read(str(_f))
            _num = round(len(_clip) * float(SR) / _sr)
            return signal.resample(_clip, _num)

        def to_pos(_d):
            return int(_d * SR / N)

        def read_pos(_data):
            return p.pipe(
                _data,
                p.map(lambda x: to_pos(x['s'])),
                list,
            )

        # get data
        config_data = self.get_data()
        is_talk = config_data.tab_index == 0
        w = self.ui.wavTableView

        src_file_list = [Path(config_data.src_file)] if is_talk else w.get_wav_list()
        src_lab_file_list = [Path(config_data.src_lab_file)] if is_talk else w.get_lab_list()

        ref_lab_file = Path(config_data.ref_lab_file)

        # read src
        src_data_list = p.pipe(
            zip(src_file_list, src_lab_file_list),
            p.map(lambda x: (resample(x[0]), lab.read(x[1]))),
            list,
        )
        self.add2log('Read wav and lab.')

        # read ref
        ref_lab_data = lab.read(ref_lab_file)
        self.add2log('Read ref.')
        if config_data.use_pau_comp:
            ref_lab_data = self.pau_comp(ref_lab_data)
        ref_lab_data = self.repeat_vowel(ref_lab_data, config_data.repeat, config_data.exclude_end)

        # wav and lab
        wav_list = []
        lab_data = []
        _end_point = 0
        for i, src_data in enumerate(src_data_list):
            _wav_data, _lab_data = src_data
            if i != len(src_data_list) - 1:
                # lab:最後が無音なら削除。
                if _lab_data[-1]['sign'] in ['sil', 'pau', 'br']:
                    _lab_data.pop()
            else:
                # lab:無音で終っていなければ無音を追加。ai voice対策
                if _lab_data[-1]['sign'] not in ['sil', 'pau', 'br']:
                    _lab_data.append({
                        's': _lab_data[-1]['e'],
                        'e': int(len(_wav_data) * N / SR),
                        'sign': 'pau'
                    })
            # wav
            last_pos = to_pos(_lab_data[-1]['e'])
            if len(_wav_data) < last_pos:
                last_pos = len(_wav_data)
            wav_list.append(_wav_data[: last_pos])
            # lab
            for _lab in _lab_data:
                _lab['s'] += _end_point
                _lab['e'] += _end_point
            _end_point = _lab_data[-1]['e']
            lab_data.extend(_lab_data)
        wav_data = np.concatenate(wav_list)

        # get pos
        pos_list: list = read_pos(lab_data)
        end_pos = len(wav_data)
        pos_list.append(end_pos)

        pos2_list: list = read_pos(ref_lab_data)
        end_pos2 = to_pos(ref_lab_data[len(pos2_list) - 1]['e'])
        pos2_list.append(end_pos2)

        if len(pos_list) > len(pos2_list):
            _d = pos2_list[-1] - pos_list[len(pos2_list) - 1]
            pos2_list.extend(p.pipe(
                pos_list[len(pos2_list): len(pos_list)],
                p.map(lambda x: x + _d),
                list,
            ))

        time_map = np.array([pos_list, pos2_list])
        x = wav_data.T
        remapped = tsm.wsola(x, time_map)
        return remapped.T

    def sync_voice(self):
        self.ui.logTextEdit.clear()

        # get data
        config_data = self.get_data()
        is_talk = config_data.tab_index == 0
        use_replace = config_data.use_replace
        w = self.ui.wavTableView

        # src wav
        src_file_list = [Path(config_data.src_file)] if is_talk else w.get_wav_list()
        if len(src_file_list) == 0:
            self.add2log('Error: 音声ファイルがありません。', log.ERROR_COLOR)
            return

        for f in src_file_list:
            if not f.is_file():
                self.add2log(f'Error: 音声ファイルがありません。{f.name}', log.ERROR_COLOR)
                return

        # src lab
        src_lab_file_list = [Path(config_data.src_lab_file)] if is_talk else w.get_lab_list()
        if len(src_lab_file_list) == 0:
            self.add2log('Error: 音素タイミングファイルがありません。', log.ERROR_COLOR)
            return

        for f in src_lab_file_list:
            if not f.is_file():
                self.add2log(f'Error: 音素タイミングファイルがありません。{f.name}', log.ERROR_COLOR)
                return

        # ref lab
        ref_lab_file = Path(config_data.ref_lab_file)
        if not ref_lab_file.is_file():
            self.add2log(f'Error: 変換用音素タイミングファイルがありません。{ref_lab_file.name}', log.ERROR_COLOR)
            return

        # replaced wav
        replaced_wav_file = Path(config_data.replaced_wav_file)
        pitch_wav_file = Path(config_data.pitch_wav_file)
        if use_replace:
            if not pitch_wav_file.is_file():
                self.add2log(f'Error: 音程参照用音声ファイルがありません。{pitch_wav_file.name}', log.ERROR_COLOR)
                return
            replaced_wav_file.parent.mkdir(parents=True, exist_ok=True)

        # dst
        dst = Path(config_data.dst_file)
        dst.parent.mkdir(parents=True, exist_ok=True)

        # sync
        self.add2log('Sync processing...')
        result = self._sync_voice_process()

        # save
        dst.parent.mkdir(parents=True, exist_ok=True)

        dst_lab_file = dst.with_suffix('.lab')
        shutil.copyfile(ref_lab_file, dst_lab_file)
        self.add2log('Copy: %s' % dst_lab_file.name)
        if is_talk:
            src_file = src_file_list[0]
            src_txt_file = src_file.with_suffix('.txt')
            dst_txt_file = dst.with_suffix('.txt')
            if src_txt_file.is_file():
                shutil.copyfile(src_txt_file, dst_txt_file)
                self.add2log('Copy: %s' % dst_txt_file.name)
        try:
            sf.write(str(dst), result, self.sampling_rate)
        except RuntimeError:
            self.add2log('Error: wavファイルの保存に失敗しました。', log.ERROR_COLOR)
            return
        self.add2log('Save: %s' % dst.name)

        # pitch replace
        if use_replace:
            self.add2log('Pitch replace...')
            replaced_data = self._pitch_replace_process()
            try:
                sf.write(str(replaced_wav_file), replaced_data, self.sampling_rate)
            except RuntimeError:
                self.add2log('Error: wavファイルの保存に失敗しました。', log.ERROR_COLOR)
                return
            self.add2log('Save: %s' % replaced_wav_file.name)

        # end
        self.add2log('Done!')

    def check(self):
        # get data
        config_data = self.get_data()
        is_talk = config_data.tab_index == 0
        w = self.ui.wavTableView

        # src lab file
        src_lab_file_list = [Path(config_data.src_lab_file)] if is_talk else w.get_lab_list()

        for f in src_lab_file_list:
            if not f.is_file():
                self.add2log(f'Error: 音素タイミングファイルがありません。{f.name}', log.ERROR_COLOR)
                return

        ref_lab_file = Path(config_data.ref_lab_file)
        if not ref_lab_file.is_file():
            self.add2log('Error: 変換用タイミングファイルがありません。', log.ERROR_COLOR)
            return

        # lab
        src_lab_data_list = p.pipe(
            src_lab_file_list,
            p.map(lambda x: lab.read(x)),
            list,
        )
        src_data = []
        number_list = []
        for i, _lab_data in enumerate(src_lab_data_list):
            _src_data = p.pipe(
                _lab_data,
                p.map(lambda x: x['sign']),
                list,
            )
            if i != len(src_lab_data_list) - 1:
                # lab:無音を削除。
                if _src_data[-1] in ['sil', 'pau', 'br']:
                    _src_data.pop()
            else:
                # lab:無音で終っていなければ無音を追加。ai voice対策
                if _src_data[-1] not in ['sil', 'pau', 'br']:
                    _src_data.append('pau')
            # lab
            src_data.extend(_src_data)
            number_list.extend(p.pipe(
                range(len(_src_data)),
                p.map(lambda x: '%0d' % (i + 1)),
                list,
            ))

        # ref lab
        ref_lab_data = lab.read(ref_lab_file)
        if config_data.use_pau_comp:
            ref_lab_data = self.pau_comp(ref_lab_data)
        ref_lab_data = self.repeat_vowel(ref_lab_data, config_data.repeat, config_data.exclude_end)

        ref_data = p.pipe(
            ref_lab_data,
            p.map(lambda x: x['sign']),
            list,
        )

        # check
        lst = list(zip_longest(src_data, ref_data, number_list, fillvalue=''))
        self.check_window.set_data(lst)
        self.check_window.show()

    def add_table(self):
        w = self.ui.wavTableView
        type_name = 'wav'
        file_names, _ = QFileDialog.getOpenFileNames(
            self,
            f'Select {type_name.upper()} File',
            '',
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if len(file_names) > 0:
            for path in file_names:
                wav_file = Path(path)
                lab_file = wav_file.with_suffix('.lab')
                lab_path = ''
                if lab_file.is_file():
                    lab_path = str(lab_file).replace('\\', '/')
                w.add(path, lab_path)

    def clear_table(self):
        w = self.ui.wavTableView
        m = w.model()
        m.clear()

    def read_lyrics(self):
        config_data = self.get_data()
        ref_lab_file = Path(config_data.ref_lab_file)
        if not ref_lab_file.is_file():
            self.add2log('Error: 変換用タイミングファイルがありません。', log.ERROR_COLOR)
            return

        data = p.pipe(
            lab.read(ref_lab_file),
            lambda x: self.repeat_vowel(x, config_data.repeat, config_data.exclude_end),
            p.map(lambda x: x['sign']),
            list,
        )
        self.ui.lyricsTextEdit.setText(p.pipe(
            lab_romaji.conv(data).split(' '),
            p.filter(lambda x: x != ''),
            '\n'.join,
        ))

    def copy_lyrics(self):
        text = self.ui.lyricsTextEdit.toPlainText()
        QApplication.clipboard().setText(text)

    def get_open_file_name(self, w, type_name: str) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            f'Select {type_name.upper()} File',
            w.text(),
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if path != '':
            w.setText(path)

    def get_wav_name(self) -> None:
        w = self.ui.srcLineEdit
        type_name = 'wav'
        path, _ = QFileDialog.getOpenFileName(
            self,
            f'Select {type_name.upper()} File',
            w.text(),
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if path != '':
            w.setText(path)
            data = self.get_data()
            if not data.use_auto_set:
                return
            wav_file = Path(path)
            lab_file = wav_file.with_suffix('.lab')
            if lab_file.is_file():
                self.ui.srcLabLineEdit.setText(str(lab_file).replace('\\', '/'))

    def get_save_file_name(self, w, type_name: str) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            'save as',
            w.text(),
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if path != '':
            w.setText(path)

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def set_data(self, c: ConfigData):
        self.ui.srcLineEdit.setText(c.src_file)
        self.ui.useAutoSetCheckBox.setChecked(c.use_auto_set)
        self.ui.srcLabLineEdit.setText(c.src_lab_file)

        self.ui.tabWidget.setCurrentIndex(c.tab_index)

        self.ui.dstLineEdit.setText(c.dst_file)

        self.ui.refLabLineEdit.setText(c.ref_lab_file)
        self.ui.usePauCompCheckBox.setChecked(c.use_pau_comp)
        self.ui.repeatSpinBox.setValue(c.repeat)
        self.ui.excludeEndCheckBox.setChecked(c.exclude_end)

        self.ui.useReplaceGroupBox.setChecked(c.use_replace)
        self.ui.pitchWavLineEdit.setText(c.pitch_wav_file)
        self.ui.replacedWavLineEdit.setText(c.replaced_wav_file)
        self.ui.apValueSpinBox.setValue(c.ap_value)

        self.ui.wavTableView.model().set_data(c.src_list)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_file = self.ui.srcLineEdit.text()
        c.use_auto_set = self.ui.useAutoSetCheckBox.isChecked()
        c.src_lab_file = self.ui.srcLabLineEdit.text()

        c.tab_index = self.ui.tabWidget.currentIndex()

        c.dst_file = self.ui.dstLineEdit.text()

        c.ref_lab_file = self.ui.refLabLineEdit.text()
        c.use_pau_comp = self.ui.usePauCompCheckBox.isChecked()
        c.repeat = self.ui.repeatSpinBox.value()
        c.exclude_end = self.ui.excludeEndCheckBox.isChecked()

        c.use_replace = self.ui.useReplaceGroupBox.isChecked()
        c.pitch_wav_file = self.ui.pitchWavLineEdit.text()
        c.replaced_wav_file = self.ui.replacedWavLineEdit.text()
        c.ap_value = self.ui.apValueSpinBox.value()

        c.src_list.set_list(self.ui.wavTableView.model().to_list())
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

    def new_file(self) -> None:
        c = ConfigData()
        self.set_data(c)

    def open_file(self) -> None:
        type_name = 'json'
        path, _ = QFileDialog.getOpenFileName(
            self,
            f'Select {type_name.upper()} File',
            '',
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if path != '':
            json_file = Path(path)
            if json_file.is_file():
                c = ConfigData()
                c.load(json_file)
                self.set_data(c)

    def save_file(self) -> None:
        type_name = 'json'
        path, _ = QFileDialog.getSaveFileName(
            self,
            'save as',
            '',
            f'{type_name.upper()} File (*.{type_name.lower()})',
        )
        if path != '':
            json_file = Path(path)
            json_file.parent.mkdir(parents=True, exist_ok=True)
            c = self.get_data()
            c.save(json_file)

    # def closeEvent(self, event):
    #     self.save_config()
    #     super().closeEvent(event)


def run() -> None:
    os.environ['PATH'] = str(config.PYTHON_SCRIPTS_PATH) + os.pathsep + os.getenv('PATH')

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

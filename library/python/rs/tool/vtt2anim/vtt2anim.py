import dataclasses
import sys
from pathlib import Path

import webvtt
from timecode import Timecode

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
)
from rs.tool.vtt2anim.vtt2anim_ui import Ui_Form

APP_NAME = 'VTT2Anim'


@dataclasses.dataclass
class ConfigData(config.Data):
    h: int = 1
    m: int = 0
    s: int = 0
    ms: int = 0
    fps: float = 30.0

    def get_timecode(self) -> Timecode:
        return Timecode(self.fps, '%02d:%02d:%02d.%03d' % (self.h, self.m, self.s, self.ms))


def dict2anim(d: dict) -> str:
    header = '\n'.join([
        '{',
        '	TemplateStyledText = BezierSpline {',
        '		KeyFrames = {',
    ])
    key01_block = '			[%d] = { %d,'
    key02_block = ' LHrel = { %f, -0.333333333333333 },'
    key03_block = ' RHrel = { %f, 0.333333333333333 },'
    key04_block = ' Flags = { Linear = true, LockedY = true }, Value = Text {'
    value_block = '\n					Value = "%s"'
    separator = '\n				} },\n'
    footer = '\n'.join([
        '				} }',
        '		}',
        '	}',
        '}',
    ])
    key_list = []
    size = len(d)
    flame_list = list(d.keys())
    for i, frame in enumerate(flame_list):
        s = key01_block % (frame, i)
        if i != 0:
            s += key02_block % ((flame_list[i - 1] - frame)/3.0)
        if i != size - 1:
            s += key03_block % ((flame_list[i + 1] - frame)/3.0)
        s += key04_block
        s += value_block % d[frame].replace('\n', '\\n').replace('"', '\\"')
        key_list.append(s)

    return '\n'.join([
        header,
        separator.join(key_list),
        footer,
    ])


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
        self.resize(400, 400)
        self.setAcceptDrops(True)
        self.ui.dropLabel.setText('VTT file')

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

    def moveEvent(self, e):
        self.ui.dropLabel.setText('VTT file')
        super().moveEvent(e)

    def leaveEvent(self, e):
        self.ui.dropLabel.setText('VTT file')
        super().leaveEvent(e)

    def resizeEvent(self, e):
        self.ui.dropLabel.setText('VTT file')
        super().resizeEvent(e)

    def dragEnterEvent(self, e):
        self.ui.dropLabel.setText('VTT file')
        mimeData = e.mimeData()

        # for mimetype in mimeData.formats():
        #     print('MIMEType:', mimetype)

        if mimeData.hasUrls():
            e.accept()
        else:
            e.ignore()

    def str2frame(self, s: str) -> int:
        data = self.get_data()
        return (Timecode(data.fps, s) - data.get_timecode()).frame_number

    def dropEvent(self, e):
        paths = p.pipe(
            e.mimeData().urls(),
            p.map(p.call.toLocalFile()),
            p.map(Path),
            p.filter(p.call.is_file()),
            p.filter(lambda f: f.name.lower().endswith('.vtt')),
            p.map(str),
            p.map(p.call.replace('\\', '/')),
            list,
            sorted,
        )
        if len(paths) > 0:
            dct = {0: ''}
            for caption in webvtt.read(paths[0]):
                dct[self.str2frame(caption.start)] = caption.text.replace('\ufeff', '')
                dct[self.str2frame(caption.end)] = ''

            clipboard = QApplication.clipboard()
            clipboard.setText(dict2anim(dct))
            self.ui.dropLabel.setText('DONE!')

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        self.ui.hSpinBox.setValue(c.h)
        self.ui.mSpinBox.setValue(c.m)
        self.ui.sSpinBox.setValue(c.s)
        self.ui.msSpinBox.setValue(c.ms)
        self.ui.fpsDoubleSpinBox.setValue(c.fps)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.h = self.ui.hSpinBox.value()
        c.m = self.ui.mSpinBox.value()
        c.s = self.ui.sSpinBox.value()
        c.ms = self.ui.msSpinBox.value()
        c.fps = self.ui.fpsDoubleSpinBox.value()
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

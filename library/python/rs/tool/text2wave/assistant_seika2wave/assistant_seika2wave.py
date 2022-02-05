import dataclasses
import sys

from pathlib import Path
from functools import partial

from PySide2.QtWidgets import (
    QApplication,
    QWidget,
)

from rs.core import (
    config,
    seika_say2,
)
from rs.gui import appearance
from rs.tool.text2wave import base
from rs.tool.text2wave.assistant_seika2wave.seika_say2_ui import Ui_Form

APP_NAME = 'AssistantSeika2wave'


@dataclasses.dataclass
class ConfigData(base.ConfigData):
    cmd: seika_say2.Data = dataclasses.field(default_factory=seika_say2.Data)


class SeikaSay2UI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class MainWindow(base.MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(APP_NAME)
        self.resize(800, 600)
        self.exe_name = seika_say2.EXE_NAME
        self.template_dir = config.ROOT_PATH.joinpath('data', 'template', APP_NAME)
        # label
        self.ui.exeLabel.setText('%sの場所' % self.exe_name)

        ss2_ui = SeikaSay2UI()
        lo = self.ui.SettingLayout.addWidget(ss2_ui)
        self.seika_say2_ui = ss2_ui.ui

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # event
        self.seika_say2_ui.templateButton.clicked.connect(partial(self.open, is_template=True))

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        cmd_data = c.cmd

        self.ui.exeLineEdit.setText(cmd_data.exe_path)

        self.ui.outLineEdit.setText(c.out_dir)

        self.seika_say2_ui.cidLineEdit.setText(cmd_data.cid)
        self.seika_say2_ui.volumeLineEdit.setText(cmd_data.volume)
        self.seika_say2_ui.speedLineEdit.setText(cmd_data.speed)
        self.seika_say2_ui.pitchLineEdit.setText(cmd_data.pitch)
        self.seika_say2_ui.alphaLineEdit.setText(cmd_data.alpha)
        self.seika_say2_ui.intonationLineEdit.setText(cmd_data.intonation)
        self.seika_say2_ui.emotion01LineEdit.setText(cmd_data.emotion01)
        self.seika_say2_ui.emotion02LineEdit.setText(cmd_data.emotion02)

        self.ui.plainTextEdit.setPlainText(cmd_data.text)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        cmd_data = c.cmd

        cmd_data.exe_path = self.ui.exeLineEdit.text()

        c.out_dir = self.ui.outLineEdit.text()

        cmd_data.cid = self.seika_say2_ui.cidLineEdit.text()
        cmd_data.volume = self.seika_say2_ui.volumeLineEdit.text()
        cmd_data.speed = self.seika_say2_ui.speedLineEdit.text()
        cmd_data.pitch = self.seika_say2_ui.pitchLineEdit.text()
        cmd_data.alpha = self.seika_say2_ui.alphaLineEdit.text()
        cmd_data.intonation = self.seika_say2_ui.intonationLineEdit.text()
        cmd_data.emotion01 = self.seika_say2_ui.emotion01LineEdit.text()
        cmd_data.emotion02 = self.seika_say2_ui.emotion02LineEdit.text()

        cmd_data.text = self.ui.plainTextEdit.toPlainText()

        return c


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

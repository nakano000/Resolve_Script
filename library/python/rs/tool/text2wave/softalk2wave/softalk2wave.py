import dataclasses
import sys

from pathlib import Path

from PySide2.QtWidgets import (
    QApplication,
    QWidget,
)

from rs.core import (
    config,
    softalk,
)
from rs.gui import appearance
from rs.tool.text2wave import base
from rs.tool.text2wave.softalk2wave.softalk_ui import Ui_Form

APP_NAME = 'softalk2wave'


@dataclasses.dataclass
class ConfigData(base.ConfigData):
    cmd: softalk.Data = dataclasses.field(default_factory=softalk.Data)


class SoftalkUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class MainWindow(base.MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(APP_NAME)
        self.resize(800, 600)
        self.exe_name = softalk.EXE_NAME
        # label
        self.ui.exeLabel.setText('%sの場所' % self.exe_name)

        st_ui = SoftalkUI()
        lo = self.ui.SettingLayout.addWidget(st_ui)
        self.softalk_ui = st_ui.ui

        # combobox
        self.softalk_ui.voiceComboBox.addItems(softalk.VOICE_LIST)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        cmd_data = c.cmd

        self.ui.exeLineEdit.setText(cmd_data.exe_path)

        self.ui.outLineEdit.setText(c.out_dir)

        self.softalk_ui.voiceComboBox.setCurrentText(cmd_data.voice)
        self.softalk_ui.volumeSpinBox.setValue(cmd_data.volume)
        self.softalk_ui.speedSpinBox.setValue(cmd_data.speed)
        self.softalk_ui.pitchSpinBox.setValue(cmd_data.pitch)
        self.ui.plainTextEdit.setPlainText(cmd_data.text)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        cmd_data = c.cmd

        cmd_data.exe_path = self.ui.exeLineEdit.text()

        c.out_dir = self.ui.outLineEdit.text()

        cmd_data.voice = self.softalk_ui.voiceComboBox.currentText()
        cmd_data.volume = self.softalk_ui.volumeSpinBox.value()
        cmd_data.speed = self.softalk_ui.speedSpinBox.value()
        cmd_data.pitch = self.softalk_ui.pitchSpinBox.value()
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

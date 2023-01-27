import chardet
import dataclasses
import json
import sys

from pathlib import Path

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)
from PySide2.QtGui import (
    QColor,
)

from PIL import Image
from psd_tools import PSDImage
import pykakasi

from rs.core import (
    config,
    util,
)
from rs.gui import (
    appearance,
    log,
)

from rs.tool.psd_splitter.psd_spliter_ui import Ui_MainWindow

APP_NAME = 'PsdSplitter'


@dataclasses.dataclass
class ConfigData(config.Data):
    src_dir: str = ''
    dst_dir: str = ''
    use_cp932: bool = False


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('%s' % APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(600, 600)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # style sheet
        self.ui.splitButton.setStyleSheet(appearance.ex_stylesheet)

        # event

        self.ui.srcToolButton.clicked.connect(self.srcToolButton_clicked)
        self.ui.dstToolButton.clicked.connect(self.dstToolButton_clicked)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.splitButton.clicked.connect(self.split, Qt.QueuedConnection)

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.close)

    def set_data(self, c: ConfigData):
        self.ui.srcLineEdit.setText(c.src_dir)
        self.ui.dstLineEdit.setText(c.dst_dir)
        self.ui.useCp932CheckBox.setChecked(c.use_cp932)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_dir = self.ui.srcLineEdit.text()
        c.dst_dir = self.ui.dstLineEdit.text()
        c.use_cp932 = self.ui.useCp932CheckBox.isChecked()

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

    def open(self, is_template=False) -> None:
        dir_path = str(self.template_dir) if is_template else self.ui.dstLineEdit.text().strip()
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
            self.ui.dstLineEdit.text().strip(),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            c = self.get_data()
            c.save(file_path)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def srcToolButton_clicked(self) -> None:
        w = self.ui.srcLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select PSD File',
            w.text(),
            'PSD File (*.psd)',
        )
        if path != '':
            w.setText(path)

    def dstToolButton_clicked(self) -> None:
        w = self.ui.dstLineEdit
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def export_layer(self, size, d: Path, group):
        kakasi = pykakasi.kakasi()
        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        kakasi.setMode('J', 'a')
        conversion = kakasi.getConverter()
        lst = []
        name_list = []
        for layer in group:
            layer_name: str = layer.name.strip()
            name: str = layer_name.translate(str.maketrans('*\\/:?"<>|', '-________', ''))
            if name == '':
                name = '_none_'
            if name[-1].isdigit():
                name += '_'

            layer_name_en = ''.join(filter(str.isalnum, conversion.do(layer_name)))
            if len(layer_name_en) == 0:
                layer_name_en = ''.join(filter(lambda s: s not in '!@#$%^&*()-=+\\|`~[]{};\':",./<>?', layer_name))
            if len(layer_name_en) == 0:
                layer_name_en = 'none'

            if layer.is_group():
                grp_dir = d.joinpath(name)
                grp_dir.mkdir(parents=True, exist_ok=True)
                self.add2log('Mkdir: %s => %s' % (layer_name, str(grp_dir).replace('\\', '/')))
                dct = {
                    'name': layer_name,
                    'name_en': layer_name_en,
                    'visible': layer.is_visible(),
                    'data': self.export_layer(size, grp_dir, layer),
                }
                lst.append(dct)
            else:
                img = Image.new("RGBA", size, (0, 0, 0, 0))
                if layer.topil() is not None:
                    img.paste(layer.topil(), layer.offset)

                if name in name_list:  # 重複チェック
                    _tmp_name = name + '_'
                    for i in range(100):
                        if _tmp_name not in name_list:
                            break
                        _tmp_name = name + '_' + str(i) + '_'
                    name = _tmp_name

                img_path = d.joinpath(name + '.png')
                img.save(img_path)
                dct = {
                    'name': layer_name,
                    'name_en': layer_name_en,
                    'visible': layer.is_visible(),
                    'data': str(img_path).replace('\\', '/'),
                }
                lst.append(dct)
                name_list.append(name)
                self.add2log('Export: %s => %s' % (dct['name'], dct['data']))
        return lst

    def split(self):
        self.ui.logTextEdit.clear()

        data = self.get_data()

        # src directory check
        src_text = data.src_dir.strip()
        src_file: Path = Path(src_text)
        if src_file.is_file() and src_text != '':
            self.add2log('PSD: %s' % str(src_file))
        else:
            self.add2log('[ERROR]PSDが存在しません。', log.ERROR_COLOR)
            return

        self.add2log('')  # new line

        # dst directory check
        dst_text = data.dst_dir.strip()
        dst_dir: Path = Path(dst_text)
        if dst_dir.is_dir() and dst_text != '':
            self.add2log('出力先: %s' % str(dst_dir))
        else:
            self.add2log('[ERROR]出力先が存在しません。', log.ERROR_COLOR)
            return

        self.add2log('')  # new line
        if not data.use_cp932:
            psd = PSDImage.open(src_file)
        else:
            try:
                psd = PSDImage.open(src_file, encoding='cp932')
            except UnicodeDecodeError:
                self.add2log('[ERROR]CP932でエンコードされていません。', log.ERROR_COLOR)
                return
        out_dir = dst_dir.joinpath(src_file.stem)
        out_dir.mkdir(parents=True, exist_ok=True)
        self.add2log('Mkdir: %s => %s' % (src_file.stem, str(out_dir).replace('\\', '/')))
        json_path = out_dir.joinpath(src_file.stem + '.json')
        util.write_text(
            json_path,
            json.dumps(
                {
                    'name': 'Root',
                    'x': psd.size[0],
                    'y': psd.size[1],
                    'data': self.export_layer(psd.size, out_dir, psd),
                },
                indent=2,
                ensure_ascii=False,
            ),
        )
        self.add2log('')  # new line
        self.add2log('Save JSON: %s' % str(json_path).replace('\\', '/'))
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

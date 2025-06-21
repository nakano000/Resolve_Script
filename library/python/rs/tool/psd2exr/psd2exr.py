import dataclasses
import json
import sys

from pathlib import Path

import OpenEXR
import numpy as np
from psd_tools import PSDImage
from psd_tools.constants import ChannelID
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)
from PySide6.QtGui import (
    QColor,
)

import pykakasi

from rs.core import (
    config,
    util,
)
from rs.gui import (
    appearance,
    log,
)

from rs.tool.psd2exr.psd2exr_ui import Ui_MainWindow

APP_NAME = 'Psd2Exr'


@dataclasses.dataclass
class ConfigData(config.Data):
    src_dir: str = ''


def rename_layer(layer, s):
    if s == '':
        s = layer.name
    else:
        s = s + '.' + layer.name
    if layer.is_group():
        for child in layer:
            rename_layer(child, s)
    else:
        layer.name = s


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('%s' % APP_NAME)
        self.setWindowFlags(
            Qt.Window
            # | Qt.WindowCloseButtonHint
            # | Qt.WindowStaysOnTopHint
        )
        self.resize(600, 600)

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # style sheet
        self.ui.convertButton.setStyleSheet(appearance.ex_stylesheet)

        # event

        self.ui.srcToolButton.clicked.connect(self.srcToolButton_clicked)

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.convertButton.clicked.connect(self.psd_layers_to_exr, Qt.QueuedConnection)

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.close)

    def set_data(self, c: ConfigData):
        self.ui.srcLineEdit.setText(c.src_dir)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_dir = self.ui.srcLineEdit.text()

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
        dir_path = Path(self.ui.srcLineEdit.text().strip()).parent
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            str(dir_path),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if file_path.is_file():
                c = self.get_data()
                c.load(file_path)
                self.set_data(c)

    def save(self) -> None:
        dir_path = Path(self.ui.srcLineEdit.text().strip()).parent
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            str(dir_path),
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

    def get_layer_info(self, group):
        kakasi = pykakasi.kakasi()
        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        kakasi.setMode('J', 'a')
        conversion = kakasi.getConverter()
        lst = []
        for layer in group:
            layer_name: str = layer.name
            layer_name_en = ''.join(filter(str.isalnum, conversion.do(layer_name)))
            if len(layer_name_en) == 0:
                layer_name_en = ''.join(filter(lambda s: s not in '!@#$%^&*()-=+\\|`~[]{};\':",./<>?', layer_name))
            if len(layer_name_en) == 0:
                layer_name_en = 'none'
            dct = {
                'name': layer_name,
                'name_en': layer_name_en,
                'visible': layer.is_visible(),
                'is_group': layer.is_group(),
            }
            if layer.is_group():
                dct['data'] = self.get_layer_info(layer)
            lst.append(dct)
        return lst

    def psd_layers_to_exr(self):
        """
        PSDの各レイヤーをEXRのマルチパートとして保存する
        """
        self.ui.logTextEdit.clear()

        self.add2log('Start PSD to EXR conversion...')

        data = self.get_data()

        psd_file = Path(data.src_dir.strip())
        if not psd_file.is_file():
            self.add2log(
                '[ERROR]PSD file not found.'
                , log.ERROR_COLOR)
            return
        output_exr_file = psd_file.with_suffix('.exr')
        info_file = psd_file.with_suffix('.info.json')

        # PSDファイルを読み込む
        psd = PSDImage.open(psd_file)

        # キャンバスの解像度を取得
        canvas_width, canvas_height = psd.size

        # 色深度
        color_depth = psd.depth
        if color_depth not in [8, ]:
            self.add2log(
                f"[ERROR]Unsupported color depth: {color_depth}. Only 8 bits are supported.",
                log.ERROR_COLOR,
            )
            return

        # rename layers
        for layer in psd:
            if layer.is_group():
                rename_layer(layer, '')

        # レイヤー情報を収集
        util.write_text(
            info_file,
            json.dumps(
                {
                    'name': 'Root',
                    'x': psd.size[0],
                    'y': psd.size[1],
                    'exr_file': str(output_exr_file).replace('\\', '/'),
                    'data': self.get_layer_info(psd),
                },
                indent=2,
                ensure_ascii=False,
            ),
        )
        self.add2log('Save JSON: %s' % str(info_file).replace('\\', '/'))

        # グループレイヤーを解除
        for layer in reversed(list(psd.descendants())):
            if layer.is_group():
                continue
            layer.move_to_group(psd)

        # グループレイヤーを削除
        for layer in reversed(list(psd.descendants())):
            if layer.is_group():
                layer.delete_layer()

        # rev
        for layer in reversed(list(psd.descendants())):
            layer.move_to_group(psd)

        # レイヤーデータを収集
        parts_data = []

        for layer in psd:
            if not layer.is_group():
                # レイヤーのバウンディングボックスを取得
                bbox = layer.bbox
                layer_width = bbox[2] - bbox[0]
                layer_height = bbox[3] - bbox[1]

                if layer_width == 0 or layer_height == 0:
                    continue  # サイズが0の場合はスキップ

                # レイヤー名を取得
                layer_name = layer.name.replace(" ", "_").replace("/", "_")  # 不正文字対策

                # 各チャンネルのデータを取得
                red = np.array(layer.topil(ChannelID.CHANNEL_0)) / 255.0
                green = np.array(layer.topil(ChannelID.CHANNEL_1)) / 255.0
                blue = np.array(layer.topil(ChannelID.CHANNEL_2)) / 255.0
                alpha = np.array(layer.topil(ChannelID.TRANSPARENCY_MASK)) / 255.0

                # チャンネルデータを準備
                channels = {
                    'R': (red * alpha).astype(np.float16),
                    'G': (green * alpha).astype(np.float16),
                    'B': (blue * alpha).astype(np.float16),
                    'A': alpha.astype(np.float16),
                }

                # header
                header = {
                    'name': layer_name,
                    # 'compression': OpenEXR.RLE_COMPRESSION,
                    # 'type': OpenEXR.scanlineimage,
                    'dataWindow': (
                        np.array([bbox[0], bbox[1]], dtype=np.int32),
                        np.array([bbox[2] - 1, bbox[3] - 1], dtype=np.int32)
                    ),
                    'displayWindow': (
                        np.array([0, 0], dtype=np.int32),
                        np.array([canvas_width - 1, canvas_height - 1], dtype=np.int32)
                    ),
                }
                # part
                part = OpenEXR.Part(header, channels)

                # パート情報を保存
                parts_data.append(part)

        if not parts_data:
            self.add2log(
                '[ERROR]No valid layers found in the PSD file.',
                log.ERROR_COLOR
            )
            return
        f = OpenEXR.File(parts_data)
        f.write(str(output_exr_file))

        self.add2log('Save EXR: %s' % str(output_exr_file).replace('\\', '/'))
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
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

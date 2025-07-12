from functools import partial

import dataclasses
import sys
from pathlib import Path

import OpenEXR
import numpy as np
import pykakasi
from PySide6.QtCore import (
    Qt, QSize,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QHeaderView,
)

from PySide6.QtGui import (
    QColor,
    QStandardItemModel, QStandardItem, QPixmap, QIcon,
)
from psd_tools import PSDImage
from PIL import Image
from PIL.ImageQt import ImageQt
from psd_tools.constants import ChannelID

from rs.core import (
    config,
    util,
    pipe as p,
)
from rs.gui import (
    appearance,
    log,
)

from rs_fusion.core import (
    operator as op,
)

from rs_fusion.tool.psd2tatie.importer import Importer
from rs_fusion.tool.psd2tatie.macro_builder import MacroBuilder
from rs_fusion.tool.psd2tatie.psd2tatie_ui import Ui_MainWindow

APP_NAME = 'Psd to 立ち絵'

AIUEO_TEMPLATE_PATH = config.DATA_PATH.joinpath('app', 'Psd2Tatie', 'AIUEO_Template.setting')

ICON_SIZE = 48
EYE_COLOR = QColor(0, 114, 184)
MOUTH_COLOR = QColor(0, 121, 30)
REMOVE_COLOR = QColor(104, 104, 104)
FRONTMOST_COLOR = QColor(159, 125, 0)


@dataclasses.dataclass
class ConfigData(config.Data):
    psd_path: str = ''
    dst_path: str = ''
    eye_close: str = ''
    mouth_a: str = ''
    mouth_i: str = ''
    mouth_u: str = ''
    mouth_e: str = ''
    mouth_o: str = ''
    mouth_n: str = ''
    eye_list: list[str] = dataclasses.field(default_factory=list)
    mouth_list: list[str] = dataclasses.field(default_factory=list)
    remove_list: list[str] = dataclasses.field(default_factory=list)
    front_list: list[str] = dataclasses.field(default_factory=list)


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

    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(750, 1000)

        self.fusion = fusion

        self.psd = None
        self.canvas_width = 0
        self.canvas_height = 0
        self.info_data = None
        self.layer_list = []

        # tree
        self.tree = self.ui.treeView
        self.tree.setHeaderHidden(True)
        self.tree.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.tree.setEditTriggers(QHeaderView.NoEditTriggers)
        self.tree.setSelectionMode(self.tree.SelectionMode.ExtendedSelection)
        self.tree.setSelectionBehavior(self.tree.SelectionBehavior.SelectRows)
        self.tree.setRootIsDecorated(False)
        self.tree.setUniformRowHeights(True)
        self.model = QStandardItemModel()
        self.tree.setModel(self.model)
        self.selection_model = self.tree.selectionModel()

        header = self.tree.header()
        header.setSectionResizeMode(1, header.ResizeMode.Stretch)

        # button
        self.ui.convertButton.setStyleSheet(appearance.other_stylesheet)

        # event
        self.ui.psdLineEdit.textChanged.connect(self.load_psd)

        self.ui.psdToolButton.clicked.connect(self.psdToolButton_clicked)
        self.ui.dstToolButton.clicked.connect(self.dstToolButton_clicked)

        self.ui.convertButton.clicked.connect(self.conv)
        self.ui.closeButton.clicked.connect(self.close)

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionExit.triggered.connect(self.close)

        self.ui.setEyetButton.clicked.connect(self.set_eye)
        self.ui.setMouthButton.clicked.connect(self.set_mouth)
        self.ui.setFrontmostButton.clicked.connect(self.set_frontmost)
        self.ui.setRemoveButton.clicked.connect(self.set_remove)
        self.ui.clearButton.clicked.connect(self.clear_status)

        self.ui.setCloseToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.closeComboBox)
        )
        self.ui.setAToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.aComboBox)
        )
        self.ui.setIToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.iComboBox)
        )
        self.ui.setUToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.uComboBox)
        )
        self.ui.setEToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.eComboBox)
        )
        self.ui.setOToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.oComboBox)
        )
        self.ui.setNToolButton.clicked.connect(
            partial(self.set_combo_box_current_text, self.ui.nComboBox)
        )

        self.ui.actionPSD.triggered.connect(self.open_psd_dir)
        self.ui.actionGenerators_Dir_User.triggered.connect(partial(
            self.open_dir,
            config.RESOLVE_USER_PATH.joinpath('Templates', 'Edit', 'Generators'),
        ))

    def make_tree_data(self, layer_list: list[str]) -> dict:
        dct = {}
        for layer in layer_list:
            ss = layer.split('.')
            pre_dct = dct
            for i, name in enumerate(ss):
                # image layer
                if i == len(ss) - 1:
                    if layer not in pre_dct:
                        pre_dct[layer] = {}
                    continue
                # group layer
                if name not in pre_dct:
                    pre_dct[name] = {}
                if 'data' not in pre_dct[name]:
                    pre_dct[name]['data'] = {}
                pre_dct = pre_dct[name]['data']

        def set_attrs(_dct: dict, info_data: dict) -> None:
            for k, v in _dct.items():
                _info_data = info_data.get(k, {})
                if isinstance(v, dict):
                    v['name_en'] = _info_data.get('name_en', k)
                    v['visible'] = _info_data.get('visible', True)
                    if 'data' in v:
                        set_attrs(v['data'], _info_data.get('data', {}))

        set_attrs(dct, self.info_data)
        return dct

    def save_thumbnail(self, config_data: ConfigData):
        self.add2log('Making thumbnail...')
        # 104x58のサムネイルを保存
        # 下をクロップ
        ref_height = self.canvas_width * 58 // 104
        ref_width = self.canvas_height * 104 // 58
        if self.canvas_height > ref_height:
            viewport = (0, 0, self.canvas_width, ref_height)
        else:
            viewport = (0, 0, ref_width, self.canvas_height)

        self.add2log('Compositing PSD image...')
        base_img = self.psd.composite(viewport=viewport, color=(0.5, 0.5, 0.5))
        if base_img is None:
            self.add2log('[ERROR] Failed to composite PSD image', log.ERROR_COLOR)
            return

        # サイズを変更
        self.add2log('Resizing thumbnail image...')
        thumbnail_img = base_img.resize((104, 58))
        if thumbnail_img is None:
            self.add2log('[ERROR] Failed to resize thumbnail image', log.ERROR_COLOR)
        # 保存先のパスを決定
        psd_path = Path(config_data.psd_path)
        thumbnail_path = psd_path.with_suffix('.png')
        # サムネイルを保存
        thumbnail_img.save(thumbnail_path, format='PNG', compress_level=6)
        self.add2log('Thumbnail saved: %s' % str(thumbnail_path).replace('\\', '/'))

    def save_png(self, output_dir: Path, config_data: ConfigData) -> dict:

        # レイヤーデータを収集
        parts_data = {}

        for layer in self.psd:
            if layer.is_group():
                continue
            if layer.name in config_data.remove_list:
                continue

            if layer.size[0] == 0 or layer.size[1] == 0:
                parts_data[layer.name] = {
                    'path': None,
                    'size': layer.size,
                    'bbox': layer.bbox,
                    'offset': layer.offset,
                }
                continue

            # pil image
            img = Image.new("RGBA", layer.size, (0, 0, 0, 0))
            layer_img = layer.topil()
            if layer_img is not None:
                # img.paste(layer_img, (0, 0), mask=layer_img)
                img.paste(layer_img, (0, 0))

            # filename
            name: str = layer.name.strip().translate(str.maketrans('*\\/:?"<>|', '-________', ''))
            if name == '':
                name = '_none_'
            if name[-1].isdigit():
                name += '_'
            png_path = output_dir.joinpath(f'{name}.png')
            for i in range(1, 100):
                if png_path.is_file():
                    png_path = output_dir.joinpath(f'{name}_{i}_.png')
                else:
                    break

            # save image
            # todo:compress_levelを変更してパフォーマンスをチェック
            # compress_levelは0-9で、0が圧縮なし、9が最大圧縮
            # defaultは6
            # えーーなんでオプション付けると色変わるの？オプションはpathのみなら正しいっぽい
            # img.save(png_path, format='PNG', compress_level=6)
            img.save(png_path)
            self.add2log('Save PNG: ' + str(png_path).replace("\\", "/"))

            #
            parts_data[layer.name] = {
                'path': str(png_path).replace('\\', '/'),
                'size': layer.size,
                'bbox': layer.bbox,
                'offset': layer.offset,
            }

        return parts_data

    def save_exr(self, exr_path: Path, config_data: ConfigData) -> None:
        # レイヤーデータを収集
        parts_data = []

        for layer in self.psd:
            if layer.is_group():
                continue
            if layer.name in config_data.remove_list:
                continue
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
                'dataWindow': (
                    np.array([bbox[0], bbox[1]], dtype=np.int32),
                    np.array([bbox[2] - 1, bbox[3] - 1], dtype=np.int32)
                ),
                'displayWindow': (
                    np.array([0, 0], dtype=np.int32),
                    np.array([self.canvas_width - 1, self.canvas_height - 1], dtype=np.int32)
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
        f.write(str(exr_path))

        self.add2log('Save EXR: %s' % str(exr_path).replace('\\', '/'))

    def conv(self):
        self.ui.logTextEdit.clear()
        self.add2log('Convert PSD to 立ち絵')
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            self.add2log('[ERROR] Not in Fusion page', log.ERROR_COLOR)
            return

        comp = self.fusion.CurrentComp
        if comp is None:
            self.add2log('[ERROR] No current composition', log.ERROR_COLOR)
            return

        tools = list(comp.GetToolList().values())
        if len(tools) > 0:
            self.add2log('[ERROR] Please delete all tools in the current composition', log.ERROR_COLOR)
            return

        data = self.get_data()
        if data.psd_path == '':
            self.add2log('[ERROR] Please select PSD file', log.ERROR_COLOR)
            return
        psd_path = Path(data.psd_path)
        if not psd_path.is_file():
            self.add2log(f'[ERROR] PSD file does not exist:\n{psd_path}', log.ERROR_COLOR)
            return
        if data.dst_path == '':
            self.add2log('[ERROR] Please select output directory', log.ERROR_COLOR)
            return
        dst_path = Path(data.dst_path)
        if not dst_path.is_dir():
            self.add2log(f'[ERROR] Output directory does not exist:\n{dst_path}', log.ERROR_COLOR)
            return

        if data.eye_close == '':
            self.add2log('[ERROR] Please select eye close layer', log.ERROR_COLOR)
            return
        if data.mouth_a == '':
            self.add2log('[ERROR] Please select mouth A layer', log.ERROR_COLOR)
            return
        if data.mouth_i == '':
            self.add2log('[ERROR] Please select mouth I layer', log.ERROR_COLOR)
            return
        if data.mouth_u == '':
            self.add2log('[ERROR] Please select mouth U layer', log.ERROR_COLOR)
            return
        if data.mouth_e == '':
            self.add2log('[ERROR] Please select mouth E layer', log.ERROR_COLOR)
            return
        if data.mouth_o == '':
            self.add2log('[ERROR] Please select mouth O layer', log.ERROR_COLOR)
            return
        if data.mouth_n == '':
            self.add2log('[ERROR] Please select mouth N layer', log.ERROR_COLOR)
            return

        # save thumbnail
        self.save_thumbnail(data)

        # OpenEXR
        # exr_path = psd_path.with_suffix('.exr')
        # self.save_exr(exr_path, config_data=data)
        # if not exr_path.is_file():
        #     self.add2log(f'[ERROR] Failed to save EXR file:\n{exr_path}', log.ERROR_COLOR)
        #     return

        # png export
        out_dir = dst_path.joinpath(psd_path.stem)
        if not out_dir.is_dir():
            out_dir.mkdir(parents=True, exist_ok=True)
        parts_data = self.save_png(out_dir, config_data=data)

        # tree data
        other_list = []
        eye_list = []
        mouth_list = []
        front_list = []
        for layer in reversed(self.layer_list):
            if layer in data.eye_list:
                eye_list.append(layer)
                continue
            if layer in data.mouth_list:
                mouth_list.append(layer)
                continue
            if layer in data.front_list:
                front_list.append(layer)
                continue
            if layer in data.remove_list:
                continue
            other_list.append(layer)
        other_tree_data = self.make_tree_data(other_list)
        eye_tree_data = self.make_tree_data(eye_list)
        mouth_tree_data = self.make_tree_data(mouth_list)
        front_tree_data = self.make_tree_data(front_list)

        # main
        flow = comp.CurrentFrame.FlowView
        comp.Lock()
        comp.StartUndo('RS Builder')

        # load template
        self.add2log('Load Template...')
        dummy_tool = comp.AddTool('Background', 0, 20)  # 位置決め用
        flow.Select(dummy_tool)
        aiueo_template = bmd.readfile(str(AIUEO_TEMPLATE_PATH))
        comp.Paste(aiueo_template)
        dummy_tool.Delete()
        self.add2log('Template loaded')

        # node
        root_xf = comp.FindTool('Root')

        # import
        self.add2log('Importing layers...')
        importer = Importer(
            comp,
            root_xf=root_xf,
            other_data=other_tree_data,
            eye_data=eye_tree_data,
            mouth_data=mouth_tree_data,
            front_data=front_tree_data,
            close_layer=data.eye_close,
            a_layer=data.mouth_a,
            i_layer=data.mouth_i,
            u_layer=data.mouth_u,
            e_layer=data.mouth_e,
            o_layer=data.mouth_o,
            n_layer=data.mouth_n,
            parts_data=parts_data,
            canvas_width=self.canvas_width,
            canvas_height=self.canvas_height,
        )
        importer.make()
        self.add2log('Import completed')

        # macro
        self.add2log('Saving macro...')
        macro_path = psd_path.with_suffix('.setting')
        macro_builder = MacroBuilder(comp)
        macro_builder.build('Template', macro_path)
        self.add2log(f'Macro saved: {macro_path}')

        # end
        comp.EndUndo(True)
        comp.Unlock()
        self.add2log('Done!')

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def psdToolButton_clicked(self) -> None:
        w = self.ui.psdLineEdit
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

    def set_combo_box_current_text(self, w):
        indexes = self.selection_model.selectedRows()
        if len(indexes) == 0:
            return
        row = indexes[0].row()
        index = self.model.index(row, 1)
        item = self.model.itemFromIndex(index)
        if item is not None:
            w.setCurrentText(item.text())

    def set_layer_status(self, status: str, color):
        indexes = self.selection_model.selectedRows()
        for index in indexes:
            item = self.model.itemFromIndex(index)
            if item is not None:
                item.setText(status)
                item.setBackground(color)

    def set_frontmost(self):
        self.set_layer_status('F', FRONTMOST_COLOR)

    def set_eye(self):
        self.set_layer_status('E', EYE_COLOR)

    def set_mouth(self):
        self.set_layer_status('M', MOUTH_COLOR)

    def set_remove(self):
        self.set_layer_status('R', REMOVE_COLOR)

    def clear_status(self):
        self.set_layer_status('', appearance.palette.base().color())

    def set_data(self, c: ConfigData):
        self.ui.psdLineEdit.setText(c.psd_path)
        self.ui.dstLineEdit.setText(c.dst_path)
        self.ui.closeComboBox.setCurrentText(c.eye_close)
        self.ui.aComboBox.setCurrentText(c.mouth_a)
        self.ui.iComboBox.setCurrentText(c.mouth_i)
        self.ui.uComboBox.setCurrentText(c.mouth_u)
        self.ui.eComboBox.setCurrentText(c.mouth_e)
        self.ui.oComboBox.setCurrentText(c.mouth_o)
        self.ui.nComboBox.setCurrentText(c.mouth_n)
        for i in range(0, self.model.rowCount()):
            s_item = self.model.item(i, 0)
            if s_item is None:
                continue
            item = self.model.item(i, 1)
            if item is None:
                continue
            if item.text() in c.eye_list:
                s_item.setText('E')
                s_item.setBackground(EYE_COLOR)
            elif item.text() in c.mouth_list:
                s_item.setText('M')
                s_item.setBackground(QColor(MOUTH_COLOR))
            elif item.text() in c.remove_list:
                s_item.setText('R')
                s_item.setBackground(REMOVE_COLOR)
            elif item.text() in c.front_list:
                s_item.setText('F')
                s_item.setBackground(FRONTMOST_COLOR)

        return c

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.psd_path = self.ui.psdLineEdit.text().strip().replace('\\', '/')
        c.dst_path = self.ui.dstLineEdit.text().strip().replace('\\', '/')
        c.eye_close = self.ui.closeComboBox.currentText()
        c.mouth_a = self.ui.aComboBox.currentText()
        c.mouth_i = self.ui.iComboBox.currentText()
        c.mouth_u = self.ui.uComboBox.currentText()
        c.mouth_e = self.ui.eComboBox.currentText()
        c.mouth_o = self.ui.oComboBox.currentText()
        c.mouth_n = self.ui.nComboBox.currentText()
        c.eye_list = []
        c.mouth_list = []
        c.remove_list = []
        c.front_list = []
        for i in range(0, self.model.rowCount()):
            s_item = self.model.item(i, 0)
            if s_item is None:
                continue
            item = self.model.item(i, 1)
            if item is None:
                continue
            if s_item.text() == 'E':
                c.eye_list.append(item.text())
            elif s_item.text() == 'M':
                c.mouth_list.append(item.text())
            elif s_item.text() == 'R':
                c.remove_list.append(item.text())
            elif s_item.text() == 'F':
                c.front_list.append(item.text())
        return c

    def open(self) -> None:
        dir_path = Path(self.ui.psdLineEdit.text().strip()).parent
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open File',
            str(dir_path),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            if not file_path.is_file():
                return
            c = self.get_data()
            c.load(file_path)
            if c.psd_path != '':
                psd_path = Path(c.psd_path)
                if not psd_path.is_file():
                    r = QMessageBox.question(
                        self,
                        'Warning:  %s' % str(psd_path),
                        f'Warning:  {str(psd_path)} is not found\n\nSelect it?',
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if r == QMessageBox.StandardButton.Yes:
                        psd_path, _ = QFileDialog.getOpenFileName(
                            self,
                            'Select PSD File',
                            str(psd_path.parent),
                            'PSD File (*.psd)',
                        )
                        if psd_path != '':
                            c.psd_path = psd_path
                        else:
                            return
                    else:
                        self.add2log(f'[ERROR] PSD file does not exist:\n{psd_path}', log.ERROR_COLOR)
                        return

            self.set_data(c)

    def save(self) -> None:
        dir_path = Path(self.ui.psdLineEdit.text().strip()).parent
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

    def clear(self):
        self.psd = None
        self.info_data = None
        self.canvas_width = 0
        self.canvas_height = 0
        self.model.clear()
        self.layer_list.clear()
        ws = [
            self.ui.closeComboBox,
            self.ui.aComboBox,
            self.ui.iComboBox,
            self.ui.uComboBox,
            self.ui.eComboBox,
            self.ui.oComboBox,
            self.ui.nComboBox,
        ]
        for w in ws:
            w.clear()

    def set_combobox(self) -> None:
        lst = [''] + self.layer_list
        ws = [
            self.ui.closeComboBox,
            self.ui.aComboBox,
            self.ui.iComboBox,
            self.ui.uComboBox,
            self.ui.eComboBox,
            self.ui.oComboBox,
            self.ui.nComboBox,
        ]
        for w in ws:
            w.clear()
            w.addItems(lst)

    def set_layer_data(self, psd):
        # layer list
        for layer in reversed(list(psd.descendants())):
            if layer.is_group():
                continue
            self.layer_list.append(layer.name)

        # ui
        for layer in reversed(list(psd.descendants())):
            if layer.is_group():
                continue
            s_item = QStandardItem('')
            item = QStandardItem(layer.name)
            # サムネイルを設定
            img = layer.topil()
            if img is not None:
                length = max(img.size)
                scale = ICON_SIZE / length
                layer_img = img.resize((int(img.width * scale), int(img.height * scale)))
                img = Image.new("RGB", (ICON_SIZE, ICON_SIZE), (128, 128, 128))
                img.paste(
                    layer_img,
                    ((ICON_SIZE - layer_img.width) // 2, (ICON_SIZE - layer_img.height) // 2),
                    mask=layer_img,
                )
                img_qt = ImageQt(img)
                pixmap = QPixmap(img_qt)
                item.setIcon(QIcon(pixmap))
            #
            self.model.appendRow([s_item, item])
        self.tree.setColumnWidth(0, ICON_SIZE)

    def get_layer_info(self, group):
        kakasi = pykakasi.kakasi()
        kakasi.setMode('H', 'a')
        kakasi.setMode('K', 'a')
        kakasi.setMode('J', 'a')
        conversion = kakasi.getConverter()
        dct = {}
        for layer in group:
            layer_name: str = layer.name
            ss: list[str] = layer_name.split('.')
            layer_name_en = ''.join(filter(str.isalnum, conversion.do(ss[-1])))
            if len(layer_name_en) == 0:
                layer_name_en = ''.join(filter(lambda s: s not in '!@#$%^&*()-=+\\|`~[]{};\':",./<>?', ss[-1]))
            if len(layer_name_en) == 0:
                layer_name_en = 'none'
            _dct = {
                'name_en': layer_name_en,
                'visible': layer.is_visible(),
            }
            if layer.is_group():
                _dct['data'] = self.get_layer_info(layer)
            dct[layer_name] = _dct
        return dct

    def load_psd(self):
        self.ui.logTextEdit.clear()
        psd_path = Path(self.ui.psdLineEdit.text().strip())
        if self.psd is not None:
            self.clear()

        if not psd_path.is_file():
            return

        # PSDファイルを読み込む
        self.add2log(f'Loading PSD file: {psd_path}')
        psd = PSDImage.open(str(psd_path))

        # キャンバスの解像度を取得
        self.canvas_width, self.canvas_height = psd.size

        # 色深度
        color_depth = psd.depth
        if color_depth not in [8, ]:
            self.add2log(
                f"[ERROR] Unsupported color depth: {color_depth}. Only 8 bits are supported.",
                log.ERROR_COLOR,
            )
            return

        # ."を全角に変換
        for layer in psd.descendants():
            layer.name = layer.name.strip().replace('.', '．').replace('"', '”')

        # rename layers
        for layer in psd:
            if layer.is_group():
                rename_layer(layer, '')

        # レイヤー情報を収集
        self.info_data = self.get_layer_info(psd)

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

        self.set_layer_data(psd)
        self.set_combobox()
        self.psd = psd
        self.add2log(f'PSD loaded: {psd_path}')

    def open_psd_dir(self):
        psd_path = Path(self.ui.psdLineEdit.text().strip())
        if not psd_path.is_file():
            self.add2log('[ERROR] PSD file does not exist:\n%s' % psd_path, log.ERROR_COLOR)
            return
        self.open_dir(psd_path.parent)

    def open_dir(self, d):
        if not d.is_dir():
            r = QMessageBox.warning(
                self,
                f'Warning:  {str(d)}', f'Directory does not exist:\n{str(d)}\n\nCreate it?',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if r == QMessageBox.StandardButton.Yes:
                d.mkdir(parents=True, exist_ok=True)
            else:
                return
        util.open_directory(d)

    def closeEvent(self, event):
        super().closeEvent(event)


def run(fusion) -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow(fusion=fusion)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    pass

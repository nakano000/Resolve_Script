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
    QButtonGroup,
    QFileDialog, QHeaderView,
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
    pose,
)
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


class Importer:
    def __init__(
            self,
            comp,
            root_xf,
            other_data: dict,
            eye_data: dict,
            mouth_data: dict,
            front_data: dict,
            close_layer: str,
            a_layer: str,
            i_layer: str,
            u_layer: str,
            e_layer: str,
            o_layer: str,
            n_layer: str,
            exr_path: Path,
    ):
        self.comp = comp
        self.flow = comp.CurrentFrame.FlowView
        self.root_xf = root_xf

        self.other_data = other_data
        self.eye_data = eye_data
        self.mouth_data = mouth_data
        self.front_data = front_data
        self.exr_path = exr_path

        self.close_layer = close_layer
        self.close_node = None
        self.a_layer = a_layer
        self.a_node = None
        self.i_layer = i_layer
        self.i_node = None
        self.u_layer = u_layer
        self.u_node = None
        self.e_layer = e_layer
        self.e_node = None
        self.o_layer = o_layer
        self.o_node = None
        self.n_layer = n_layer
        self.n_node = None

        self.size_x = 0
        self.size_y = 0

        self.X_OFFSET = 1
        self.Y_OFFSET = 4

        self.btn_size: float = 0.25

        self.exr_node = None
        self.blank_node = None

        self.layer_list: list[str] = []
        self.tree_data = None
        self.json_data = None

    def set_pos(self, node, pos_x, pos_y):
        _x, _y = self.flow.GetPosTable(node).values()
        x = _x if pos_x is None else pos_x * self.X_OFFSET
        y = _y if pos_y is None else pos_y * self.Y_OFFSET
        self.flow.SetPos(node, x, y)

    def set_x(self, node, x):
        self.set_pos(node, x, None)

    def set_y(self, node, y):
        self.set_pos(node, None, y)

    @staticmethod
    def set_orange(node):
        node.TileColor = {
            '__flags': 256,
            'R': 0.92156862745098,
            'G': 0.431372549019608,
            'B': 0,
        }

    @staticmethod
    def uc_button(mg, node, page, layer_name, width):
        if node is None:
            lua = [
                'local mg = comp:FindTool("%s")' % mg.Name,
                'mg.Foreground = nil',
            ]
        else:
            lua = [
                'local mg = comp:FindTool("%s")' % mg.Name,
                'local node = comp:FindTool("%s")' % node.Name,
                'mg:ConnectInput("Foreground", node)',
                'mg.Center:HideViewControls()',
                'mg.Angle:HideViewControls()',
                'mg.Size:HideViewControls()',
            ]
        return {
            'LINKS_Name': layer_name,
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'ButtonControl',
            'INP_Integer': False,
            'BTNCS_Execute': '\n'.join(lua),
            'INP_External': False,
            'ICS_ControlPage': page,
            'ICD_Width': width,
        }

    def setup_base_node(self):
        pos_x = 0
        pos_y = 0
        # exr
        exr_x = pos_x - 1
        exr = self.add_tool('Loader', exr_x, pos_y)
        exr.Clip[1] = self.comp.ReverseMapPath(str(self.exr_path).replace('/', '\\'))
        exr.Loop[1] = 1
        exr.GlobalIn = -1000
        exr.GlobalOut = -1000

        # node
        self.exr_node = exr

        # layer
        outp = exr.FindMainOutput(1)
        lst = list(outp.GetLayerList().values())
        if '' in lst:
            lst.remove('')
        self.layer_list = lst

        # get image size
        img = outp.GetValue()
        self.size_x = img.Width
        self.size_y = img.Height

        # bg
        bg_x = pos_x - 2
        bg_y = pos_y - 1
        bg = self.add_tool('Background', bg_x, bg_y)
        bg.UseFrameFormatSettings = 0
        bg.Width = self.size_x
        bg.Height = self.size_y
        bg.TopLeftAlpha = 0
        bg.Depth = 3  # 16bit floating point

        # set domain
        node_x = pos_x - 2
        node = self.add_tool('SetDomain', node_x, pos_y)
        node.Mode = 'Set'
        node.Left = 0
        node.Bottom = 0
        node.Right = 0
        node.Top = 0
        node.ConnectInput('Input', bg)

        # node
        self.blank_node = node

    def add_tool(self, tool_name, pos_x, pos_y):
        node = self.comp.AddTool(tool_name, pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        return node

    def add_blank(self, pos_x, pos_y):
        node = self.add_tool('Fuse.Wireless', pos_x, pos_y)
        node.ConnectInput('Input', self.blank_node)
        return node

    def add_layer(self, pos_x, pos_y, layer_name):
        node = self.add_tool('Fuse.Wireless', pos_x, pos_y)
        ss = layer_name.split('.')
        node.SetAttrs({'TOOLS_Name': ss[-1]})
        node.ConnectInput('Input', self.exr_node)
        node.Input_LayerSelect = layer_name

        if layer_name == self.close_layer:
            self.close_node = node
        elif layer_name == self.a_layer:
            self.a_node = node
        elif layer_name == self.i_layer:
            self.i_node = node
        elif layer_name == self.u_layer:
            self.u_node = node
        elif layer_name == self.e_layer:
            self.e_node = node
        elif layer_name == self.o_layer:
            self.o_node = node
        elif layer_name == self.n_layer:
            self.n_node = node
        return node

    def add_node(self, pos_x, pos_y, data, name, uc):
        pos_x += 1
        xf = self.add_tool('Transform', pos_x, pos_y)
        xf.SetAttrs({'TOOLS_Name': name})
        wire = self.add_blank(pos_x, pos_y - 1)
        pos_x += 1

        pos_y -= 2

        # data sort
        a_data = {}
        b_data = {}
        c_data = {}
        for layer_name, layer in data.items():
            _name = layer_name.split('.')[-1]
            if _name.startswith('*'):
                b_data[layer_name] = layer
            else:
                if len(b_data) == 0:
                    a_data[layer_name] = layer
                else:
                    c_data[layer_name] = layer
        _data = a_data | b_data | c_data

        # main
        pre_node = wire
        a_mg = None
        page_name = 'ポーズ'
        name_list = []
        user_controls = {}
        user_controls2 = {}
        uc_list = []
        for i, (layer_name, layer) in enumerate(_data.items()):
            layer_name_en: str = layer['name_en']
            visible: bool = layer['visible']
            uc_name = 'N' + str(i).zfill(3) + '_' + layer_name_en

            # add loader
            if 'data' in layer:
                node, pos_x, _uc, _name_list = self.add_node(
                    pos_x, pos_y - 1, layer['data'], layer_name, {},
                )
                uc_list.append(_uc)
                name_list += _name_list
            else:
                node = self.add_layer(pos_x, pos_y, layer_name)

            # mg
            _name = layer_name.split('.')[-1]
            if _name.startswith('*'):
                if a_mg is None:
                    a_mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y + 1) * self.Y_OFFSET)
                    a_mg.SetAttrs({'TOOLS_Name': xf.Name + '_MG'})
                    a_mg.ConnectInput('Background', pre_node)
                    name_list.append(a_mg.Name)
                else:
                    self.set_x(a_mg, pos_x)
                if visible or a_mg.Foreground.GetConnectedOutput() is None:
                    a_mg.ConnectInput('Foreground', node)
                pre_node = a_mg
                if not _name.startswith('!'):
                    user_controls[uc_name + str(pos_x)] = self.uc_button(
                        a_mg, node, page_name, _name, self.btn_size
                    )
            else:
                mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y + 1) * self.Y_OFFSET)
                mg.SetAttrs({'TOOLS_Name': _name + '_MG'})
                name_list.append(mg.Name)
                mg.ConnectInput('Background', pre_node)
                if visible or _name.startswith('!'):
                    mg.ConnectInput('Foreground', node)
                pre_node = mg
                if not _name.startswith('!'):
                    user_controls2[uc_name + '_hide_' + str(pos_x)] = self.uc_button(
                        mg, None, page_name, _name + ' hide', 0.5
                    )
                    user_controls2[uc_name + '_show_' + str(pos_x)] = self.uc_button(
                        mg, node, page_name, _name + ' show', 0.5
                    )
            pos_x += 1

        #
        for k, v in user_controls2.items():
            user_controls[k] = v
        user_controls['Grp_' + xf.Name] = {
            'LINKS_Name': name.replace('!', '').replace('*', ''),
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'LabelControl',
            'LBLC_DropDownButton': True,
            'LBLC_NumInputs': len(user_controls),
            'INP_Default': 1,
            'INP_External': False,
            'INP_Passive': True,
            'ICS_ControlPage': page_name,
        }
        for _uc in uc_list:
            uc.update(_uc)
        uc.update(user_controls)
        pos_x -= 1
        xf.ConnectInput('Input', pre_node)
        self.set_x(xf, pos_x)

        return xf, pos_x, uc, name_list

    def set_mouth_scale(self):
        xf = self.comp.FindTool('MouthScale')
        center_list = []
        for node in [
            self.a_node, self.i_node, self.u_node,
            self.e_node, self.o_node, self.n_node
        ]:
            outp = node.FindMainOutput(1)
            img = outp.GetValue()
            dw = img.DataWindow
            if dw is not None:
                center_x = (dw[1] + dw[3]) / 2
                center_y = (dw[2] + dw[4]) / 2
                center_list.append((center_x, center_y))
        if len(center_list) == 0:
            xf.Pivot = (0.5, 0.5)
        else:
            center_x = sum(x for x, _ in center_list) / len(center_list)
            center_y = sum(y for _, y in center_list) / len(center_list)
            xf.Pivot = (center_x / self.size_x, center_y / self.size_y)

    def make(self):
        self.setup_base_node()
        name_list = []
        uc_dict = {}
        other_xf, pas_x, _uc, _name_list = self.add_node(
            0, 0, self.other_data, 'BaseGrp', {},
        )
        name_list += _name_list
        uc_dict.update(_uc)
        mouth_xf, pas_x, _uc, _name_list = self.add_node(
            pas_x + 1, 0, self.mouth_data, 'MouthGrp', _uc,
        )
        name_list += _name_list
        uc_dict.update(_uc)
        eye_xf, pas_x, _uc, _name_list = self.add_node(
            pas_x + 1, 0, self.eye_data, 'EyeGrp', _uc,
        )
        name_list += _name_list
        uc_dict.update(_uc)
        front_xf, pas_x, _uc, _name_list = self.add_node(
            pas_x + 1, 0, self.front_data, 'FrontGrp', _uc,
        )
        name_list += _name_list
        uc_dict.update(_uc)

        # link
        link_dct = {
            'BASE_LINK': other_xf,
            'MOUSE_LINK': mouth_xf,
            'EYE_LINK': eye_xf,
            'FRONT_LINK': front_xf,
            'Closed': self.close_node,
            'A': self.a_node,
            'I': self.i_node,
            'U': self.u_node,
            'E': self.e_node,
            'O': self.o_node,
            'N': self.n_node,
        }
        for k, v in link_dct.items():
            _node = self.comp.FindTool(k)
            _node.ConnectInput('Input', v)

        # set mouth scale
        self.set_mouth_scale()

        # xf
        # uc = {'__flags': 2097152}  # 順番を保持するフラグ
        uc = pose.get_uc(None)
        for k, v in reversed(list(uc_dict.items())):
            if isinstance(v, dict):
                if 'INPID_InputControl' in v and v['INPID_InputControl'] == 'LabelControl':
                    if 'LBLC_NumInputs' in v and v['LBLC_NumInputs'] == 0:
                        continue
            uc[k] = v

        self.root_xf.UserControls = uc
        self.root_xf = self.root_xf.Refresh()
        self.set_orange(self.root_xf)

        self.root_xf.Comments = '\n'.join(reversed(name_list))


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
        self.resize(750, 900)

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
        psd_path = Path(data.psd_path)
        if not psd_path.is_file():
            self.add2log(f'[ERROR] PSD file does not exist:\n{psd_path}', log.ERROR_COLOR)
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

        # OpenEXR
        exr_path = psd_path.with_suffix('.exr')
        self.save_exr(exr_path, config_data=data)
        if not exr_path.is_file():
            self.add2log(f'[ERROR] Failed to save EXR file:\n{exr_path}', log.ERROR_COLOR)
            return

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
        dummy_tool = comp.AddTool('Background', 0, 20)  # 位置決め用
        flow.Select(dummy_tool)
        aiueo_template = bmd.readfile(str(AIUEO_TEMPLATE_PATH))
        comp.Paste(aiueo_template)
        dummy_tool.Delete()

        # node
        root_xf = comp.FindTool('Root')

        # import
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
            exr_path=exr_path,
        )
        importer.make()

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

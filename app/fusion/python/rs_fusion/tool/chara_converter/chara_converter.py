import pprint

import dataclasses
import json
import os
import shutil
import sys

from collections import OrderedDict
from functools import partial
from pathlib import Path
from typing import List, Optional

from PIL import Image

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

from rs.core import (
    config,
    pipe as p,
)
from rs.gui import (
    appearance,
    log,
)
from rs_fusion.tool.chara_converter.chara_converter_ui import Ui_MainWindow

APP_NAME = 'キャラ素材変換'

OTHER = '他'
HAIR = '髪'
EYEBROW = '眉'
EYE = '目'
MOUTH = '口'
FACE = '顔'
BODY = '体'
ALL = '全'
BACK = '後'
FRONT = '前'

PARTS_LIST = [
    BACK,
    BODY,
    FACE,
    MOUTH,
    EYE,
    EYEBROW,
    HAIR,
    OTHER,
    FRONT,
]

ADD_NULL = [
    BACK,
    OTHER,
    FRONT,
    FACE,
]


def part2en(part: str) -> str:
    dct = {
        BACK: 'BACK',
        BODY: 'BODY',
        FACE: 'FACE',
        MOUTH: 'MOUTH',
        EYE: 'EYE',
        EYEBROW: 'EYEBROW',
        HAIR: 'HAIR',
        OTHER: 'OTHER',
        FRONT: 'FRONT',
    }
    if part not in dct.keys():
        return ''
    return dct[part]


X_OFFSET = 1
Y_OFFSET = 4


def add_node(comp, pos_x, pos_y, size_x, size_y, data, name, p_name, index):
    flow = comp.CurrentFrame.FlowView
    xf = comp.AddTool('Transform', pos_x * X_OFFSET, pos_y * Y_OFFSET)
    xf.SetAttrs({'TOOLS_Name': name})
    pre_node = comp.AddTool('Background', pos_x * X_OFFSET, (pos_y - 1) * Y_OFFSET)
    pre_node.UseFrameFormatSettings = 0
    pre_node.Width = size_x
    pre_node.Height = size_y
    pre_node.TopLeftAlpha = 0
    pre_node.Depth = 1
    pos_x += 1
    pos_y -= 2
    user_controls = {}
    ctrl_name = part2en(name) + '_Slider'
    imp_def = len(data) - 1 if name in ADD_NULL else 0
    user_controls[ctrl_name] = {
        'LINKID_DataType': 'Number',
        'INPID_InputControl': 'SliderControl',
        'LINKS_Name': name,
        'INP_Integer': True,
        'INP_Default': imp_def,
        'INP_MinScale': 0,
        'INP_MaxScale': len(data) - 1,
        'ICS_ControlPage': 'User',
    }
    ctrl_cnt: int = 0
    for key, lst in data.items():
        f: Path = lst[0] if len(lst) - 1 < index else lst[index]
        mg = comp.AddTool('Merge', pos_x * X_OFFSET, (pos_y + 1) * Y_OFFSET)
        node = comp.AddTool('Loader', pos_x * X_OFFSET, pos_y * Y_OFFSET)
        node.Clip[1] = comp.ReverseMapPath(str(f).replace('/', '\\'))
        node.Loop[1] = 1
        node.PostMultiplyByAlpha = 0

        pos_x += 1
        mg.ConnectInput('Foreground', node)
        mg.ConnectInput('Background', pre_node)
        mg.Blend.SetExpression('iif(%s.%s == %d, 1, 0)' % (p_name, ctrl_name, ctrl_cnt))
        ctrl_cnt += 1
        pre_node = mg
    pos_x -= 1
    xf.ConnectInput('Input', pre_node)
    _x, _y = flow.GetPosTable(xf).values()
    flow.SetPos(xf, pos_x, _y)
    return xf, user_controls, pos_x


@dataclasses.dataclass
class ConfigData(config.Data):
    src_dir: str = ''
    dst_dir: str = ''


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
        self.resize(700, 500)

        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # style sheet
        self.ui.importButton.setStyleSheet(appearance.in_stylesheet)

        # event

        self.ui.srcToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.srcLineEdit))
        self.ui.dstToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.dstLineEdit))

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.importButton.clicked.connect(self.import_chara, Qt.QueuedConnection)

    def import_chara(self) -> None:
        self.ui.logTextEdit.clear()
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            self.add2log('[ERROR]Fusion Pageで実行してください。', log.ERROR_COLOR)
            return
        data = self.get_data()

        # src directory check
        src_text = data.src_dir.strip()
        src_dir: Path = Path(src_text)
        if src_dir.is_dir() and src_text != '':
            self.add2log('キャラ素材: %s' % str(src_dir))
        else:
            self.add2log('[ERROR]キャラ素材が存在しません。', log.ERROR_COLOR)
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
        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            self.add2log('[ERROR]コンポジションが見付かりません。', log.ERROR_COLOR)
            return
        flow = comp.CurrentFrame.FlowView

        self.add2log('処理中(前準備)')
        # file_dataにパーツ、プレフィックスで整理する
        src_data = {}
        height = None
        width = None

        for d in p.pipe(
                src_dir.iterdir(),
                p.filter(p.call.is_dir()),
        ):
            part_data = {}
            for f in p.pipe(
                    d.iterdir(),
                    p.filter(p.call.is_file()),
                    p.filter(lambda x: x.name.lower().endswith('.png')),
                    p.map(str),
                    sorted,
                    p.map(Path),
            ):
                f: Path
                if height is None:
                    with Image.open(f) as im:
                        height, width = im.size

                key = f.name.split('.')[0][:2]
                if f.name.startswith(key + 'm') and f.name[len(key) + 1].isdigit():
                    key = f.name[:len(key) + 2]
                if f.name.startswith(key + 'u') and f.name[len(key) + 1].isdigit():
                    key = f.name[:len(key) + 2]
                if f.name[:3].isdigit():
                    key = f.name[:3]
                if key not in part_data:
                    part_data[key] = []
                part_data[key].append(f)
            if len(part_data) > 0:
                src_data[d.name] = part_data
        # コンバート
        dst_data = {}
        for part in src_data:
            self.add2log('処理中(変換,%s)' % part)
            part_data = {}
            for key in src_data[part]:
                key: str
                f0: Path = src_data[part][key][0]
                lst: List[Path] = src_data[part][key]
                # 保存先ディレクトリ
                dir_name = f0.parent.name
                dst_part_dir = dst_dir.joinpath(dir_name)
                dst_part_dir.mkdir(exist_ok=True)
                # 口と目は別処理
                if part in [MOUTH, EYE]:
                    s: str = f0.stem
                    # 特殊な指定は文字残すように
                    suffix: str = ''
                    if s.endswith('-15'):
                        suffix = '-15'
                    if s.endswith('z'):
                        suffix = '+眉'
                    dst_name = key + suffix
                    dst_file_list = []
                    for i, f in enumerate(lst):
                        # コピー先決定
                        dst_file = dst_part_dir.joinpath(
                            # 最後だけ連番を付けない
                            dst_name + '.' + str(i).zfill(2) + '.' + part + '.png'
                        )
                        # copy
                        shutil.copy(f, dst_file)
                        dst_file_list.append(dst_file)
                    part_data[dst_name] = dst_file_list
                # 他の処理
                else:
                    # 名前決め
                    dst_file_name = f0.stem + '.' + part + f0.suffix
                    is_front = False
                    if len(key) == 4 and key[2] == 'm':
                        dst_file_name = key[:2] + '.' + part + key[2:4] + f0.name[4:]
                        # 手前に表示したい
                        dst_part_dir = dst_dir.joinpath(FRONT)
                        dst_part_dir.mkdir(exist_ok=True)
                        is_front = True
                    if len(key) == 4 and key[2] == 'u':
                        dst_file_name = key[:2] + '.' + part + key[2:4] + f0.name[4:]
                    # コピー先決定
                    dst_file = dst_part_dir.joinpath(dst_file_name)
                    # copy
                    shutil.copy(f0, dst_file)
                    if is_front:
                        if FRONT not in dst_data.keys():
                            dst_data[FRONT] = {}
                        dst_data[FRONT][key] = [dst_file]
                    else:
                        part_data[key] = [dst_file]
            if len(part_data) > 0:
                dst_data[part] = part_data
        self.add2log('処理中(変換,透明素材)')
        space_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        space_file = dst_dir.joinpath('透明.png')
        space_image.save(space_file)
        for part in ADD_NULL:
            if part not in dst_data.keys():
                continue
            dst_data[part]['space'] = [space_file]

        # import
        comp.Lock()
        comp.StartUndo('RS Import')
        xf = comp.AddTool('Transform', 0, 0)
        xf.SetAttrs({'TOOLS_Name': 'Root'})
        pre_node = comp.AddTool('Background', 0, - Y_OFFSET)
        pre_node.UseFrameFormatSettings = 0
        pre_node.Width = width
        pre_node.Height = height
        pre_node.TopLeftAlpha = 0
        pre_node.Depth = 1
        pos_x = 1
        pos_y = -2
        user_controls = {}
        max_size = {}
        for part in dst_data.keys():
            max_size[part] = p.pipe(
                dst_data[part].values(),
                p.map(len),
                max,
            )
        # 眉の非表示と口、眉のオフセット
        no_eyebrow_list = []
        offset_list = []
        for i, key in enumerate(dst_data[EYE].keys()):
            if key.endswith('-15'):
                offset_list.append('[%d]=1' % i)
            if key.endswith('+眉'):
                no_eyebrow_list.append('[%d]=1' % i)
        no_eyebrow_exp = ''
        offset_exp = ''
        if len(no_eyebrow_list) > 0:
            no_eyebrow_exp = ':dct = {%s};if dct[%s.EYE_Slider] then return 0 else return 1 end' % (
                ','.join(no_eyebrow_list),
                xf.Name,
            )
        if len(offset_list) > 0:
            offset_exp = ':dct = {%s};' \
                         'if dct[%s.EYE_Slider] then return Point(0.5, 0.5 + (10/%d)) ' \
                         'else return Point(0.5, 0.5) end' % (
                             ','.join(offset_list),
                             xf.Name,
                             height,
                         )
        for part in PARTS_LIST:
            if part not in dst_data.keys():
                continue
            self.add2log('処理中(読み込み,%s)' % part)
            pos_x += 2
            pre_pos_x = pos_x
            node, uc, pos_x = add_node(comp, pos_x, pos_y, width, height, dst_data[part], part, xf.Name, 0)
            if max_size[part] > 1 and part in [EYE, MOUTH]:
                _pre_node = None
                _node = node
                for i in range(1, max_size[part]):
                    dx = comp.AddTool(
                        'Dissolve',
                        (pos_x + 4) * X_OFFSET,
                        (pos_y - 3 * (i - 1)) * Y_OFFSET
                    )
                    if part == MOUTH:
                        dx.Mix.SetExpression(
                            'iif((%s.%s * %d) > %d, 1, 0)' % (xf.Name, 'MouthOpen', max_size[part], i)
                        )
                    if part == EYE:
                        dx.Mix.SetExpression(
                            'iif((%s.%s * %d) > %d, 1, 0)' % (xf.Name, 'EyeClose', max_size[part], i)
                        )
                    if _pre_node is not None:
                        _pre_node.ConnectInput('Foreground', dx)
                    if _node is not None:
                        dx.ConnectInput('Background', _node)
                    _pre_node = dx
                    _node, _, _ = add_node(
                        comp, pre_pos_x, pos_y + (-3 * i), width, height, dst_data[part], part, xf.Name, i
                    )
                    if i == 1:
                        node = dx
                    if i == max_size[part] - 1:
                        dx.ConnectInput('Foreground', _node)
                pos_x += 4
            for key in uc.keys():
                user_controls[key] = uc[key]
            mg = comp.AddTool('Merge', pos_x * X_OFFSET, (pos_y + 1) * Y_OFFSET)
            mg.ConnectInput('Foreground', node)
            mg.ConnectInput('Background', pre_node)
            if part in [FACE]:
                mg.ApplyMode = 'Multiply'
            if part in [EYEBROW] and no_eyebrow_exp != '':
                mg.Blend.SetExpression(no_eyebrow_exp)
            if part in [MOUTH, EYEBROW] and offset_exp != '':
                mg.Center.SetExpression(offset_exp)
            pre_node = mg

        xf.ConnectInput('Input', pre_node)
        _x, _y = flow.GetPosTable(xf).values()
        flow.SetPos(xf, pos_x, _y)
        uc = {'__flags': 2097152}  # 順番を保持するフラグ
        for k, v in reversed(list(user_controls.items())):
            uc[k] = v
        uc['MouthOpen'] = {
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'SliderControl',
            'LINKS_Name': 'MouthOpen',
            # 'INP_Integer': True,
            'INP_Default': 0,
            'INP_MinScale': 0,
            'INP_MaxScale': 1,
            'ICS_ControlPage': 'User',
        }
        uc['EyeClose'] = {
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'SliderControl',
            'LINKS_Name': 'EyeClose',
            # 'INP_Integer': True,
            'INP_Default': 0,
            'INP_MinScale': 0,
            'INP_MaxScale': 1,
            'ICS_ControlPage': 'User',
        }
        xf.UserControls = uc
        xf = xf.Refresh()
        xf.TileColor = {
            '__flags': 256,
            'R': 0.92156862745098,
            'G': 0.431372549019608,
            'B': 0,
        }
        # end
        comp.EndUndo(True)
        comp.Unlock()
        self.add2log('Done!')

    def add2log(self, text: str, color: QColor = log.TEXT_COLOR) -> None:
        self.ui.logTextEdit.log(text, color)

    def toolButton_clicked(self, w) -> None:
        path = QFileDialog.getExistingDirectory(
            self,
            'Select Directory',
            w.text(),
        )
        if path != '':
            w.setText(path)

    def set_data(self, c: ConfigData):
        self.ui.srcLineEdit.setText(c.src_dir)
        self.ui.dstLineEdit.setText(c.dst_dir)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_dir = self.ui.srcLineEdit.text()
        c.dst_dir = self.ui.dstLineEdit.text()

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

    def closeEvent(self, event):
        self.save_config()
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

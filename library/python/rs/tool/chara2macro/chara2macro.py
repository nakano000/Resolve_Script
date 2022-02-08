import dataclasses
import json
import re
import shutil
import subprocess
import sys

from collections import OrderedDict
from functools import partial
from pathlib import Path
from typing import List

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
    resolve,
)
from rs.gui import (
    appearance,
    log,
)
from rs.tool.chara2macro.chara2macro_ui import Ui_MainWindow

TOP = 'top'
BOTTOM = 'bottom'
HAIR = 'hair'
EYEBROW = 'eyebrow'
EYE = 'eye'
MOUTH = 'mouth'
FACE = 'face'
BODY = 'body'

PARTS_DICT = OrderedDict((
    (BODY, '体'),
    (FACE, '顔'),
    (MOUTH, '口'),
    (EYE, '目'),
    (EYEBROW, '眉'),
    (HAIR, '髪'),
    (BOTTOM, '服下'),
    (TOP, '服上'),
))

APP_NAME = 'Chara2MACRO'


@dataclasses.dataclass
class ConfigData(config.Data):
    src_dir: str = ''
    dst_dir: str = ''
    fps: int = 30
    step: int = 1
    idle: int = 90
    x_size: int = 960
    y_size: int = 540
    anim_list: List[str] = dataclasses.field(default_factory=lambda: [EYE, MOUTH])

    def save_template(self, path: Path) -> None:
        dct = dataclasses.asdict(self)
        del dct['src_dir']
        del dct['dst_dir']
        path.write_text(
            json.dumps(dct, indent=2),
            encoding='utf-8',
        )


def file_operation(data: ConfigData, src: Path, dst: Path):
    dst.mkdir(exist_ok=True)
    part = dst.name
    dct = OrderedDict()
    for f in p.pipe(
            src.iterdir(),
            p.filter(p.call.is_file()),
            p.filter(lambda x: len(x.name) > 2 and x.name[:2].isdigit()),
            p.map(str),
            sorted,
            p.map(Path)
    ):
        f: Path
        key = f.name[:2] if part in data.anim_list else f.name.split('.')[0]
        if key not in dct:
            dct[key] = []
        dct[key].append(f)

    for key in dct:
        first_file = dct[key][0]
        ss: List[str] = first_file.name.split('.')
        ss.insert(1, part)
        dst_file: Path = dst.joinpath('.'.join(ss))
        shutil.copy(first_file, dst_file)
        dct[key][0] = dst_file
        size = len(dct[key])
        if size > 1:
            anim01_dir = dst.joinpath('%s.%s.%s' % (key, part, 'anim01'))
            anim02_dir = dst.joinpath('%s.%s.%s' % (key, part, 'anim02'))
            anim01_dir.mkdir(exist_ok=True)
            anim02_dir.mkdir(exist_ok=True)

            cnt: int = 0
            anim_list = list(range(1, size)) + list(reversed(range(1, size - 1)))
            for anim_frame in anim_list:
                f = dct[key][anim_frame]
                for i in range(data.step):
                    anim01_file = anim01_dir.joinpath('%s.%s%s' % (anim01_dir.name, str(cnt).zfill(3), f.suffix))
                    anim02_file = anim02_dir.joinpath('%s.%s%s' % (anim02_dir.name, str(cnt).zfill(3), f.suffix))
                    shutil.copy(f, anim01_file)
                    shutil.copy(f, anim02_file)
                    cnt += 1
            for i in range(data.idle):
                anim02_file = anim02_dir.joinpath(
                    '%s.%s%s' % (anim02_dir.name, str(cnt).zfill(3), dct[key][0].suffix)
                )
                shutil.copy(dct[key][0], anim02_file)
                cnt += 1

            dct[key] = [
                dct[key][0],
                anim01_dir.joinpath('%s.%s%s' % (anim01_dir.name, str(0).zfill(3), dct[key][0].suffix)),
                anim02_dir.joinpath('%s.%s%s' % (anim02_dir.name, str(0).zfill(3), dct[key][0].suffix)),
            ]
    return dct


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.resize(500, 800)
        # checkbox_dict
        self.checkbox_dict = OrderedDict((
            (BODY, self.ui.bodyCheckBox),
            (FACE, self.ui.faceCheckBox),
            (MOUTH, self.ui.mouthCheckBox),
            (EYE, self.ui.eyeCheckBox),
            (EYEBROW, self.ui.eyebrowCheckBox),
            (HAIR, self.ui.hairCheckBox),
            (BOTTOM, self.ui.bottomCheckBox),
            (TOP, self.ui.topCheckBox),
        ))

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        self.template_dir = config.ROOT_PATH.joinpath('data', 'template', APP_NAME)
        # event

        self.ui.srcToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.srcLineEdit))
        self.ui.dstToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.dstLineEdit))

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.exportButton.clicked.connect(self.export)
        self.ui.templateButton.clicked.connect(partial(self.open, is_template=True))

        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_Template.triggered.connect(self.save_template)
        self.ui.actionExit.triggered.connect(self.close)

    def set_data(self, c: ConfigData):
        self.ui.srcLineEdit.setText(c.src_dir)
        self.ui.dstLineEdit.setText(c.dst_dir)

        self.ui.fpsSpinBox.setValue(c.fps)
        self.ui.stepSpinBox.setValue(c.step)
        self.ui.idleSpinBox.setValue(c.idle)
        self.ui.xSpinBox.setValue(c.x_size)
        self.ui.ySpinBox.setValue(c.y_size)

        p.pipe(
            self.checkbox_dict,
            dict.items,
            p.iter(lambda x: x[1].setChecked(x[0] in c.anim_list))
        )

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_dir = self.ui.srcLineEdit.text()
        c.dst_dir = self.ui.dstLineEdit.text()

        c.fps = self.ui.fpsSpinBox.value()
        c.step = self.ui.stepSpinBox.value()
        c.idle = self.ui.idleSpinBox.value()
        c.x_size = self.ui.xSpinBox.value()
        c.y_size = self.ui.ySpinBox.value()

        c.anim_list = p.pipe(
            self.checkbox_dict,
            dict.items,
            p.filter(lambda x: x[1].isChecked()),
            p.map(lambda x: x[0]),
            list,
        )
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

    def save_template(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            'SaveTemplate',
            str(self.template_dir),
            'JSON File (*.json);;All File (*.*)'
        )
        if path != '':
            file_path = Path(path)
            c = self.get_data()
            c.save_template(file_path)

    def closeEvent(self, event):
        self.save_config()
        super().closeEvent(event)

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

    def export(self) -> None:
        self.ui.logTextEdit.clear()

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

        # resolve check
        resolve_app = resolve.get()
        if resolve_app is None:
            self.add2log('[ERROR]Resolveが見つかりません', log.ERROR_COLOR)
            return

        # file
        self.add2log('処理中(copy)')
        parts_file_dct = OrderedDict()
        for key in PARTS_DICT:
            src = src_dir.joinpath(PARTS_DICT[key])
            if src.is_dir():
                self.add2log('処理中(%s)' % PARTS_DICT[key])
                parts_file_dct[key] = file_operation(
                    data,
                    src,
                    dst_dir.joinpath(key),
                )

        self.add2log('')  # new line

        # comp
        name = src_dir.name

        self.add2log('処理中(comp)')
        fusion = resolve_app.Fusion()
        comp = fusion.NewComp()
        comp.Lock()
        # --------------------
        # pref
        comp.SetPrefs({
            "Comp.FrameFormat.Name": name,
            "Comp.FrameFormat.Width": data.x_size,
            "Comp.FrameFormat.Height": data.y_size,
            "Comp.FrameFormat.AspectX": 1.0,
            "Comp.FrameFormat.AspectY": 1.0,
            "Comp.FrameFormat.GuideRatio": float(data.x_size) / float(data.y_size),
            "Comp.FrameFormat.Rate": data.fps,
            "Comp.FrameFormat.DepthInteractive": 2,  # 16 bits Float
            "Comp.FrameFormat.DepthFull": 2,  # 16 bits Float
            "Comp.FrameFormat.DepthPreview": 2  # 16 bits Float
        })
        # node
        ctrl_xf_name = 'Ctrl_Transform'
        bg_base = comp.AddTool('Background', 0, 0)
        bg_base.TopLeftAlpha = 0

        base_node = bg_base

        part_cnt = 0
        for part in parts_file_dct:
            file_dct = parts_file_dct[part]
            ld_list = []
            count = 0
            for k in file_dct:
                lst = file_dct[k]
                x_pos = part_cnt * 5
                y_pos = -3 * (count + 1)
                result = None
                for i in range(len(lst) - 1, -1, -1):
                    ld = comp.AddTool('Loader', x_pos, y_pos - i)
                    ld.Clip[1] = str(lst[i])
                    ld.Loop[1] = 1
                    ld.SetAttrs({'TOOLS_Name': '%s_%s' % (part, k)})
                    if i == len(lst) - 1:
                        result = ld
                    else:
                        dx = comp.AddTool('Dissolve', x_pos + 1, y_pos - i)
                        dx.ConnectInput('Background', ld)
                        dx.ConnectInput('Foreground', result)
                        dx.Mix = 0
                        dx.Mix.SetExpression('%s.%s - %d' % (ctrl_xf_name, part + '_anim', i))
                        result = dx

                ld_list.append(result)
                count += 1

            dx_list = []
            sp_size = 10
            ld10_list = p.pipe(
                range(0, len(ld_list), sp_size),
                p.map(lambda index: ld_list[index: index + sp_size]),
            )
            x_pos = 2 + part_cnt * 5
            if len(ld_list) > 1:
                for i in range(len(ld_list) - 1, 0, -1):
                    y_pos = -3 * i
                    node = ld_list[i]
                    if len(dx_list) > 0:
                        node = dx_list[len(dx_list) - 1]
                    dx = comp.AddTool('Dissolve', x_pos, y_pos)
                    dx.ConnectInput('Background', ld_list[i - 1])
                    dx.ConnectInput('Foreground', node)
                    dx.Mix = 0
                    dx.Mix.SetExpression('%s.%s - %d' % (ctrl_xf_name, part, i - 1))
                    dx_list.append(dx)
            else:
                dx_list.append(ld_list[0])

            mg = comp.AddTool('Merge', x_pos + 1, 0)
            mg.ConnectInput('Background', base_node)
            mg.ConnectInput('Foreground', dx_list[len(dx_list) - 1])
            base_node = mg

            part_cnt += 1

        uc = {}
        for part in PARTS_DICT:
            if part in parts_file_dct:
                file_dct = parts_file_dct[part]
                size = len(file_dct)
                uc[part] = {
                    'LINKS_Name': part,
                    'LINKID_DataType': "Number",
                    'INPID_InputControl': "SliderControl",
                    'INP_Default': 0,
                    'INP_Integer': True,
                    'INP_MinScale': 0,
                    'INP_MaxScale': size - 1,
                    'INP_MinAllowed': 0,
                    'INP_MaxAllowed': size - 1,
                    'ICS_ControlPage': "Controls",
                }
                if part in data.anim_list:
                    uc_name = part + '_anim'
                    uc[uc_name] = {
                        'LINKS_Name': uc_name,
                        'LINKID_DataType': "Number",
                        'INPID_InputControl': "SliderControl",
                        'INP_Default': 0,
                        'INP_Integer': True,
                        'INP_MinScale': 0,
                        'INP_MaxScale': 2,
                        'INP_MinAllowed': 0,
                        'INP_MaxAllowed': 2,
                        'ICS_ControlPage': "Controls",
                    }

        xf = comp.AddTool('Transform', 2 + part_cnt * 5, 0)
        xf.ConnectInput('Input', base_node)
        xf.UserControls = uc
        xf.SetAttrs({'TOOLS_Name': ctrl_xf_name})

        # --------------------
        comp.Unlock()
        comp_file = dst_dir.joinpath('%s.comp' % name)
        comp.Save(str(comp_file))
        comp.Close()
        self.add2log('Save: %s' % str(comp_file))

        self.add2log('')  # new line

        # config file
        self.add2log('設定保存(json file)')
        json_file = dst_dir.joinpath('%s.json' % name)
        data.save(json_file)
        self.add2log('Export: %s' % str(json_file))

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

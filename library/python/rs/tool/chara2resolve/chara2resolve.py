from pprint import pprint

import dataclasses
import shutil
import sys
import json

from collections import OrderedDict
from functools import partial
from pathlib import Path
from typing import List, Optional

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
    chara_sozai as cs,
    pipe as p,
    resolve as reso,
    fusion as fu,
)
from rs.gui import (
    appearance,
    log,
)
from rs.tool.chara2resolve.chara2resolve_ui import Ui_MainWindow

APP_NAME = 'Chara2Resolve'


@dataclasses.dataclass
class ConfigData(config.Data):
    src_dir: str = ''
    dst_dir: str = ''
    fps: int = 30
    step: int = 1
    idle: int = 90
    offset: int = 30

    def save_template(self, path: Path) -> None:
        dct = dataclasses.asdict(self)
        del dct['src_dir']
        del dct['dst_dir']
        path.write_text(
            json.dumps(dct, indent=2),
            encoding='utf-8',
        )


def copy_file(f: Path, dst_dir: Path, part: str) -> Path:
    ss: List[str] = f.name.split('.')
    ss.insert(1, part)
    dst_file: Path = dst_dir.joinpath('.'.join(ss))
    shutil.copy(f, dst_file)
    return dst_file


def copy_anim(lst: List[Path], dst_dir: Path, anim_type: str) -> Optional[Path]:
    if len(lst) < 1:
        return None

    anim_dir_name = '%s.%s' % (anim_type, 'anim')
    anim_dir = dst_dir.joinpath(anim_dir_name)
    anim_dir.mkdir(exist_ok=True)

    anim_file = None
    for i in range(len(lst)):
        f = lst[i]
        dst_anim_file = anim_dir.joinpath('%s.%s%s' % (anim_dir_name, str(i).zfill(3), f.suffix))
        shutil.copy(f, dst_anim_file)
        if i == 0:
            anim_file = dst_anim_file
    return anim_file


def copy_files(data: ConfigData, pattern: str, part: str):
    part_src = Path(data.src_dir).joinpath(cs.PARTS_DICT[part])
    pattern_src = part_src.joinpath(pattern)
    src = pattern_src if pattern_src.is_dir() else part_src

    dst = Path(data.dst_dir).joinpath(pattern, part)
    dst.mkdir(parents=True, exist_ok=True)

    dct = cs.path_to_dict(src)
    if part == cs.BODY:
        for key in p.pipe(
                dct.keys(),
                p.filter(lambda s: s != pattern),
                list,
        ):
            dct.pop(key)
    dst_dct = OrderedDict()
    for key in dct:
        if part == cs.BODY:
            # Body
            dst_dct[key] = [copy_file(dct[key][0], dst, part)]

        elif part not in [cs.MOUTH, cs.EYE]:
            # General
            lst = p.pipe(
                cs.get_key_file(dct[key]),
                p.filter(lambda x: x is not None),
                list,
            )
            dst_dct[key] = []
            for f in lst:
                dst_dct[key].append(copy_file(f, dst, part))
        else:
            # Animated
            base_file, v_file, _ = cs.get_key_file(dct[key], is_anim=True)
            lst = p.pipe(
                [base_file, v_file],
                p.filter(lambda x: x is not None),
                list,
            )
            dst_dct[key] = []
            for f in lst:
                dst_dct[key].append(copy_file(f, dst, part))
            # Anim
            anim_file_list = cs.get_anim_file_list(base_file.name, dct[key])
            anim_list = cs.make_anim(data.step, anim_file_list)
            anim_list02 = cs.make_anim02(data.step, data.idle, data.offset, base_file, anim_file_list)
            v_anim_file_list = [] if v_file is None else cs.get_anim_file_list(v_file.name, dct[key])
            v_anim_list = cs.make_anim(data.step, v_anim_file_list)
            v_anim_list02 = cs.make_anim02(data.step, data.idle, data.offset, v_file, v_anim_file_list)

            anim_file = copy_anim(anim_list, dst, '%s_01.%s' % (key, part))
            if anim_file is not None:
                dst_dct[key].append(anim_file)
            v_anim_file = copy_anim(v_anim_list, dst, '%sv_01.%s' % (key, part))
            if v_anim_file is not None:
                dst_dct[key].append(v_anim_file)
            anim_file02 = copy_anim(anim_list02, dst, '%s_02.%s' % (key, part))
            if anim_file02 is not None:
                dst_dct[key].append(anim_file02)
            v_anim_file02 = copy_anim(v_anim_list02, dst, '%sv_02.%s' % (key, part))
            if v_anim_file02 is not None:
                dst_dct[key].append(v_anim_file02)

    return dst_dct


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
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

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        self.template_dir = config.ROOT_PATH.joinpath('data', 'template', APP_NAME)

        # style sheet
        self.ui.exportButton.setStyleSheet(appearance.ex_stylesheet)
        self.ui.installButton.setStyleSheet(appearance.in_stylesheet)

        # event

        self.ui.srcToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.srcLineEdit))
        self.ui.dstToolButton.clicked.connect(partial(self.toolButton_clicked, self.ui.dstLineEdit))

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.exportButton.clicked.connect(self.export, Qt.QueuedConnection)
        self.ui.installButton.clicked.connect(self.install)
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
        self.ui.offsetSpinBox.setValue(c.offset)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_dir = self.ui.srcLineEdit.text()
        c.dst_dir = self.ui.dstLineEdit.text()

        c.fps = self.ui.fpsSpinBox.value()
        c.step = self.ui.stepSpinBox.value()
        c.idle = self.ui.idleSpinBox.value()
        c.offset = self.ui.offsetSpinBox.value()
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
        resolve = reso.get()
        if resolve is None:
            self.add2log('[ERROR]Resolveが見つかりません', log.ERROR_COLOR)
            return

        # file
        self.add2log('処理中(copy)')
        body_src = src_dir.joinpath(cs.PARTS_DICT[cs.BODY])
        if not body_src.is_dir():
            self.add2log('[ERROR] %sが存在しません。' % cs.PARTS_DICT[cs.BODY], log.ERROR_COLOR)
            return
        pattern_list = p.pipe(
            body_src.iterdir(),
            p.filter(p.call.is_file()),
            p.map(p.get.name),
            p.filter(lambda s: len(s) > 2 and s[:2].isdigit()),
            p.map(lambda s: s.split('.')[0]),
            sorted,
        )

        all_file_dct = OrderedDict()
        for pattern in pattern_list:
            parts_file_dct = OrderedDict()
            for key in cs.PARTS_DICT:
                src = src_dir.joinpath(cs.PARTS_DICT[key])
                if src.is_dir():
                    self.add2log('処理中(copy, %s, %s)' % (pattern, cs.PARTS_DICT[key]))
                    lst = copy_files(
                        data,
                        pattern,
                        key,
                    )
                    if len(lst) > 0:
                        parts_file_dct[key] = lst
            all_file_dct[pattern] = parts_file_dct

        self.add2log('')  # new line

        # comp
        name = src_dir.name

        self.add2log('処理中(comp)')
        fusion = resolve.Fusion()
        comp = fusion.NewComp()
        comp.Lock()
        # --------------------
        # pref
        fu.set_pref(comp, name, data.fps)

        # node
        ctrl_xf_name = 'Ctrl_Transform'
        end_nodes = []
        BODY_X_OFFSET = 42
        Y_OFFSET = -7
        X_OFFSET = 5
        for pattern in all_file_dct.keys():
            # offset expression parameter
            mouth_xf = None
            mouth_y_pos_list = []
            eyebrow_xf = None
            eyebrow_y_pos_list = []
            # blend expression parameter
            mouth_mg = None
            mouth_blend_list = []
            eyebrow_mg = None
            eyebrow_blend_list = []

            # Body parts
            body_x_pos = (len(all_file_dct) - len(end_nodes) - 1) * BODY_X_OFFSET
            body_y_pos = 0
            file_dct = all_file_dct[pattern]

            ld = fu.add_ld(comp, body_x_pos, body_y_pos, file_dct[cs.BODY][pattern][0])
            base_node = ld

            # parts
            part_cnt = 0
            for part in file_dct:
                self.add2log('処理中(comp, %s, %s)' % (pattern, cs.PARTS_DICT[part]))
                if part in [cs.BODY]:
                    continue
                dct = file_dct[part]
                image_list = []
                for k in dct:
                    lst = dct[k]

                    if part == cs.EYE:  # for expression
                        mouth_offset, eyebrow_offset = cs.get_offset(lst[0])
                        i = len(image_list)
                        if mouth_offset is not None:
                            mouth_y_pos_list.append((i, mouth_offset))
                        if eyebrow_offset is not None:
                            eyebrow_y_pos_list.append((i, eyebrow_offset))

                        mouth_blend, eyebrow_blend = cs.get_blend(lst[0])
                        if mouth_blend is not None:
                            mouth_blend_list.append((i, mouth_blend))
                        if eyebrow_blend is not None:
                            eyebrow_blend_list.append((i, eyebrow_blend))

                    x_pos = body_x_pos + (part_cnt * X_OFFSET)
                    y_pos = body_y_pos + (Y_OFFSET * (len(image_list) + 2))
                    result = None
                    # General
                    if part not in [cs.EYE, cs.MOUTH] or len(lst) < 3:
                        for i in range(len(lst) - 1, -1, -1):
                            ld = fu.add_ld(comp, x_pos, y_pos - i, lst[i])
                            if i == len(lst) - 1:
                                result = ld
                            else:
                                mg = comp.AddTool('Merge', x_pos + 1, y_pos - i)
                                mg.ConnectInput('Foreground', ld)
                                mg.ConnectInput('Background', result)
                                result = mg
                    # Animated
                    else:
                        ld_list = []
                        for i in range(len(lst) - 1, -1, -1):
                            ld = fu.add_ld(comp, x_pos, y_pos - i, lst[i])
                            ld_list.append(ld)

                        anim_type_list = []
                        if len(lst) == 6:  # marge 00,00v
                            for i in [4, 2, 0]:
                                mg = comp.AddTool('Merge', x_pos + 1, y_pos - i)
                                mg.ConnectInput('Foreground', ld_list[5 - i])
                                mg.ConnectInput('Background', ld_list[4 - i])
                                anim_type_list.append(mg)
                        elif len(lst) == 3:
                            anim_type_list = ld_list

                        # anim selector
                        if len(anim_type_list) == 3:
                            for i in [2, 1, 0]:
                                if i == len(anim_type_list) - 1:
                                    result = anim_type_list[2 - i]
                                else:
                                    dx = comp.AddTool(
                                        'Dissolve',
                                        x_pos + 2,
                                        y_pos - (i * int(len(lst) / len(anim_type_list)))
                                    )
                                    dx.ConnectInput('Background', anim_type_list[2 - i])
                                    dx.ConnectInput('Foreground', result)
                                    dx.Mix = 0
                                    dx.Mix.SetExpression('%s.%s - %d' % (ctrl_xf_name, part + '_anim', i))
                                    result = dx
                        else:
                            result = ld_list[0]

                    image_list.append(result)
                # empty image(-1)
                bg = comp.AddTool('Background', body_x_pos + (part_cnt * X_OFFSET), body_y_pos + (Y_OFFSET * 1))
                bg.TopLeftAlpha = 0

                image_list = [bg] + image_list

                # parts selector
                part_node = None
                x_pos = body_x_pos + (3 + part_cnt * X_OFFSET)
                for i in range(len(image_list) - 1, -1, -1):
                    y_pos = body_y_pos + (Y_OFFSET * (i + 1))
                    if i == len(image_list) - 1:
                        part_node = image_list[i]
                    else:
                        dx = comp.AddTool('Dissolve', x_pos, y_pos)
                        dx.ConnectInput('Background', image_list[i])
                        dx.ConnectInput('Foreground', part_node)
                        dx.Mix = 0
                        dx.Mix.SetExpression('%s.%s - (%d)' % (ctrl_xf_name, part, i - 1))
                        part_node = dx

                # parts marge
                xf = comp.AddTool('Transform', x_pos, body_y_pos + (Y_OFFSET * 0) - 2)
                xf.ConnectInput('Input', part_node)
                if part == cs.EYEBROW:
                    eyebrow_xf = xf
                if part == cs.MOUTH:
                    mouth_xf = xf
                mg = comp.AddTool('Merge', x_pos, body_y_pos + (Y_OFFSET * 0))
                mg.ConnectInput('Background', base_node)
                mg.ConnectInput('Foreground', xf)
                base_node = mg
                if part == cs.EYEBROW:
                    eyebrow_mg = mg
                if part == cs.MOUTH:
                    mouth_mg = mg

                part_cnt += 1

            end_nodes.append(base_node)

            # expression
            if len(mouth_y_pos_list) > 0:
                mouth_xf.Center.SetExpression(fu.make_offset_expression(mouth_y_pos_list))
            if len(eyebrow_y_pos_list) > 0:
                eyebrow_xf.Center.SetExpression(fu.make_offset_expression(eyebrow_y_pos_list))
            if len(mouth_blend_list) > 0:
                mouth_mg.Blend.SetExpression(fu.make_blend_expression(mouth_blend_list))
            if len(eyebrow_blend_list) > 0:
                eyebrow_mg.Blend.SetExpression(fu.make_blend_expression(eyebrow_blend_list))
        end_node = None

        # body selector
        for i in range(len(end_nodes) - 1, -1, -1):
            if i == len(end_nodes) - 1:
                end_node = end_nodes[i]
            else:
                dx = comp.AddTool('Dissolve', (len(all_file_dct) - i) * BODY_X_OFFSET - 3, -4 * Y_OFFSET)
                dx.ConnectInput('Background', end_nodes[i])
                dx.ConnectInput('Foreground', end_node)
                dx.Mix = 0
                dx.Mix.SetExpression('%s.%s - %d' % (ctrl_xf_name, cs.BODY, i))
                end_node = dx

        # User Control
        uc = {}
        uc_list = []
        for part in cs.PARTS_DICT:
            if part in all_file_dct['00']:
                file_dct = all_file_dct['00'][part]
                size = len(all_file_dct) if part == cs.BODY else len(file_dct) + 1
                if size != 1:
                    uc[part] = (
                        fu.get_uc(part, 0, size - 1)
                    ) if part == cs.BODY else (
                        fu.get_uc(part, -1, size - 2, center=int((size - 1) / 2))
                    )
                    uc_list.append(part)

                    if part in [cs.EYE, cs.MOUTH]:
                        uc_name = part + '_anim'
                        uc[uc_name] = fu.get_uc(uc_name, 0, 2)
                        uc_list.append(uc_name)

        # ctrl transform
        xf = comp.AddTool('Transform', len(all_file_dct) * BODY_X_OFFSET, -4 * Y_OFFSET)
        xf.ConnectInput('Input', end_node)
        xf.UserControls = uc
        xf.SetAttrs({'TOOLS_Name': ctrl_xf_name})

        # copy
        fu.copy_all_nodes(comp)
        setting_base = QApplication.clipboard().text()
        # --------------------
        comp.Unlock()
        comp_file = dst_dir.joinpath('%s.comp' % name)
        comp.Save(str(comp_file))
        comp.Close()

        self.add2log('Save: %s' % str(comp_file))

        # setting file
        setting_file = dst_dir.joinpath('%s.setting' % name)
        setting_file.write_text(fu.make_setting_file(setting_base, uc_list))
        self.add2log('Make: %s' % str(setting_file))

        self.add2log('')  # new line

        # config file
        self.add2log('設定保存(json file)')
        json_file = dst_dir.joinpath('%s.json' % name)
        data.save(json_file)
        self.add2log('Export: %s' % str(json_file))

        self.add2log('')  # new line
        # end
        self.add2log('Done!')

    def install(self):
        pass


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

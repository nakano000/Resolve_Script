import json
import sys
from functools import partial
from pathlib import Path
from enum import IntEnum

import dataclasses
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from rs.core import (
    config,
    pipe as p,
    lang,
)
from rs.gui import (
    appearance,
)
from rs_fusion.core import pose
from rs_fusion.tool.importer.importer_ui import Ui_MainWindow

APP_NAME = '読み込み(PsdSplitter用)'
APP_NAME_EN = 'Import(For PsdSplitter)'


class TatieStyle(IntEnum):
    EXPRESSION = 0
    CONNECTION = 1
    CONNECTION_LABEL = 2


@dataclasses.dataclass
class ConfigData(config.Data):
    json_path: str = ''
    style: TatieStyle = TatieStyle.CONNECTION_LABEL
    btn_size: float = 0.25
    space_x: int = 400
    space_y: int = 600
    is_normal: bool = False
    use_mm: bool = False
    use_frame_format_settings: bool = True


class Importer:
    def __init__(self, comp, fusion_ver, config_data: ConfigData, json_path: Path):
        self.comp = comp
        self.flow = comp.CurrentFrame.FlowView
        self.config_data = config_data
        self.json_path = json_path

        self.json_data = None
        self.dir = None
        self.size_x = 0
        self.size_y = 0

        self.fusion_ver = fusion_ver

        self.use_frame_format_settings = True

        self.X_OFFSET = 1
        self.Y_OFFSET = 4

    def load_json(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.json_data = json.load(f)
            self.size_x = self.json_data['x']
            self.size_y = self.json_data['y']
            if 'directory' in self.json_data:
                self.dir = Path(self.json_data['directory'])

    def set_x(self, node, x):
        _x, _y = self.flow.GetPosTable(node).values()
        self.flow.SetPos(node, x * self.X_OFFSET, _y)

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

    def add_set_dod(self, pos_x, pos_y, name, data_window):
        node = self.comp.AddTool('SetDomain', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        node.SetAttrs({'TOOLS_Name': name})
        node.Mode = 'Set'
        node.Left = data_window[0] / self.size_x
        node.Bottom = data_window[1] / self.size_y
        node.Right = data_window[2] / self.size_x
        node.Top = data_window[3] / self.size_y
        if name is not None:
            node.SetAttrs({'TOOLS_Name': name})
        return node

    def add_bg(self, pos_x, pos_y):
        bg = self.comp.AddTool('Background', pos_x * self.X_OFFSET, (pos_y - 1) * self.Y_OFFSET)
        bg.UseFrameFormatSettings = 0
        bg.Width = self.size_x
        bg.Height = self.size_y
        bg.TopLeftAlpha = 0
        bg.Depth = 1
        node = self.add_set_dod(pos_x, pos_y, None, [0, 0, 0, 0])
        node.ConnectInput('Input', bg)
        return node

    def add_base_bg(self, pos_x, pos_y):
        bg = self.comp.AddTool('Background', pos_x * self.X_OFFSET, (pos_y - 1) * self.Y_OFFSET)
        if self.use_frame_format_settings:
            bg.UseFrameFormatSettings = 1
        else:
            bg.UseFrameFormatSettings = 0
            bg.Width = self.size_x + self.config_data.space_x
            bg.Height = self.size_y + self.config_data.space_y
        bg.TopLeftAlpha = 0
        bg.Depth = 1
        node = self.add_set_dod(pos_x, pos_y, None, [0, 0, 0, 0])
        node.ConnectInput('Input', bg)
        return node

    def add_xf_bg(self, pos_x, pos_y, name):
        xf = self.comp.AddTool('Transform', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        xf.SetAttrs({'TOOLS_Name': name})
        if name == 'Root':
            bg = self.add_base_bg(pos_x, pos_y - 1)
        else:
            bg = self.add_bg(pos_x, pos_y - 1)
        return xf, bg

    def add_xf_bg_c(self, pos_x, pos_y, name):
        xf = self.comp.AddTool('Transform', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        xf.SetAttrs({'TOOLS_Name': name})
        node = self.add_bg(pos_x, pos_y - 1)
        return xf, node

    def add_ld(self, pos_x, pos_y, path: str):
        if self.dir is not None:
            # json file 基準で相対パスに画像がある場合
            _path = self.json_path.parent.joinpath(
                Path(path).relative_to(self.dir)
            )
            if _path.is_file():
                path = str(_path)

        node = self.comp.AddTool('Loader', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        node.Clip[1] = self.comp.ReverseMapPath(path.replace('/', '\\'))
        node.Loop[1] = 1
        node.PostMultiplyByAlpha = 1 if self.fusion_ver < 10 else 0
        node.GlobalIn = -1000
        node.GlobalOut = -1000
        return node

    def add_mask(self, pos_x, pos_y, data_window):
        node = self.comp.AddTool('RectangleMask', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        left = data_window[0] / self.size_x
        bottom = data_window[1] / self.size_y
        right = data_window[2] / self.size_x
        top = data_window[3] / self.size_y
        node.Center = [(left + right) / 2, (bottom + top) / 2]
        node.Width = right - left
        node.Height = top - bottom
        return node

    def add_node_A(self, pos_x, pos_y, data, name):
        pos_x += 1
        xf, bg = self.add_xf_bg(pos_x, pos_y, name)
        pos_x += 1
        pos_y -= 2

        # main
        user_controls = {}
        cb_name = ''
        cb_cnt: int = 0
        pre_node = bg
        for i, layer in enumerate(data):
            layer_name: str = layer['name']
            layer_name_en: str = layer['name_en']
            visible: bool = layer['visible']
            layer_data = layer['data']

            mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y + 1) * self.Y_OFFSET)
            if type(layer_data) is list:
                node, pos_x = self.add_node_A(pos_x, pos_y - 1, layer_data, layer_name)
                self.set_x(mg, pos_x - 1)
            else:
                node = self.add_ld(pos_x, pos_y, layer_data)
                if 'data_window' in layer.keys():
                    _mask = self.add_mask(pos_x, pos_y - 1, layer['data_window'])
                    node.ConnectInput('EffectMask', _mask)
                pos_x += 1
            mg.ConnectInput('Foreground', node)
            mg.ConnectInput('Background', pre_node)
            if layer_name.startswith('*'):
                if cb_name == '':
                    cb_name = 'N' + str(i).zfill(3)
                    user_controls[cb_name] = {
                        'LINKID_DataType': 'Number',
                        'INPID_InputControl': 'ComboControl',
                        'LINKS_Name': name if name != 'Root' else 'Select',
                        'INP_Integer': True,
                        'INP_Default': 0,
                        'ICS_ControlPage': 'User',
                    }
                dct = user_controls[cb_name]
                dct[cb_cnt + 1] = {'CCS_AddString': '%s' % layer_name}
                if visible:
                    dct['INP_Default'] = cb_cnt
                mg.Blend.SetExpression('iif(%s.%s == %d, 1, 0)' % (xf.Name, cb_name, cb_cnt))
                cb_cnt += 1
            else:
                uc_name = 'N' + str(i).zfill(3) + '_' + layer_name_en
                user_controls[uc_name] = {
                    'LINKID_DataType': 'Number',
                    'INPID_InputControl': 'CheckboxControl',
                    'LINKS_Name': layer_name,
                    'INP_Integer': True,
                    'CBC_TriState': False,
                    'INP_Default': 1 if visible else 0,
                    'ICS_ControlPage': 'User',
                    # 'ICS_ControlPage': 'Controls',
                }
                mg.Blend.SetExpression('%s.%s' % (xf.Name, uc_name))

            pre_node = mg

        # user control
        user_controls['Grp_' + name] = {
            'LINKS_Name': name,
            'LINKID_DataType': 'Number',
            'INPID_InputControl': 'LabelControl',
            'LBLC_DropDownButton': True,
            'LBLC_NumInputs': len(user_controls),
            'INP_Default': 1,
            'INP_External': False,
            'INP_Passive': True,
            'ICS_ControlPage': 'User',
        }
        if name == 'Root':
            user_controls['Refresh'] = {
                'LINKS_Name': 'Refresh',
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'ButtonControl',
                'INP_Integer': False,
                'BTNCS_Execute': "comp:StartUndo('RS Refresh');"
                                 "local tool_list = comp:GetToolList(false, 'Fuse.RS_GlobalStart');"
                                 "for k,v in pairs(tool_list) do v:Refresh() end;"
                                 "comp:EndUndo(true)\n",
                'ICS_ControlPage': 'Tools',
            }
        xf.ConnectInput('Input', pre_node)
        uc = {'__flags': 2097152}  # 順番を保持するフラグ
        for k, v in reversed(list(user_controls.items())):
            uc[k] = v
        xf.UserControls = uc
        xf = xf.Refresh()

        #
        self.set_x(xf, pos_x - 1)
        self.set_orange(xf)
        return xf, pos_x

    def add_node_B(self, pos_x, pos_y, data, name, uc, use_label):
        pos_x += 1
        xf, bg = self.add_xf_bg(pos_x, pos_y, name)
        pos_x += 1
        pos_y -= 2

        # data sort
        a_data = []
        b_data = []
        c_data = []
        for layer in data:
            if layer['name'].startswith('*'):
                b_data.append(layer)
            else:
                if len(b_data) == 0:
                    a_data.append(layer)
                else:
                    c_data.append(layer)
        _data = a_data + b_data + c_data

        # main
        pre_node = bg
        a_mg = None
        page_name = 'ポーズ' if use_label else xf.Name
        name_list = []
        user_controls = {}
        user_controls2 = {}
        uc_list = []
        for i, layer in enumerate(_data):
            layer_name: str = layer['name']
            layer_name_en: str = layer['name_en']
            visible: bool = layer['visible']
            layer_data = layer['data']
            uc_name = 'N' + str(i).zfill(3) + '_' + layer_name_en

            # add loader
            if type(layer_data) is list:
                node, pos_x, _uc, _name_list = self.add_node_B(
                    pos_x, pos_y - 1, layer_data, layer_name, {}, use_label
                )
                uc_list.append(_uc)
                name_list += _name_list
            else:
                node = self.add_ld(pos_x, pos_y, layer_data)
                if 'data_window' in layer.keys():
                    _mask = self.add_mask(pos_x, pos_y - 1, layer['data_window'])
                    node.ConnectInput('EffectMask', _mask)
            # mg
            if layer_name.startswith('*'):
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
                if not layer_name.startswith('!'):
                    user_controls[uc_name + str(pos_x)] = self.uc_button(
                        a_mg, node, page_name, layer_name, self.config_data.btn_size
                    )
            else:
                mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y + 1) * self.Y_OFFSET)
                mg.SetAttrs({'TOOLS_Name': layer_name + '_MG'})
                name_list.append(mg.Name)
                mg.ConnectInput('Background', pre_node)
                if visible or layer_name.startswith('!'):
                    mg.ConnectInput('Foreground', node)
                pre_node = mg
                if not layer_name.startswith('!'):
                    user_controls2[uc_name + '_hide_' + str(pos_x)] = self.uc_button(
                        mg, None, page_name, layer_name + ' hide', 0.5
                    )
                    user_controls2[uc_name + '_show_' + str(pos_x)] = self.uc_button(
                        mg, node, page_name, layer_name + ' show', 0.5
                    )
            pos_x += 1

        #
        for k, v in user_controls2.items():
            user_controls[k] = v
        if use_label:
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

    def add_node_ST(self, pos_x, pos_y, data, name):
        pos_x += 1
        xf, bg = self.add_xf_bg_c(pos_x, pos_y, name)
        pos_x += 1

        # main
        pre_node = bg
        for i, layer in enumerate(data):
            layer_name: str = layer['name']
            visible: bool = layer['visible']
            layer_data = layer['data']

            mg = self.comp.AddTool('Merge', pos_x * self.X_OFFSET, (pos_y - 1) * self.Y_OFFSET)
            if type(layer_data) is list:
                node, pos_x = self.add_node_ST(pos_x, pos_y - 3, layer_data, layer_name)
                self.set_x(mg, pos_x - 1)
            else:
                node = self.add_ld(pos_x, pos_y - 3, layer_data)
                if 'data_window' in layer.keys():
                    _mask = self.add_mask(pos_x, pos_y - 4, layer['data_window'])
                    node.ConnectInput('EffectMask', _mask)
                pos_x += 1
            mg.ConnectInput('Foreground', node)
            mg.ConnectInput('Background', pre_node)
            mg.Blend = 1 if visible else 0

            pre_node = mg

        xf.ConnectInput('Input', pre_node)
        #
        self.set_x(xf, pos_x - 1)
        return xf, pos_x

    def add_node_STMM(self, pos_x, pos_y, data, name):
        bg = self.add_bg(pos_x, pos_y)
        pos_x += 1
        mm = self.comp.AddTool('MultiMerge', pos_x * self.X_OFFSET, pos_y * self.Y_OFFSET)
        mm.SetAttrs({'TOOLS_Name': name})
        mm.ConnectInput('Background', bg)

        for i, layer in enumerate(data, 1):
            layer_name: str = layer['name']
            visible: bool = layer['visible']
            layer_data = layer['data']

            if type(layer_data) is list:
                node, pos_x = self.add_node_STMM(pos_x, pos_y - 3, layer_data, layer_name)
            else:
                node = self.add_ld(pos_x, pos_y - 3, layer_data)
                if 'data_window' in layer.keys():
                    _mask = self.add_mask(pos_x, pos_y - 4, layer['data_window'])
                    node.ConnectInput('EffectMask', _mask)
                pos_x += 1
            mm.ConnectInput(f'Layer{i}.Foreground', node)
            mm.SetInput(f'LayerEnabled{i}', 1 if visible else 0)

        #
        self.set_x(mm, pos_x - 1)
        return mm, pos_x

    def make(self):
        c = self.config_data
        self.use_frame_format_settings = c.use_frame_format_settings
        self.load_json()
        if c.is_normal:
            if c.use_mm:
                self.add_node_STMM(0, 0, self.json_data['data'], self.json_data['name'])
            else:
                self.add_node_ST(0, 0, self.json_data['data'], self.json_data['name'])
        else:
            if c.style == TatieStyle.EXPRESSION:
                self.add_node_A(0, 0, self.json_data['data'], self.json_data['name'])
            else:
                use_label = c.style == TatieStyle.CONNECTION_LABEL
                xf, _, _uc, name_list = self.add_node_B(
                    0, 0, self.json_data['data'], self.json_data['name'], {}, use_label
                )

                # xf
                # uc = {'__flags': 2097152}  # 順番を保持するフラグ
                uc = pose.get_uc(None)
                for k, v in reversed(list(_uc.items())):
                    uc[k] = v
                xf.UserControls = uc
                xf = xf.Refresh()
                self.set_orange(xf)

                xf.Comments = '\n'.join(reversed(name_list))


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(300, 200)

        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # translate
        self.lang_code: lang.Code = lang.load()
        self.setWindowTitle('%s' % (APP_NAME if self.lang_code == lang.Code.ja else APP_NAME_EN))
        self.translate()

        # style sheet
        self.ui.importButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.useFrameFormatSettingsCheckBox.stateChanged.connect(self.use_frame_format_settings_changed)

        self.ui.jsonToolButton.clicked.connect(partial(self.toolButton_clicked))

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.importButton.clicked.connect(self.import_json, Qt.QueuedConnection)

    def translate(self) -> None:
        if self.lang_code == lang.Code.en:
            self.ui.fileGroupBox.setTitle('File')
            self.ui.tatieFormatGroupBox.setTitle('Tatie Format')
            self.ui.connectOptionGroupBox.setTitle('Options of Switching Connection')
            self.ui.expandGroupBox.setTitle('Expand size')

            self.ui.tabWidget.setTabText(0, 'Tatie')
            self.ui.tabWidget.setTabText(1, 'Normal')

            self.ui.expRadioButton.setText('Expression')
            self.ui.connectRadioButton.setText('Switching Connection(Page)')
            self.ui.connectLabelRadioButton.setText('Switching Connection(Label)')
            self.ui.label.setText('')
            self.ui.btnSizeLabel.setText('Button Size')

    def use_frame_format_settings_changed(self, state: int) -> None:
        self.ui.expandGroupBox.setEnabled(not(state == Qt.Checked))

    def import_json(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            print(
                'Please execute in Fusion Page.'
                if self.lang_code == lang.Code.en else
                'Fusion Pageで実行してください。'
            )
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            print(
                'Composition not found.'
                if self.lang_code == lang.Code.en else
                'コンポジションが見付かりません。'
            )
            return
        ver = self.fusion.Version

        # main
        c = self.get_data()
        comp.Lock()
        comp.StartUndo('RS Import')
        json_path: Path = Path(comp.MapPath(c.json_path))
        importer = Importer(comp, ver, self.get_data(), json_path)
        importer.make()
        comp.EndUndo(True)
        comp.Unlock()
        QMessageBox.information(self, "Info", 'Done!')
        print('Done!')

    def toolButton_clicked(self) -> None:
        w = self.ui.jsonLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select JSON File',
            w.text(),
            'JSON File (*.json)',
        )
        if path != '':
            w.setText(path)

    def set_data(self, c: ConfigData):
        self.ui.jsonLineEdit.setText(c.json_path)
        if c.style == TatieStyle.EXPRESSION:
            self.ui.expRadioButton.setChecked(True)
        elif c.style == TatieStyle.CONNECTION:
            self.ui.connectRadioButton.setChecked(True)
        else:
            self.ui.connectLabelRadioButton.setChecked(True)

        self.ui.btnSizeSpinBox.setValue(c.btn_size)

        self.ui.xSpinBox.setValue(c.space_x)
        self.ui.ySpinBox.setValue(c.space_y)

        self.ui.tabWidget.setCurrentIndex(1 if c.is_normal else 0)
        self.ui.useMMCheckBox.setChecked(c.use_mm)

        self.ui.useFrameFormatSettingsCheckBox.setChecked(c.use_frame_format_settings)
        self.ui.expandGroupBox.setEnabled(not c.use_frame_format_settings)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.json_path = self.ui.jsonLineEdit.text()
        if self.ui.expRadioButton.isChecked():
            c.style = TatieStyle.EXPRESSION
        elif self.ui.connectRadioButton.isChecked():
            c.style = TatieStyle.CONNECTION
        else:
            c.style = TatieStyle.CONNECTION_LABEL

        c.btn_size = self.ui.btnSizeSpinBox.value()

        c.space_x = self.ui.xSpinBox.value()
        c.space_y = self.ui.ySpinBox.value()

        c.is_normal = self.ui.tabWidget.currentIndex() == 1
        c.use_mm = self.ui.useMMCheckBox.isChecked()

        c.use_frame_format_settings = self.ui.useFrameFormatSettingsCheckBox.isChecked()

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

import json
import sys
from functools import partial
from pathlib import Path
from enum import IntEnum

import dataclasses
from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
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
from rs_fusion.tool.import_exr.import_exr_ui import Ui_MainWindow

APP_NAME = 'Import EXR'


@dataclasses.dataclass
class ConfigData(config.Data):
    exr_path: str = ''
    btn_size: float = 0.25
    is_normal: bool = False


class Importer:
    def __init__(self, comp, config_data: ConfigData, exr_path: Path):
        self.comp = comp
        self.flow = comp.CurrentFrame.FlowView
        self.config_data = config_data
        self.exr_path = exr_path

        self.size_x = 0
        self.size_y = 0

        self.X_OFFSET = 1
        self.Y_OFFSET = 4

        self.exr_node = None
        self.blank_node = None

        self.layer_list: list[str] = []
        self.tree_data = None
        self.json_data = None

    def load_json(self):
        dir_path = self.exr_path.parent
        name = self.exr_path.stem
        json_path = dir_path.joinpath(name + '.info.json')
        if json_path.is_file():
            with open(json_path, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)

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

    def setup_tree_data(self):
        dct = {'Root': {'visible': True, 'data': {}}}
        for layer in self.layer_list:
            ss = layer.split('.')
            pre_dct = dct['Root']['data']
            for i, name in enumerate(ss):
                # image layer
                if i == len(ss) - 1:
                    if layer not in pre_dct:
                        pre_dct[layer] = {
                            'visible': True,
                        }
                    continue
                # group layer
                if name not in pre_dct:
                    pre_dct[name] = {
                        'visible': True,
                    }
                if 'data' not in pre_dct[name]:
                    pre_dct[name]['data'] = {}
                pre_dct = pre_dct[name]['data']
        self.tree_data = dct

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

        # layer to Tree
        self.setup_tree_data()
        self.load_json()

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
        page_name = 'POSE'
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
                        a_mg, node, page_name, _name, self.config_data.btn_size
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

    def add_node_ST(self, pos_x, pos_y, data, name):
        pos_x += 1
        xf = self.add_tool('Transform', pos_x, pos_y)
        xf.SetAttrs({'TOOLS_Name': name})
        wire = self.add_blank(pos_x, pos_y - 1)
        pos_x += 1

        # main
        pre_node = wire
        for layer_name, layer in data.items():
            visible: bool = layer['visible']

            mg = self.add_tool('Merge', pos_x, pos_y - 1)
            if 'data' in layer:
                node, pos_x = self.add_node_ST(pos_x, pos_y - 3, layer['data'], layer_name)
                self.set_x(mg, pos_x - 1)
            else:
                node = self.add_layer(pos_x, pos_y - 3, layer_name)
                pos_x += 1
            mg.ConnectInput('Foreground', node)
            mg.ConnectInput('Background', pre_node)
            mg.Blend = 1 if visible else 0

            pre_node = mg

        xf.ConnectInput('Input', pre_node)
        #
        self.set_x(xf, pos_x - 1)
        return xf, pos_x

    def make(self):
        # c = self.config_data
        # self.load_json()
        self.setup_base_node()
        if self.json_data is None:
            self.add_node_ST(
                0, 0, self.tree_data['Root']['data'], 'Root'
            )
        else:
            xf, _, _uc, name_list = self.add_node(
                0, 0, self.json_data['Root']['data'], 'Root', {},
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
        self.resize(400, 100)

        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # translate
        self.setWindowTitle(APP_NAME)

        # style sheet
        self.ui.importButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.exrToolButton.clicked.connect(partial(self.toolButton_clicked))

        self.ui.closeButton.clicked.connect(self.close)
        self.ui.importButton.clicked.connect(self.import_json, Qt.QueuedConnection)

    def import_json(self) -> None:
        resolve = self.fusion.GetResolve()
        if resolve and resolve.GetCurrentPage() != 'fusion':
            QMessageBox.warning(self, 'Error', 'Please execute in Fusion Page.')
            return

        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            QMessageBox.warning(self, 'Error', 'Composition not found.')
            return

        # main
        c = self.get_data()
        if c.exr_path == '':
            QMessageBox.warning(self, 'Error', 'Please select EXR file.')
            return
        if not Path(c.exr_path).is_file():
            QMessageBox.warning(self, 'Error', 'EXR file not found: %s' % c.exr_path)
            return
        comp.Lock()
        comp.StartUndo('RS Import')
        exr_path: Path = Path(comp.MapPath(c.exr_path))
        importer = Importer(comp, c, exr_path)
        importer.make()
        comp.EndUndo(True)
        comp.Unlock()
        QMessageBox.information(self, "Info", 'Done!')
        print('Done!')

    def toolButton_clicked(self) -> None:
        w = self.ui.exrLineEdit
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Select EXR File',
            w.text(),
            'EXR File (*.exr)',
        )
        if path != '':
            w.setText(path)

    def set_data(self, c: ConfigData):
        self.ui.exrLineEdit.setText(c.exr_path)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.exr_path = self.ui.exrLineEdit.text().strip()
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

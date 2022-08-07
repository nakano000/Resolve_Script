from functools import partial, cmp_to_key

import dataclasses
import sys
from pathlib import Path
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow, QMessageBox,
)

from rs.core import (
    config,
    pipe as p,
)
from rs.core.app import (
    Fusion,
    Resolve,
)
from rs.gui import (
    appearance,
)
from rs_fusion.tool.tatie.tatie_ui import Ui_MainWindow

APP_NAME = '立ち絵アシスタント'


@dataclasses.dataclass
class ConfigData(config.Data):
    post_multiply: bool = False
    use_cb: bool = True
    cb_name: str = 'Select'
    width: int = 1920
    height: int = 1080


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
        self.resize(250, 250)

        self.fusion = fusion

        # config
        self.config_file: Path = config.CONFIG_DIR.joinpath('%s.json' % APP_NAME)
        self.load_config()

        # button
        self.ui.loaderButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.margeButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.loaderButton.clicked.connect(self.make_loader)
        self.ui.margeButton.clicked.connect(self.marge)
        self.ui.closeButton.clicked.connect(self.close)

    def make_loader(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            QMessageBox.warning(self, 'Warning', 'Fusion Pageで実行してください。')
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            QMessageBox.warning(self, 'Warning', 'コンポジションが見付かりません。')
            return

        # data
        data = self.get_data()

        flow = comp.CurrentFrame.FlowView
        _x = -32768  # 自動を自動的に
        _y = -32768

        # Files
        urls, _ = QFileDialog.getOpenFileNames(
            caption="画像選択",
            filter="music(*.dpx *.exr *.j2c *.jpg *.png *.tga *.tif)")
        if not urls:
            return

        # undo
        comp.Lock()
        comp.StartUndo('RS Loader')

        # deselect
        for n in comp.GetToolList(False):
            flow.Select(n, False)

        # import
        node = None
        for url in urls:
            node = comp.AddTool('Loader', _x, _y)
            if _x == -32768:
                _x, _y = flow.GetPosTable(node).values()
                _x = int(_x)
                _y = int(_y)
                flow.SetPos(node, _x, _y)
                print(_x, _y)
            node.Clip[1] = comp.ReverseMapPath(url.replace('/', '\\'))
            node.Loop[1] = 1
            node.PostMultiplyByAlpha = 1 if data.post_multiply else 0

            flow.Select(node)
            _x += 1

        # end
        comp.EndUndo(True)
        comp.Unlock()
        print('Done!')

    def marge(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            QMessageBox.warning(self, 'Warning', 'Fusion Pageで実行してください。')
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            QMessageBox.warning(self, 'Warning', 'コンポジションが見付かりません。')
            return

        # tools
        tools = list(comp.GetToolList(True).values())
        if len(tools) == 0:
            QMessageBox.warning(self, 'Warning', 'ノードを選択してください。')
            return
        flow = comp.CurrentFrame.FlowView
        tools.sort(key=lambda x: list(flow.GetPosTable(x).values())[0])

        # data
        data = self.get_data()

        # undo
        comp.Lock()
        comp.StartUndo('RS Marge')

        # XF
        _x, _y = flow.GetPosTable(tools[len(tools) - 1]).values()
        xf = comp.AddTool('Transform', _x + 1, _y + 4)

        # BG
        _x, _y = flow.GetPosTable(tools[0]).values()
        bg = comp.AddTool('Background', _x - 1, _y + 4)
        bg.UseFrameFormatSettings = 0
        bg.Width = data.width
        bg.Height = data.height
        bg.TopLeftAlpha = 0
        bg.Depth = 1

        pre_node = bg

        # user_controls
        user_controls = {}
        cb_name = 'RS_ComboBox'
        if data.use_cb:
            user_controls[cb_name] = {
                'LINKID_DataType': 'Number',
                'INPID_InputControl': 'ComboControl',
                'LINKS_Name': data.cb_name,
                'INP_Integer': True,
                'INP_Default': 0,
                'ICS_ControlPage': 'User',
            }
        for i, layer in enumerate(tools):
            layer_name: str = layer.Name
            if layer.ID == 'Loader':
                layer_name = Path(layer.Clip[1]).stem.strip()
            _x, _y = flow.GetPosTable(layer).values()
            mg = comp.AddTool('Merge', _x, _y + 4)
            mg.ConnectInput('Foreground', layer)
            mg.ConnectInput('Background', pre_node)
            if data.use_cb:
                dct = user_controls[cb_name]
                dct[i + 1] = {'CCS_AddString': '%s' % layer_name}
                mg.Blend.SetExpression('iif(%s.%s == %d, 1, 0)' % (xf.Name, cb_name, i))
            else:
                uc_name = 'N' + str(i).zfill(3) + '_' + layer.Name
                user_controls[uc_name] = {
                    'LINKID_DataType': 'Number',
                    'INPID_InputControl': 'CheckboxControl',
                    'LINKS_Name': layer_name,
                    'INP_Integer': True,
                    'CBC_TriState': False,
                    'INP_Default': 1,
                    'ICS_ControlPage': 'User',
                    # 'ICS_ControlPage': 'Controls',
                }
                mg.Blend.SetExpression('%s.%s' % (xf.Name, uc_name))
            pre_node = mg
        # xf
        xf.ConnectInput('Input', pre_node)
        uc = {'__flags': 2097152}  # 順番を保持するフラグ
        for k, v in list(user_controls.items()):
            uc[k] = v
        xf.UserControls = uc
        xf.Refresh()

        # end
        comp.EndUndo(True)
        comp.Unlock()
        print('Done!')

    def new_config(self):
        return ConfigData()

    def set_data(self, c: ConfigData):
        self.ui.multiplyCheckBox.setChecked(c.post_multiply)
        self.ui.cbGroupBox.setChecked(c.use_cb)
        self.ui.cbNameLineEdit.setText(c.cb_name)
        self.ui.widthSpinBox.setValue(c.width)
        self.ui.heightSpinBox.setValue(c.height)

    def get_data(self) -> ConfigData:
        c = self.new_config()
        c.post_multiply = self.ui.multiplyCheckBox.isChecked()
        c.use_cb = self.ui.cbGroupBox.isChecked()
        c.cb_name = self.ui.cbNameLineEdit.text().strip()
        if c.cb_name == '':
            c.cb_name = 'Select'
        c.width = self.ui.widthSpinBox.value()
        c.height = self.ui.heightSpinBox.value()
        return c

    def load_config(self) -> None:
        c = self.new_config()
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

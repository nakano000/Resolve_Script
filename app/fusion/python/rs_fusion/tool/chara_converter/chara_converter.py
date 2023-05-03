import sys
from functools import partial
from pathlib import Path

import dataclasses
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtGui import (
    QColor,
)
from PySide2.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
)

from rs.core import (
    config,
    pipe as p,
    util,
)
from rs.gui import (
    appearance,
    log,
)
from rs_fusion.tool.chara_converter import chara_sozai
from rs_fusion.tool.chara_converter.chara_converter_ui import Ui_MainWindow

APP_NAME = 'キャラ素材変換'


@dataclasses.dataclass
class ConfigData(config.Data):
    src_dir: str = ''
    dst_dir: str = ''
    make_dir: bool = True


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
        self.resize(400, 500)

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
        src_text = data.src_dir
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
        # make dir
        if data.make_dir and src_dir.name != dst_dir.name:
            dst_dir = dst_dir.joinpath(src_dir.name)
            dst_dir.mkdir(parents=True, exist_ok=True)
            self.add2log('フォルダ作成: %s' % str(dst_dir))
        self.add2log('')  # new line
        # comp check
        comp = self.fusion.CurrentComp
        if comp is None:
            self.add2log('[ERROR]コンポジションが見付かりません。', log.ERROR_COLOR)
            return
        ver = self.fusion.Version

        # file_dataをパーツ、プレフィックスで整理する
        self.add2log('処理中(前準備)')
        src_data, width, height = chara_sozai.preprocess(src_dir)

        # コンバート
        dst_data = chara_sozai.convert(width, height, src_data, dst_dir, self.add2log)

        # import
        importer = chara_sozai.Importer(comp, ver, width, height, dst_data, self.add2log)
        comp.Lock()
        comp.StartUndo('RS Import')
        importer.import_chara()
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
        self.ui.makeDirCheckBox.setChecked(c.make_dir)

    def get_data(self) -> ConfigData:
        c = ConfigData()
        c.src_dir = self.ui.srcLineEdit.text()
        c.dst_dir = self.ui.dstLineEdit.text()
        c.make_dir = self.ui.makeDirCheckBox.isChecked()

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

import sys
import functools
from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)

from rs.core import (
    pipe as p, lang,
)
from rs.gui import (
    appearance,
)
from rs_fusion.tool.path_mapper.path_mapper_ui import Ui_MainWindow

APP_NAME = 'PathMapper'


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
        self.resize(140, 100)

        self.fusion = fusion

        # translate
        self.lang_code: lang.Code = lang.load()
        self.translate()

        # button
        self.ui.applyButton.setStyleSheet(appearance.in_stylesheet)
        self.ui.removeButton.setStyleSheet(appearance.in_stylesheet)

        # event
        self.ui.applyButton.clicked.connect(
            functools.partial(self.pathmap, True)
        )
        self.ui.removeButton.clicked.connect(
            functools.partial(self.pathmap, False)
        )
        self.ui.closeButton.clicked.connect(self.close)

    def translate(self) -> None:
        if self.lang_code == lang.Code.en:
            self.ui.applyButton.setText('apply')
            self.ui.removeButton.setText('remove')
            self.ui.closeButton.setText('close')

    def pathmap(self, use_pathmap: bool) -> None:
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            if self.lang_code == lang.Code.en:
                QMessageBox.warning(self, 'Warning', 'Please run in Fusion Page.')
            else:
                QMessageBox.warning(self, 'Warning', 'Fusion Pageで実行してください。')
            return
        comp = self.fusion.CurrentComp
        if comp is None:
            if self.lang_code == lang.Code.en:
                QMessageBox.warning(self, 'Warning', 'Composition not found.')
            else:
                QMessageBox.warning(self, 'Warning', 'コンポジションが見付かりません。')
            return

        undo_name = 'RS Path Map' if use_pathmap else 'RS Path Unmap'

        comp.Lock()
        comp.StartUndo(undo_name)
        tools: dict = comp.GetToolList(True, 'Loader')
        for tool in tools.values():
            if use_pathmap:
                tool.Clip[1] = comp.ReverseMapPath(tool.Clip[1])
            else:
                tool.Clip[1] = comp.MapPath(tool.Clip[1])
        comp.EndUndo(True)
        comp.Unlock()


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

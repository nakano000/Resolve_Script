import sys

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
)

from rs.gui import (
    appearance,
)

from rs_fusion.core import operator as op

from rs_fusion.tool.comp_utility.comp_utility_ui import Ui_MainWindow

APP_NAME = 'CompUtility'


class MainWindow(QMainWindow):
    def __init__(self, parent=None, fusion=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowCloseButtonHint
            # | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.MSWindowsFixedSizeDialogHint
        )
        self.resize(140, 60)

        self.fusion = fusion

        # window
        self.pivot_window = None
        self.insert_window = None
        self.copy_window = None
        self.bake_window = None
        self.bg_window = None
        self.color_window = None
        self.font_window = None
        self.paste_window = None
        self.center_window = None
        self.number_window = None
        self.nudge_window = None
        self.separate_window = None

        # menu
        lst = [
            ('STILL IMAGE', self.load),
            ('SEPARATE LAYERS', self.separate),
            ('MERGE', self.merge),
            ('INSERT', self.insert_tool),
            ('NUDGE', self.nudge_tool),
            ('PIVOT', self.pivot_tool),
            ('CENTER', self.center_tool),
            ('NUMBER', self.number_tool),
            ('COPY PARAM', self.copy_tool),
            ('BAKE PARAM', self.bake_tool),
            ('BG', self.bg_tool),
            ('COLOR', self.color_tool),
            ('FONT', self.font_tool),
            ('PASTE SETTING', self.paste_tool),
        ]
        b = self.ui.toolButton
        menu = QMenu(b)
        for x in lst:
            act = QAction(x[0], b)
            act.triggered.connect(x[1])
            menu.addAction(act)
        b.setMenu(menu)

        # style sheet
        b.setStyleSheet(appearance.other_stylesheet)

    def check_page(self):
        resolve = self.fusion.GetResolve()
        if resolve is not None and resolve.GetCurrentPage() != 'fusion':
            return False
        return True

    def get_comp(self):
        if not self.check_page():
            return None
        comp = self.fusion.CurrentComp
        if comp is None:
            return None
        return comp

    def load(self):
        comp = self.get_comp()
        if comp is None:
            return
        op.loader(comp)

    def merge(self):
        comp = self.get_comp()
        if comp is None:
            return
        op.merge(comp)

    def insert_tool(self):
        from rs_fusion.tool.insert_tool import MainWindow as InsertWindow
        if self.insert_window is None:
            self.insert_window = InsertWindow(fusion=self.fusion)
        self.insert_window.show()

    def pivot_tool(self):
        from rs_fusion.tool.pivot_tool import MainWindow as PivotWindow
        if self.pivot_window is None:
            self.pivot_window = PivotWindow(fusion=self.fusion)
        self.pivot_window.show()

    def copy_tool(self):
        from rs_fusion.tool.copy_tool import MainWindow as CopyWindow
        if self.copy_window is None:
            self.copy_window = CopyWindow(fusion=self.fusion)
        self.copy_window.show()

    def bake_tool(self):
        from rs_fusion.tool.bake_tool import MainWindow as BakeWindow
        if self.bake_window is None:
            self.bake_window = BakeWindow(fusion=self.fusion)
        self.bake_window.show()

    def bg_tool(self):
        from rs_fusion.tool.bg_tool import MainWindow as BgWindow
        if self.bg_window is None:
            self.bg_window = BgWindow(fusion=self.fusion)
        self.bg_window.show()

    def color_tool(self):
        from rs_fusion.tool.color_tool import MainWindow as ColorWindow
        if self.color_window is None:
            self.color_window = ColorWindow(fusion=self.fusion)
        self.color_window.show()

    def font_tool(self):
        from rs_fusion.tool.font_tool import MainWindow as FontWindow
        if self.font_window is None:
            self.font_window = FontWindow(fusion=self.fusion)
        self.font_window.show()

    def paste_tool(self):
        from rs_fusion.tool.paste_tool import MainWindow as PasteWindow
        if self.paste_window is None:
            self.paste_window = PasteWindow(fusion=self.fusion)
        self.paste_window.show()

    def center_tool(self):
        from rs_fusion.tool.center_tool import MainWindow as CenterWindow
        if self.center_window is None:
            self.center_window = CenterWindow(fusion=self.fusion)
        self.center_window.show()

    def number_tool(self):
        from rs_fusion.tool.number_tool import MainWindow as NumberWindow
        if self.number_window is None:
            self.number_window = NumberWindow(fusion=self.fusion)
        self.number_window.show()

    def nudge_tool(self):
        from rs_fusion.tool.nudge_tool import MainWindow as NudgeWindow
        if self.nudge_window is None:
            self.nudge_window = NudgeWindow(fusion=self.fusion)
        self.nudge_window.show()

    def separate(self):
        from rs_fusion.tool.separate_layers import MainWindow as SeparateWindow
        if self.separate_window is None:
            self.separate_window = SeparateWindow(fusion=self.fusion)
        self.separate_window.show()


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

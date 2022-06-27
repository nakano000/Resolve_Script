import sys
from pathlib import Path

from PySide2.QtCore import (
    Qt,
)
from PySide2.QtWidgets import (
    QApplication,
    QWidget,
    QShortcut,
)
from PySide2.QtGui import (
    QKeySequence,
)

from rs.core import (
    pipe as p,
)
from rs.gui import (
    appearance,
)
from rs.tool.macro2group.macro2group_ui import Ui_Form

APP_NAME = 'Macro2Group'


class Form(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(APP_NAME)
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            | Qt.WindowStaysOnTopHint
        )
        self.resize(200, 200)
        self.setAcceptDrops(True)
        self.ui.label.setText('DROP AREA')

        QShortcut(QKeySequence('Ctrl+V'), self, self.conv)

    def conv(self):
        clipboard = QApplication.clipboard()
        setting = clipboard.text().replace('MacroOperator', 'GroupOperator')
        clipboard.setText(setting)
        self.ui.label.setText('DONE!')

    def moveEvent(self, e):
        self.ui.label.setText('DROP AREA')
        super().moveEvent(e)

    def leaveEvent(self, e):
        self.ui.label.setText('DROP AREA')
        super().leaveEvent(e)

    def resizeEvent(self, e):
        self.ui.label.setText('DROP AREA')
        super().resizeEvent(e)

    def dragEnterEvent(self, e):
        self.ui.label.setText('DROP AREA')
        mimeData = e.mimeData()

        # for mimetype in mimeData.formats():
        #     print('MIMEType:', mimetype)

        if mimeData.hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        paths = p.pipe(
            e.mimeData().urls(),
            p.map(p.call.toLocalFile()),
            p.map(Path),
            p.filter(p.call.is_file()),
            p.filter(lambda f: f.name.lower().endswith('.setting')),
            p.map(str),
            p.map(p.call.replace('\\', '/')),
            list,
            sorted,
        )
        if len(paths) > 0:
            setting = Path(paths[0]).read_text(encoding='utf-8').replace('MacroOperator', 'GroupOperator')
            clipboard = QApplication.clipboard()
            clipboard.setText(setting)
            self.ui.label.setText('DONE!')


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = Form()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()

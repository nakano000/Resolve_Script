import sys

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.core import (
    lang,
)
from rs.gui import (
    appearance,
)
from rs.gui.lang.lang_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Lang')
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
            # | Qt.WindowStaysOnTopHint
        )
        self.resize(100, 50)

        # style sheet
        self.ui.setButton.setStyleSheet(appearance.ex_stylesheet)

        # event

        self.ui.cancelButton.clicked.connect(self.close)
        self.ui.setButton.clicked.connect(self.save)

    def open(self) -> None:
        lang_code = lang.load()
        self.ui.UseEnBox.setChecked(lang_code == lang.Code.en)

    def save(self) -> None:
        lang_code = lang.Code.en if self.ui.UseEnBox.isChecked() else lang.Code.ja
        lang.save(lang_code)
        self.close()

    def show(self) -> None:
        self.open()
        super().show()


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

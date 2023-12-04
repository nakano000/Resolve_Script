import re
import sys

import pykakasi

from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from rs.core import (
    pipe as p,
)

from rs.gui import (
    appearance,
)
from rs.tool.voicevox_sequencer.lyrics_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle('Lyrics')
        self.setWindowFlags(
            Qt.Window
            | Qt.WindowCloseButtonHint
        )
        self.resize(500, 500)

        # style sheet
        self.ui.convToolButton.setStyleSheet(appearance.other_stylesheet)
        # event
        self.ui.convToolButton.clicked.connect(self.conv)

    def conv(self):
        pattern = re.compile(r'\n([ァィゥェォャュョヮ])')
        src_text = self.ui.srcPlainTextEdit.toPlainText()
        kks = pykakasi.kakasi()
        text = '\n'.join(p.pipe(
            src_text.split(),
            p.map(lambda x: x.strip()),
            lambda x: kks.convert(' '.join(x)),
            p.map(lambda x: x['kana']),
            p.map(lambda x: '\n'.join(x)),
            p.map(lambda x: pattern.sub(r'\1', x)),
            list,
        ))
        self.ui.dstPlainTextEdit.setPlainText(text)


def run() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(appearance.palette)
    app.setStyleSheet(appearance.stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run()

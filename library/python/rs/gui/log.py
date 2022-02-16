from PySide2.QtWidgets import (
    QTextEdit,
    QApplication,
)
from PySide2.QtGui import (
    QColor,
)

TEXT_COLOR = QColor(210, 210, 210)
ERROR_COLOR = QColor(210, 0, 0)


class LogTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def log(self, text: str, color: QColor = TEXT_COLOR) -> None:
        self.setTextColor(color)
        self.append(text)
        self.setTextColor(TEXT_COLOR)
        QApplication.processEvents()

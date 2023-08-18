# -*- coding: utf-8 -*-

import sys

from PySide6 import QtCore

from PySide6.QtWidgets import QApplication, QWidget

from rs.gui.frame_layout.frame_layout_ui import Ui_Form


class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._collapse = False
        self._text = ''
        self.setText('')

        # event
        self.ui.toolButton.clicked.connect(self.toggleCollapse)

    def setText(self, s):
        self._text = s
        self.ui.toolButton.setText(' ' + s)

    def setStyleSheetToTitle(self, styleSheet):
        self.ui.toolButton.setStyleSheet(styleSheet)

    def text(self):
        return self._text

    def isCollapse(self):
        return self._collapse

    def setCollapse(self, b):
        self._collapse = b
        self.ui.frame.setHidden(self._collapse)

        if self._collapse:
            self.ui.toolButton.setArrowType(QtCore.Qt.RightArrow)
        else:
            self.ui.toolButton.setArrowType(QtCore.Qt.DownArrow)

    def toggleCollapse(self):
        self.setCollapse(not self._collapse)

    def layout(self):
        return self.ui.frame.layout()

    def setLayout(self, l):
        self.ui.frame.setLayout(l)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    form = Form()

    form.setText('t')

    form.show()

    sys.exit(app.exec_())

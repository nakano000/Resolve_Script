# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lyrics.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPlainTextEdit,
    QSizePolicy, QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(450, 362)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(4, 4, 4, 4)
        self.srcPlainTextEdit = QPlainTextEdit(self.centralwidget)
        self.srcPlainTextEdit.setObjectName(u"srcPlainTextEdit")

        self.horizontalLayout.addWidget(self.srcPlainTextEdit)

        self.convToolButton = QToolButton(self.centralwidget)
        self.convToolButton.setObjectName(u"convToolButton")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.convToolButton.sizePolicy().hasHeightForWidth())
        self.convToolButton.setSizePolicy(sizePolicy)
        self.convToolButton.setMinimumSize(QSize(40, 100))
        self.convToolButton.setArrowType(Qt.RightArrow)

        self.horizontalLayout.addWidget(self.convToolButton)

        self.dstPlainTextEdit = QPlainTextEdit(self.centralwidget)
        self.dstPlainTextEdit.setObjectName(u"dstPlainTextEdit")

        self.horizontalLayout.addWidget(self.dstPlainTextEdit)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.convToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
    # retranslateUi


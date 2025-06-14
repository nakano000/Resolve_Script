# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'separate_layers.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(322, 50)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.layerMuxerButton = QPushButton(self.centralwidget)
        self.layerMuxerButton.setObjectName(u"layerMuxerButton")
        self.layerMuxerButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.layerMuxerButton)

        self.wirelessLinkButton = QPushButton(self.centralwidget)
        self.wirelessLinkButton.setObjectName(u"wirelessLinkButton")
        self.wirelessLinkButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.wirelessLinkButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.layerMuxerButton.setText(QCoreApplication.translate("MainWindow", u"Layer Muxer", None))
        self.wirelessLinkButton.setText(QCoreApplication.translate("MainWindow", u"Wireless Link", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


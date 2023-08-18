# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'resolve_launcher.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

from rs.tool.resolve_launcher.drag_button import DragButton

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(684, 282)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.resolveLineEdit = QLineEdit(self.centralwidget)
        self.resolveLineEdit.setObjectName(u"resolveLineEdit")

        self.gridLayout.addWidget(self.resolveLineEdit, 0, 1, 1, 1)

        self.resolveToolButton = QToolButton(self.centralwidget)
        self.resolveToolButton.setObjectName(u"resolveToolButton")

        self.gridLayout.addWidget(self.resolveToolButton, 0, 2, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.fusionLineEdit = QLineEdit(self.centralwidget)
        self.fusionLineEdit.setObjectName(u"fusionLineEdit")

        self.gridLayout.addWidget(self.fusionLineEdit, 1, 1, 1, 1)

        self.fusionToolButton = QToolButton(self.centralwidget)
        self.fusionToolButton.setObjectName(u"fusionToolButton")

        self.gridLayout.addWidget(self.fusionToolButton, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.verticalSpacer = QSpacerItem(653, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.dragButton = DragButton(self.centralwidget)
        self.dragButton.setObjectName(u"dragButton")
        self.dragButton.setMinimumSize(QSize(100, 100))

        self.horizontalLayout_2.addWidget(self.dragButton)

        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setMaximumSize(QSize(16777215, 100))
        self.plainTextEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.plainTextEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.resolveButton = QPushButton(self.centralwidget)
        self.resolveButton.setObjectName(u"resolveButton")
        self.resolveButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.resolveButton)

        self.fusionButton = QPushButton(self.centralwidget)
        self.fusionButton.setObjectName(u"fusionButton")
        self.fusionButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.fusionButton)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Resolve", None))
        self.resolveToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Fusion", None))
        self.fusionToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"DaVinciResolve \u307e\u305f\u306f Fusion \u8d77\u52d5\u6642\u306b\u81ea\u52d5\u3067\u9589\u3058\u308b", None))
        self.dragButton.setText(QCoreApplication.translate("MainWindow", u"\u8a2d\u5b9a", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"\u521d\u56de\u8d77\u52d5\u6642\u3001\u307e\u305f\u306f\u30b9\u30af\u30ea\u30d7\u30c8\u304c\u30e1\u30cb\u30e5\u30fc\u306b\u8868\u793a\u3055\u308c\u306a\u3044\u5834\u5408\n"
"\u5de6\u306e\u8a2d\u5b9a\u30dc\u30bf\u30f3\u3092DaVinci Resolve\u306e\u30b3\u30f3\u30bd\u30fc\u30eb\u3078\u30c9\u30e9\u30c3\u30b0\u30a2\u30f3\u30c9\u30c9\u30ed\u30c3\u30d7\u3057\u3066\u304f\u3060\u3055\u3044\u3002\n"
"Path Map\u306eUserPaths:\u3078$(RS_FUSION_USER_PATH)\u3092\u8ffd\u52a0\u3057\u307e\u3059\u3002\n"
"\u3053\u308c\u3067\u30e1\u30cb\u30e5\u30fc\u306b\u30b9\u30af\u30ea\u30d7\u30c8\u304c\u8868\u793a\u3055\u308c\u307e\u3059\u3002", None))
        self.resolveButton.setText(QCoreApplication.translate("MainWindow", u"Resolve", None))
        self.fusionButton.setText(QCoreApplication.translate("MainWindow", u"Fusion", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


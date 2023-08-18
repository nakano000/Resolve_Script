# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_button.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(295, 166)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.refreshCheckBox = QCheckBox(self.centralwidget)
        self.refreshCheckBox.setObjectName(u"refreshCheckBox")
        self.refreshCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.refreshCheckBox)

        self.loadCheckBox = QCheckBox(self.centralwidget)
        self.loadCheckBox.setObjectName(u"loadCheckBox")
        self.loadCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.loadCheckBox)

        self.saveCheckBox = QCheckBox(self.centralwidget)
        self.saveCheckBox.setObjectName(u"saveCheckBox")
        self.saveCheckBox.setChecked(True)

        self.verticalLayout.addWidget(self.saveCheckBox)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.addButton = QPushButton(self.centralwidget)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.addButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u203bMacro\u3084Group\u3067\u306f\u3001\u4e0a\u624b\u304f\u52d5\u304b\u306a\u3044\u3088\u3046\u3067\u3059\u3002", None))
        self.refreshCheckBox.setText(QCoreApplication.translate("MainWindow", u"Refresh:\u7acb\u3061\u7d75\u7528\u3001\u30ea\u30d5\u30ec\u30c3\u30b7\u30e5\u30dc\u30bf\u30f3\u306e\u8ffd\u52a0", None))
        self.loadCheckBox.setText(QCoreApplication.translate("MainWindow", u"LoadSettings:\u30ce\u30fc\u30c9\u306e\u8aad\u307f\u8fbc\u307f\u7528\u306e\u30dc\u30bf\u30f3\u3092\u8ffd\u52a0", None))
        self.saveCheckBox.setText(QCoreApplication.translate("MainWindow", u"SaveSettings:\u30ce\u30fc\u30c9\u306e\u4fdd\u5b58\u7528\u306e\u30dc\u30bf\u30f3\u3092\u8ffd\u52a0", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"\u8ffd\u52a0", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


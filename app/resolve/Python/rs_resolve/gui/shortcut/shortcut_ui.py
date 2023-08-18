# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'shortcut.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(331, 156)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.deselectAllLineEdit = QLineEdit(self.centralwidget)
        self.deselectAllLineEdit.setObjectName(u"deselectAllLineEdit")

        self.gridLayout.addWidget(self.deselectAllLineEdit, 1, 1, 1, 1)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.razorLineEdit = QLineEdit(self.centralwidget)
        self.razorLineEdit.setObjectName(u"razorLineEdit")

        self.gridLayout.addWidget(self.razorLineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.activeTimelinePanelLineEdit = QLineEdit(self.centralwidget)
        self.activeTimelinePanelLineEdit.setObjectName(u"activeTimelinePanelLineEdit")

        self.gridLayout.addWidget(self.activeTimelinePanelLineEdit, 2, 1, 1, 1)

        self.razorTestButton = QPushButton(self.centralwidget)
        self.razorTestButton.setObjectName(u"razorTestButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.razorTestButton.sizePolicy().hasHeightForWidth())
        self.razorTestButton.setSizePolicy(sizePolicy)
        self.razorTestButton.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.razorTestButton, 0, 2, 1, 1)

        self.activeTimelinePanelTestButton = QPushButton(self.centralwidget)
        self.activeTimelinePanelTestButton.setObjectName(u"activeTimelinePanelTestButton")
        sizePolicy.setHeightForWidth(self.activeTimelinePanelTestButton.sizePolicy().hasHeightForWidth())
        self.activeTimelinePanelTestButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.activeTimelinePanelTestButton, 2, 2, 1, 1)

        self.deselectAllTestButton = QPushButton(self.centralwidget)
        self.deselectAllTestButton.setObjectName(u"deselectAllTestButton")
        sizePolicy.setHeightForWidth(self.deselectAllTestButton.sizePolicy().hasHeightForWidth())
        self.deselectAllTestButton.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.deselectAllTestButton, 1, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.setButton = QPushButton(self.centralwidget)
        self.setButton.setObjectName(u"setButton")
        self.setButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.setButton)

        self.cancelButton = QPushButton(self.centralwidget)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.cancelButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Active Panel Selection\n"
"-> Timeline", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Deselect All", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Razor", None))
        self.razorTestButton.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.activeTimelinePanelTestButton.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.deselectAllTestButton.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.setButton.setText(QCoreApplication.translate("MainWindow", u"set", None))
        self.cancelButton.setText(QCoreApplication.translate("MainWindow", u"cancel", None))
    # retranslateUi


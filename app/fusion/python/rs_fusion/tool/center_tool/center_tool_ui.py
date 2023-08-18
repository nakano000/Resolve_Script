# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'center_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(298, 558)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(280, 0))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.l2rRadioButton = QRadioButton(self.groupBox_4)
        self.l2rRadioButton.setObjectName(u"l2rRadioButton")
        self.l2rRadioButton.setChecked(True)

        self.horizontalLayout_3.addWidget(self.l2rRadioButton)

        self.randomRadioButton = QRadioButton(self.groupBox_4)
        self.randomRadioButton.setObjectName(u"randomRadioButton")

        self.horizontalLayout_3.addWidget(self.randomRadioButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(280, 140))
        self.groupBox_3.setMaximumSize(QSize(280, 140))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.distributeVButton = QPushButton(self.groupBox_3)
        self.distributeVButton.setObjectName(u"distributeVButton")
        sizePolicy.setHeightForWidth(self.distributeVButton.sizePolicy().hasHeightForWidth())
        self.distributeVButton.setSizePolicy(sizePolicy)
        self.distributeVButton.setMinimumSize(QSize(45, 45))
        self.distributeVButton.setMaximumSize(QSize(45, 45))
        font = QFont()
        font.setFamilies([u"\u30e1\u30a4\u30ea\u30aa"])
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        self.distributeVButton.setFont(font)
        self.distributeVButton.setStyleSheet(u"font:16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.distributeVButton, 0, 3, 1, 1)

        self.distributeHButton = QPushButton(self.groupBox_3)
        self.distributeHButton.setObjectName(u"distributeHButton")
        sizePolicy.setHeightForWidth(self.distributeHButton.sizePolicy().hasHeightForWidth())
        self.distributeHButton.setSizePolicy(sizePolicy)
        self.distributeHButton.setMinimumSize(QSize(45, 45))
        self.distributeHButton.setMaximumSize(QSize(45, 45))
        font1 = QFont()
        font1.setFamilies([u"\u30e1\u30a4\u30ea\u30aa"])
        font1.setPointSize(24)
        font1.setBold(False)
        font1.setItalic(False)
        self.distributeHButton.setFont(font1)
        self.distributeHButton.setStyleSheet(u"font: 24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.distributeHButton, 1, 3, 1, 1)

        self.alignLButton = QPushButton(self.groupBox_3)
        self.alignLButton.setObjectName(u"alignLButton")
        sizePolicy.setHeightForWidth(self.alignLButton.sizePolicy().hasHeightForWidth())
        self.alignLButton.setSizePolicy(sizePolicy)
        self.alignLButton.setMinimumSize(QSize(45, 45))
        self.alignLButton.setMaximumSize(QSize(45, 45))
        self.alignLButton.setFont(font1)
        self.alignLButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.alignLButton, 0, 0, 1, 1)

        self.alignHCButton = QPushButton(self.groupBox_3)
        self.alignHCButton.setObjectName(u"alignHCButton")
        sizePolicy.setHeightForWidth(self.alignHCButton.sizePolicy().hasHeightForWidth())
        self.alignHCButton.setSizePolicy(sizePolicy)
        self.alignHCButton.setMinimumSize(QSize(45, 45))
        self.alignHCButton.setMaximumSize(QSize(45, 45))
        self.alignHCButton.setFont(font)
        self.alignHCButton.setStyleSheet(u"font: 16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.alignHCButton, 1, 1, 1, 1)

        self.alignTButton = QPushButton(self.groupBox_3)
        self.alignTButton.setObjectName(u"alignTButton")
        sizePolicy.setHeightForWidth(self.alignTButton.sizePolicy().hasHeightForWidth())
        self.alignTButton.setSizePolicy(sizePolicy)
        self.alignTButton.setMinimumSize(QSize(45, 45))
        self.alignTButton.setMaximumSize(QSize(45, 45))
        self.alignTButton.setFont(font1)
        self.alignTButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.alignTButton, 1, 0, 1, 1)

        self.alignVCButton = QPushButton(self.groupBox_3)
        self.alignVCButton.setObjectName(u"alignVCButton")
        sizePolicy.setHeightForWidth(self.alignVCButton.sizePolicy().hasHeightForWidth())
        self.alignVCButton.setSizePolicy(sizePolicy)
        self.alignVCButton.setMinimumSize(QSize(45, 45))
        self.alignVCButton.setMaximumSize(QSize(45, 45))
        self.alignVCButton.setFont(font)
        self.alignVCButton.setStyleSheet(u"font: 16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.alignVCButton, 0, 1, 1, 1)

        self.alignBButton = QPushButton(self.groupBox_3)
        self.alignBButton.setObjectName(u"alignBButton")
        sizePolicy.setHeightForWidth(self.alignBButton.sizePolicy().hasHeightForWidth())
        self.alignBButton.setSizePolicy(sizePolicy)
        self.alignBButton.setMinimumSize(QSize(45, 45))
        self.alignBButton.setMaximumSize(QSize(45, 45))
        self.alignBButton.setFont(font1)
        self.alignBButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.alignBButton, 1, 2, 1, 1)

        self.alignRButton = QPushButton(self.groupBox_3)
        self.alignRButton.setObjectName(u"alignRButton")
        sizePolicy.setHeightForWidth(self.alignRButton.sizePolicy().hasHeightForWidth())
        self.alignRButton.setSizePolicy(sizePolicy)
        self.alignRButton.setMinimumSize(QSize(45, 45))
        self.alignRButton.setMaximumSize(QSize(45, 45))
        self.alignRButton.setFont(font1)
        self.alignRButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout.addWidget(self.alignRButton, 0, 2, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.useDodCheckBox = QCheckBox(self.groupBox_3)
        self.useDodCheckBox.setObjectName(u"useDodCheckBox")

        self.verticalLayout_3.addWidget(self.useDodCheckBox)

        self.useCanvasCheckBox = QCheckBox(self.groupBox_3)
        self.useCanvasCheckBox.setObjectName(u"useCanvasCheckBox")

        self.verticalLayout_3.addWidget(self.useCanvasCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(51, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(280, 0))
        self.groupBox_2.setMaximumSize(QSize(280, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.absoluteRadioButton = QRadioButton(self.groupBox_2)
        self.absoluteRadioButton.setObjectName(u"absoluteRadioButton")
        self.absoluteRadioButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.absoluteRadioButton)

        self.relativeRadioButton = QRadioButton(self.groupBox_2)
        self.relativeRadioButton.setObjectName(u"relativeRadioButton")

        self.horizontalLayout_4.addWidget(self.relativeRadioButton)

        self.horizontalSpacer_3 = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.yLineEdit = QLineEdit(self.groupBox_2)
        self.yLineEdit.setObjectName(u"yLineEdit")

        self.gridLayout_2.addWidget(self.yLineEdit, 2, 1, 1, 1)

        self.setYButton = QPushButton(self.groupBox_2)
        self.setYButton.setObjectName(u"setYButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.setYButton.sizePolicy().hasHeightForWidth())
        self.setYButton.setSizePolicy(sizePolicy1)
        self.setYButton.setMinimumSize(QSize(50, 50))
        self.setYButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.setYButton, 2, 3, 2, 1)

        self.yStepLineEdit = QLineEdit(self.groupBox_2)
        self.yStepLineEdit.setObjectName(u"yStepLineEdit")

        self.gridLayout_2.addWidget(self.yStepLineEdit, 3, 1, 1, 1)

        self.ySupLineEdit = QLineEdit(self.groupBox_2)
        self.ySupLineEdit.setObjectName(u"ySupLineEdit")

        self.gridLayout_2.addWidget(self.ySupLineEdit, 8, 1, 1, 1)

        self.xInfLineEdit = QLineEdit(self.groupBox_2)
        self.xInfLineEdit.setObjectName(u"xInfLineEdit")

        self.gridLayout_2.addWidget(self.xInfLineEdit, 5, 1, 1, 1)

        self.randomYButton = QPushButton(self.groupBox_2)
        self.randomYButton.setObjectName(u"randomYButton")
        sizePolicy1.setHeightForWidth(self.randomYButton.sizePolicy().hasHeightForWidth())
        self.randomYButton.setSizePolicy(sizePolicy1)
        self.randomYButton.setMinimumSize(QSize(50, 50))
        self.randomYButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.randomYButton, 7, 3, 2, 1)

        self.randomXButton = QPushButton(self.groupBox_2)
        self.randomXButton.setObjectName(u"randomXButton")
        sizePolicy1.setHeightForWidth(self.randomXButton.sizePolicy().hasHeightForWidth())
        self.randomXButton.setSizePolicy(sizePolicy1)
        self.randomXButton.setMinimumSize(QSize(50, 50))
        self.randomXButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.randomXButton, 5, 3, 2, 1)

        self.xStepLineEdit = QLineEdit(self.groupBox_2)
        self.xStepLineEdit.setObjectName(u"xStepLineEdit")

        self.gridLayout_2.addWidget(self.xStepLineEdit, 1, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_7, 2, 2, 1, 1)

        self.xSupLineEdit = QLineEdit(self.groupBox_2)
        self.xSupLineEdit.setObjectName(u"xSupLineEdit")

        self.gridLayout_2.addWidget(self.xSupLineEdit, 6, 1, 1, 1)

        self.yInfLineEdit = QLineEdit(self.groupBox_2)
        self.yInfLineEdit.setObjectName(u"yInfLineEdit")

        self.gridLayout_2.addWidget(self.yInfLineEdit, 7, 1, 1, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_8, 3, 2, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_11, 7, 2, 1, 1)

        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 3, 0, 1, 1)

        self.setXButton = QPushButton(self.groupBox_2)
        self.setXButton.setObjectName(u"setXButton")
        sizePolicy1.setHeightForWidth(self.setXButton.sizePolicy().hasHeightForWidth())
        self.setXButton.setSizePolicy(sizePolicy1)
        self.setXButton.setMinimumSize(QSize(50, 50))
        self.setXButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.setXButton, 0, 3, 2, 1)

        self.horizontalSpacer_12 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_12, 8, 2, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)

        self.randomButton = QPushButton(self.groupBox_2)
        self.randomButton.setObjectName(u"randomButton")
        sizePolicy1.setHeightForWidth(self.randomButton.sizePolicy().hasHeightForWidth())
        self.randomButton.setSizePolicy(sizePolicy1)
        self.randomButton.setMinimumSize(QSize(60, 106))
        self.randomButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.randomButton, 5, 4, 4, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 6, 0, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_10, 6, 2, 1, 1)

        self.xLineEdit = QLineEdit(self.groupBox_2)
        self.xLineEdit.setObjectName(u"xLineEdit")

        self.gridLayout_2.addWidget(self.xLineEdit, 0, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 5, 0, 1, 1)

        self.label_8 = QLabel(self.groupBox_2)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 8, 0, 1, 1)

        self.setButton = QPushButton(self.groupBox_2)
        self.setButton.setObjectName(u"setButton")
        sizePolicy1.setHeightForWidth(self.setButton.sizePolicy().hasHeightForWidth())
        self.setButton.setSizePolicy(sizePolicy1)
        self.setButton.setMinimumSize(QSize(60, 106))
        self.setButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout_2.addWidget(self.setButton, 0, 4, 4, 1)

        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_9, 5, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)

        self.label_7 = QLabel(self.groupBox_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_2.addWidget(self.label_7, 7, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 4, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(30, 30))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.l2rRadioButton, self.randomRadioButton)
        QWidget.setTabOrder(self.randomRadioButton, self.alignLButton)
        QWidget.setTabOrder(self.alignLButton, self.alignVCButton)
        QWidget.setTabOrder(self.alignVCButton, self.alignRButton)
        QWidget.setTabOrder(self.alignRButton, self.distributeVButton)
        QWidget.setTabOrder(self.distributeVButton, self.alignTButton)
        QWidget.setTabOrder(self.alignTButton, self.alignHCButton)
        QWidget.setTabOrder(self.alignHCButton, self.alignBButton)
        QWidget.setTabOrder(self.alignBButton, self.distributeHButton)
        QWidget.setTabOrder(self.distributeHButton, self.absoluteRadioButton)
        QWidget.setTabOrder(self.absoluteRadioButton, self.relativeRadioButton)
        QWidget.setTabOrder(self.relativeRadioButton, self.xLineEdit)
        QWidget.setTabOrder(self.xLineEdit, self.xStepLineEdit)
        QWidget.setTabOrder(self.xStepLineEdit, self.setXButton)
        QWidget.setTabOrder(self.setXButton, self.yLineEdit)
        QWidget.setTabOrder(self.yLineEdit, self.yStepLineEdit)
        QWidget.setTabOrder(self.yStepLineEdit, self.setYButton)
        QWidget.setTabOrder(self.setYButton, self.setButton)
        QWidget.setTabOrder(self.setButton, self.xInfLineEdit)
        QWidget.setTabOrder(self.xInfLineEdit, self.xSupLineEdit)
        QWidget.setTabOrder(self.xSupLineEdit, self.randomXButton)
        QWidget.setTabOrder(self.randomXButton, self.yInfLineEdit)
        QWidget.setTabOrder(self.yInfLineEdit, self.ySupLineEdit)
        QWidget.setTabOrder(self.ySupLineEdit, self.randomYButton)
        QWidget.setTabOrder(self.randomYButton, self.randomButton)
        QWidget.setTabOrder(self.randomButton, self.minimizeButton)
        QWidget.setTabOrder(self.minimizeButton, self.closeButton)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Oder", None))
        self.l2rRadioButton.setText(QCoreApplication.translate("MainWindow", u"LtoR", None))
        self.randomRadioButton.setText(QCoreApplication.translate("MainWindow", u"random", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Align", None))
        self.distributeVButton.setText(QCoreApplication.translate("MainWindow", u"|||", None))
        self.distributeHButton.setText(QCoreApplication.translate("MainWindow", u"\u2261", None))
        self.alignLButton.setText(QCoreApplication.translate("MainWindow", u"\u21e4", None))
        self.alignHCButton.setText(QCoreApplication.translate("MainWindow", u"\u2501", None))
        self.alignTButton.setText(QCoreApplication.translate("MainWindow", u"\u2912", None))
        self.alignVCButton.setText(QCoreApplication.translate("MainWindow", u"\u2503", None))
        self.alignBButton.setText(QCoreApplication.translate("MainWindow", u"\u2913", None))
        self.alignRButton.setText(QCoreApplication.translate("MainWindow", u"\u21e5", None))
        self.useDodCheckBox.setText(QCoreApplication.translate("MainWindow", u"DoD", None))
        self.useCanvasCheckBox.setText(QCoreApplication.translate("MainWindow", u"Canvas", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Input", None))
        self.absoluteRadioButton.setText(QCoreApplication.translate("MainWindow", u"Absolute", None))
        self.relativeRadioButton.setText(QCoreApplication.translate("MainWindow", u"Relative", None))
        self.setYButton.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.randomYButton.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.randomXButton.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.setXButton.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.randomButton.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"sup", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"inf", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"sup", None))
        self.setButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"inf ", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


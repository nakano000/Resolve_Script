# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'number_tool.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(298, 717)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_3 = QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.toolTreeView = QTreeView(self.tab)
        self.toolTreeView.setObjectName(u"toolTreeView")
        self.toolTreeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.toolTreeView.setSelectionMode(QAbstractItemView.SingleSelection)

        self.verticalLayout_3.addWidget(self.toolTreeView)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.toolBTreeView = QTreeView(self.tab_2)
        self.toolBTreeView.setObjectName(u"toolBTreeView")

        self.horizontalLayout_7.addWidget(self.toolBTreeView)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.modifierTreeView = QTreeView(self.tab_2)
        self.modifierTreeView.setObjectName(u"modifierTreeView")

        self.verticalLayout_5.addWidget(self.modifierTreeView)

        self.loadButton = QPushButton(self.tab_2)
        self.loadButton.setObjectName(u"loadButton")

        self.verticalLayout_5.addWidget(self.loadButton)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.tabWidget)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(280, 0))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.l2rRadioButton = QRadioButton(self.groupBox_4)
        self.l2rRadioButton.setObjectName(u"l2rRadioButton")
        self.l2rRadioButton.setChecked(True)

        self.horizontalLayout_3.addWidget(self.l2rRadioButton)

        self.r2lRadioButton = QRadioButton(self.groupBox_4)
        self.r2lRadioButton.setObjectName(u"r2lRadioButton")

        self.horizontalLayout_3.addWidget(self.r2lRadioButton)

        self.randomRadioButton = QRadioButton(self.groupBox_4)
        self.randomRadioButton.setObjectName(u"randomRadioButton")

        self.horizontalLayout_3.addWidget(self.randomRadioButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.alignGroupBox = QGroupBox(self.centralwidget)
        self.alignGroupBox.setObjectName(u"alignGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alignGroupBox.sizePolicy().hasHeightForWidth())
        self.alignGroupBox.setSizePolicy(sizePolicy)
        self.alignGroupBox.setMinimumSize(QSize(280, 80))
        self.alignGroupBox.setMaximumSize(QSize(16777215, 80))
        self.horizontalLayout_2 = QHBoxLayout(self.alignGroupBox)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.alignRButton = QPushButton(self.alignGroupBox)
        self.alignRButton.setObjectName(u"alignRButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.alignRButton.sizePolicy().hasHeightForWidth())
        self.alignRButton.setSizePolicy(sizePolicy1)
        self.alignRButton.setMinimumSize(QSize(45, 45))
        self.alignRButton.setMaximumSize(QSize(45, 45))
        font = QFont()
        font.setFamilies([u"\u30e1\u30a4\u30ea\u30aa"])
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        self.alignRButton.setFont(font)
        self.alignRButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_2.addWidget(self.alignRButton, 0, 2, 1, 1)

        self.alignLButton = QPushButton(self.alignGroupBox)
        self.alignLButton.setObjectName(u"alignLButton")
        sizePolicy1.setHeightForWidth(self.alignLButton.sizePolicy().hasHeightForWidth())
        self.alignLButton.setSizePolicy(sizePolicy1)
        self.alignLButton.setMinimumSize(QSize(45, 45))
        self.alignLButton.setMaximumSize(QSize(45, 45))
        self.alignLButton.setFont(font)
        self.alignLButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_2.addWidget(self.alignLButton, 0, 0, 1, 1)

        self.distributeButton = QPushButton(self.alignGroupBox)
        self.distributeButton.setObjectName(u"distributeButton")
        sizePolicy1.setHeightForWidth(self.distributeButton.sizePolicy().hasHeightForWidth())
        self.distributeButton.setSizePolicy(sizePolicy1)
        self.distributeButton.setMinimumSize(QSize(45, 45))
        self.distributeButton.setMaximumSize(QSize(45, 45))
        font1 = QFont()
        font1.setFamilies([u"\u30e1\u30a4\u30ea\u30aa"])
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setItalic(False)
        self.distributeButton.setFont(font1)
        self.distributeButton.setStyleSheet(u"font:16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_2.addWidget(self.distributeButton, 0, 3, 1, 1)

        self.alignCButton = QPushButton(self.alignGroupBox)
        self.alignCButton.setObjectName(u"alignCButton")
        sizePolicy1.setHeightForWidth(self.alignCButton.sizePolicy().hasHeightForWidth())
        self.alignCButton.setSizePolicy(sizePolicy1)
        self.alignCButton.setMinimumSize(QSize(45, 45))
        self.alignCButton.setMaximumSize(QSize(45, 45))
        self.alignCButton.setFont(font1)
        self.alignCButton.setStyleSheet(u"font: 16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_2.addWidget(self.alignCButton, 0, 1, 1, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout_2)

        self.horizontalSpacer_2 = QSpacerItem(51, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.alignGroupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(280, 0))
        self.groupBox_2.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(self.groupBox_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.currentFrameRadioButton = QRadioButton(self.groupBox)
        self.currentFrameRadioButton.setObjectName(u"currentFrameRadioButton")
        self.currentFrameRadioButton.setChecked(True)

        self.horizontalLayout_5.addWidget(self.currentFrameRadioButton)

        self.keyFrameRadioButton = QRadioButton(self.groupBox)
        self.keyFrameRadioButton.setObjectName(u"keyFrameRadioButton")

        self.horizontalLayout_5.addWidget(self.keyFrameRadioButton)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_13)


        self.verticalLayout_4.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_6.addWidget(self.label_9)

        self.keyFrameIndexSpinBox = QSpinBox(self.groupBox)
        self.keyFrameIndexSpinBox.setObjectName(u"keyFrameIndexSpinBox")
        self.keyFrameIndexSpinBox.setMinimumSize(QSize(80, 0))
        self.keyFrameIndexSpinBox.setMinimum(1)
        self.keyFrameIndexSpinBox.setMaximum(999)

        self.horizontalLayout_6.addWidget(self.keyFrameIndexSpinBox)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_14)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.groupBox)

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

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.valueLineEdit = QLineEdit(self.groupBox_2)
        self.valueLineEdit.setObjectName(u"valueLineEdit")

        self.gridLayout.addWidget(self.valueLineEdit, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_5, 0, 2, 1, 1)

        self.setButton = QPushButton(self.groupBox_2)
        self.setButton.setObjectName(u"setButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.setButton.sizePolicy().hasHeightForWidth())
        self.setButton.setSizePolicy(sizePolicy2)
        self.setButton.setMinimumSize(QSize(60, 56))
        self.setButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.setButton, 0, 3, 2, 1)

        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.stepLineEdit = QLineEdit(self.groupBox_2)
        self.stepLineEdit.setObjectName(u"stepLineEdit")

        self.gridLayout.addWidget(self.stepLineEdit, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 13, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 2, 0, 1, 1)

        self.label_5 = QLabel(self.groupBox_2)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.infLineEdit = QLineEdit(self.groupBox_2)
        self.infLineEdit.setObjectName(u"infLineEdit")

        self.gridLayout.addWidget(self.infLineEdit, 3, 1, 1, 1)

        self.horizontalSpacer_9 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_9, 3, 2, 1, 1)

        self.randomButton = QPushButton(self.groupBox_2)
        self.randomButton.setObjectName(u"randomButton")
        sizePolicy2.setHeightForWidth(self.randomButton.sizePolicy().hasHeightForWidth())
        self.randomButton.setSizePolicy(sizePolicy2)
        self.randomButton.setMinimumSize(QSize(60, 56))
        self.randomButton.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.randomButton, 3, 3, 2, 1)

        self.label_6 = QLabel(self.groupBox_2)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.supLineEdit = QLineEdit(self.groupBox_2)
        self.supLineEdit.setObjectName(u"supLineEdit")

        self.gridLayout.addWidget(self.supLineEdit, 4, 1, 1, 1)

        self.horizontalSpacer_10 = QSpacerItem(13, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_10, 4, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sourceButton = QPushButton(self.centralwidget)
        self.sourceButton.setObjectName(u"sourceButton")
        self.sourceButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.sourceButton)

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
        QWidget.setTabOrder(self.alignLButton, self.alignCButton)
        QWidget.setTabOrder(self.alignCButton, self.alignRButton)
        QWidget.setTabOrder(self.alignRButton, self.distributeButton)
        QWidget.setTabOrder(self.distributeButton, self.absoluteRadioButton)
        QWidget.setTabOrder(self.absoluteRadioButton, self.relativeRadioButton)
        QWidget.setTabOrder(self.relativeRadioButton, self.valueLineEdit)
        QWidget.setTabOrder(self.valueLineEdit, self.stepLineEdit)
        QWidget.setTabOrder(self.stepLineEdit, self.setButton)
        QWidget.setTabOrder(self.setButton, self.infLineEdit)
        QWidget.setTabOrder(self.infLineEdit, self.supLineEdit)
        QWidget.setTabOrder(self.supLineEdit, self.randomButton)
        QWidget.setTabOrder(self.randomButton, self.minimizeButton)
        QWidget.setTabOrder(self.minimizeButton, self.closeButton)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tool", None))
        self.loadButton.setText(QCoreApplication.translate("MainWindow", u"Load", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Modifier", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Oder", None))
        self.l2rRadioButton.setText(QCoreApplication.translate("MainWindow", u"LtoR", None))
        self.r2lRadioButton.setText(QCoreApplication.translate("MainWindow", u"RtoL", None))
        self.randomRadioButton.setText(QCoreApplication.translate("MainWindow", u"random", None))
        self.alignGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Align", None))
        self.alignRButton.setText(QCoreApplication.translate("MainWindow", u"\u21e5", None))
        self.alignLButton.setText(QCoreApplication.translate("MainWindow", u"\u21e4", None))
        self.distributeButton.setText(QCoreApplication.translate("MainWindow", u"|||", None))
        self.alignCButton.setText(QCoreApplication.translate("MainWindow", u"\u2503", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Input", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Target Frame", None))
        self.currentFrameRadioButton.setText(QCoreApplication.translate("MainWindow", u"Current Frame", None))
        self.keyFrameRadioButton.setText(QCoreApplication.translate("MainWindow", u"Key Frame", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Key Frame Index: ", None))
        self.absoluteRadioButton.setText(QCoreApplication.translate("MainWindow", u"Absolute", None))
        self.relativeRadioButton.setText(QCoreApplication.translate("MainWindow", u"Relative", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Value", None))
        self.setButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"inf", None))
        self.randomButton.setText(QCoreApplication.translate("MainWindow", u"Random", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"sup", None))
        self.sourceButton.setText(QCoreApplication.translate("MainWindow", u"source", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


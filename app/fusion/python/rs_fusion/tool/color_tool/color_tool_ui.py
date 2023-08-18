# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'color_tool.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

from rs_fusion.tool.color_tool.color_table import View

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(566, 757)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableView = View(self.centralwidget)
        self.tableView.setObjectName(u"tableView")
        self.tableView.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)

        self.verticalLayout_2.addWidget(self.tableView)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.colormindDefButton = QPushButton(self.groupBox)
        self.colormindDefButton.setObjectName(u"colormindDefButton")
        self.colormindDefButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.colormindDefButton)

        self.colormindUiButton = QPushButton(self.groupBox)
        self.colormindUiButton.setObjectName(u"colormindUiButton")
        self.colormindUiButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.colormindUiButton)

        self.useSelectionCheckBox = QCheckBox(self.groupBox)
        self.useSelectionCheckBox.setObjectName(u"useSelectionCheckBox")

        self.horizontalLayout.addWidget(self.useSelectionCheckBox)

        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.openUrlButton = QPushButton(self.groupBox)
        self.openUrlButton.setObjectName(u"openUrlButton")
        self.openUrlButton.setMinimumSize(QSize(0, 30))

        self.horizontalLayout.addWidget(self.openUrlButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_5.addWidget(self.groupBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.l2rRadioButton = QRadioButton(self.groupBox_3)
        self.l2rRadioButton.setObjectName(u"l2rRadioButton")
        self.l2rRadioButton.setChecked(True)

        self.horizontalLayout_3.addWidget(self.l2rRadioButton)

        self.randomRadioButton = QRadioButton(self.groupBox_3)
        self.randomRadioButton.setObjectName(u"randomRadioButton")

        self.horizontalLayout_3.addWidget(self.randomRadioButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.groupBox_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.currentRowButton = QPushButton(self.centralwidget)
        self.currentRowButton.setObjectName(u"currentRowButton")
        self.currentRowButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_4.addWidget(self.currentRowButton)

        self.selectedButton = QPushButton(self.centralwidget)
        self.selectedButton.setObjectName(u"selectedButton")
        self.selectedButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_4.addWidget(self.selectedButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(30, 30))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout_4.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.closeButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 566, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Colormind", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Add:", None))
        self.colormindDefButton.setText(QCoreApplication.translate("MainWindow", u"model: default", None))
        self.colormindUiButton.setText(QCoreApplication.translate("MainWindow", u"model: ui", None))
        self.useSelectionCheckBox.setText(QCoreApplication.translate("MainWindow", u"use selection", None))
        self.openUrlButton.setText(QCoreApplication.translate("MainWindow", u"website", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Oder", None))
        self.l2rRadioButton.setText(QCoreApplication.translate("MainWindow", u"LtoR", None))
        self.randomRadioButton.setText(QCoreApplication.translate("MainWindow", u"random", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Apply:", None))
        self.currentRowButton.setText(QCoreApplication.translate("MainWindow", u"current row", None))
        self.selectedButton.setText(QCoreApplication.translate("MainWindow", u"selected", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


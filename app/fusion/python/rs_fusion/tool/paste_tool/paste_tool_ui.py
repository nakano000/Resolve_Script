# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\paste_tool\paste_tool.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\paste_tool\paste_tool.ui' applies.
#
# Created: Thu Apr  6 00:21:11 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(308, 356)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.nodeButton = QtWidgets.QPushButton(self.groupBox)
        self.nodeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.nodeButton.setObjectName("nodeButton")
        self.horizontalLayout_2.addWidget(self.nodeButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.saveButton = QtWidgets.QPushButton(self.groupBox)
        self.saveButton.setMinimumSize(QtCore.QSize(80, 30))
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.loadButton = QtWidgets.QPushButton(self.groupBox)
        self.loadButton.setMinimumSize(QtCore.QSize(80, 30))
        self.loadButton.setObjectName("loadButton")
        self.horizontalLayout_2.addWidget(self.loadButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.useRefreshCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.useRefreshCheckBox.setObjectName("useRefreshCheckBox")
        self.verticalLayout_2.addWidget(self.useRefreshCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pasteButton = QtWidgets.QPushButton(self.centralwidget)
        self.pasteButton.setMinimumSize(QtCore.QSize(80, 30))
        self.pasteButton.setObjectName("pasteButton")
        self.horizontalLayout.addWidget(self.pasteButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.minimizeButton = QtWidgets.QToolButton(self.centralwidget)
        self.minimizeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.minimizeButton.setArrowType(QtCore.Qt.DownArrow)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "exclusion", None, -1))
        self.nodeButton.setText(QtWidgets.QApplication.translate("MainWindow", "node", None, -1))
        self.saveButton.setText(QtWidgets.QApplication.translate("MainWindow", "save", None, -1))
        self.loadButton.setText(QtWidgets.QApplication.translate("MainWindow", "load", None, -1))
        self.useRefreshCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "refresh", None, -1))
        self.pasteButton.setText(QtWidgets.QApplication.translate("MainWindow", "paste", None, -1))
        self.minimizeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "最小化", None, -1))
        self.minimizeButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.closeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


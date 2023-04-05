# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\paste_tool\node_window.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\paste_tool\node_window.ui' applies.
#
# Created: Thu Apr  6 00:24:58 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(278, 272)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.readButton = QtWidgets.QPushButton(self.centralwidget)
        self.readButton.setMinimumSize(QtCore.QSize(80, 30))
        self.readButton.setObjectName("readButton")
        self.horizontalLayout.addWidget(self.readButton)
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setMinimumSize(QtCore.QSize(80, 30))
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.readButton.setText(QtWidgets.QApplication.translate("MainWindow", "read", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("MainWindow", "add", None, -1))
        self.closeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


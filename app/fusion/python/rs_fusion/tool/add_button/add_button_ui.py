# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\add_button\add_button.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\add_button\add_button.ui' applies.
#
# Created: Wed Nov  9 11:32:49 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(295, 132)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.refreshCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.refreshCheckBox.setObjectName("refreshCheckBox")
        self.verticalLayout.addWidget(self.refreshCheckBox)
        self.loadCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.loadCheckBox.setObjectName("loadCheckBox")
        self.verticalLayout.addWidget(self.loadCheckBox)
        self.saveCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.saveCheckBox.setObjectName("saveCheckBox")
        self.verticalLayout.addWidget(self.saveCheckBox)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setMinimumSize(QtCore.QSize(100, 40))
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 40))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.refreshCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "Refresh:立ち絵用、リフレッシュボタンの追加", None, -1))
        self.loadCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "LoadSettings:ノードの読み込み用のボタンを追加", None, -1))
        self.saveCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "SaveSettings:ノードの保存用のボタンを追加", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("MainWindow", "追加", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


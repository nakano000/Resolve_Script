# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\resolve_launcher\resolve_launcher.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\resolve_launcher\resolve_launcher.ui' applies.
#
# Created: Fri Jul  8 14:59:02 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(674, 133)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.resolveLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.resolveLineEdit.setObjectName("resolveLineEdit")
        self.gridLayout.addWidget(self.resolveLineEdit, 0, 1, 1, 1)
        self.resolveToolButton = QtWidgets.QToolButton(self.centralwidget)
        self.resolveToolButton.setObjectName("resolveToolButton")
        self.gridLayout.addWidget(self.resolveToolButton, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.fusionLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.fusionLineEdit.setObjectName("fusionLineEdit")
        self.gridLayout.addWidget(self.fusionLineEdit, 1, 1, 1, 1)
        self.fusionToolButton = QtWidgets.QToolButton(self.centralwidget)
        self.fusionToolButton.setObjectName("fusionToolButton")
        self.gridLayout.addWidget(self.fusionToolButton, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(653, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.resolveButton = QtWidgets.QPushButton(self.centralwidget)
        self.resolveButton.setMinimumSize(QtCore.QSize(100, 40))
        self.resolveButton.setObjectName("resolveButton")
        self.horizontalLayout.addWidget(self.resolveButton)
        self.fusionButton = QtWidgets.QPushButton(self.centralwidget)
        self.fusionButton.setMinimumSize(QtCore.QSize(100, 40))
        self.fusionButton.setObjectName("fusionButton")
        self.horizontalLayout.addWidget(self.fusionButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
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
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Resolve", None, -1))
        self.resolveToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Fusion", None, -1))
        self.fusionToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.resolveButton.setText(QtWidgets.QApplication.translate("MainWindow", "Resolve", None, -1))
        self.fusionButton.setText(QtWidgets.QApplication.translate("MainWindow", "Fusion", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


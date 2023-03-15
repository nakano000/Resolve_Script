# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\gui\lang\lang.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\gui\lang\lang.ui' applies.
#
# Created: Wed Mar 15 14:57:35 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(192, 78)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.UseEnBox = QtWidgets.QCheckBox(self.centralwidget)
        self.UseEnBox.setObjectName("UseEnBox")
        self.verticalLayout.addWidget(self.UseEnBox)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.setButton = QtWidgets.QPushButton(self.centralwidget)
        self.setButton.setMinimumSize(QtCore.QSize(80, 30))
        self.setButton.setObjectName("setButton")
        self.horizontalLayout.addWidget(self.setButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(80, 30))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.UseEnBox.setText(QtWidgets.QApplication.translate("MainWindow", "Use English(WIP)", None, -1))
        self.setButton.setText(QtWidgets.QApplication.translate("MainWindow", "set", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("MainWindow", "cancel", None, -1))


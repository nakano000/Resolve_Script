# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\path_mapper\path_mapper.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\path_mapper\path_mapper.ui' applies.
#
# Created: Mon Mar 13 22:57:57 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(98, 120)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setMinimumSize(QtCore.QSize(80, 30))
        self.applyButton.setObjectName("applyButton")
        self.verticalLayout.addWidget(self.applyButton)
        self.removeButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.removeButton.setObjectName("removeButton")
        self.verticalLayout.addWidget(self.removeButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.verticalLayout.addWidget(self.closeButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionauto = QtWidgets.QAction(MainWindow)
        self.actionauto.setCheckable(True)
        self.actionauto.setObjectName("actionauto")
        self.actionja = QtWidgets.QAction(MainWindow)
        self.actionja.setCheckable(True)
        self.actionja.setObjectName("actionja")
        self.actionen = QtWidgets.QAction(MainWindow)
        self.actionen.setCheckable(True)
        self.actionen.setObjectName("actionen")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.applyButton.setText(QtWidgets.QApplication.translate("MainWindow", "適用", None, -1))
        self.removeButton.setText(QtWidgets.QApplication.translate("MainWindow", "取り除く", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))
        self.actionauto.setText(QtWidgets.QApplication.translate("MainWindow", "auto", None, -1))
        self.actionja.setText(QtWidgets.QApplication.translate("MainWindow", "ja", None, -1))
        self.actionen.setText(QtWidgets.QApplication.translate("MainWindow", "en", None, -1))


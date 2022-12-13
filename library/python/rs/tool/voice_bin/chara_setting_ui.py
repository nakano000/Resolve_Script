# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\voice_bin\chara_setting.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\voice_bin\chara_setting.ui' applies.
#
# Created: Tue Dec 13 18:27:35 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(470, 463)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableView = View(self.centralwidget)
        self.tableView.setWordWrap(False)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(150)
        self.verticalLayout.addWidget(self.tableView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setMinimumSize(QtCore.QSize(100, 40))
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.setButton = QtWidgets.QPushButton(self.centralwidget)
        self.setButton.setMinimumSize(QtCore.QSize(100, 40))
        self.setButton.setObjectName("setButton")
        self.horizontalLayout.addWidget(self.setButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(100, 40))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 470, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionUp = QtWidgets.QAction(MainWindow)
        self.actionUp.setObjectName("actionUp")
        self.actionDown = QtWidgets.QAction(MainWindow)
        self.actionDown.setObjectName("actionDown")
        self.actionDelete = QtWidgets.QAction(MainWindow)
        self.actionDelete.setObjectName("actionDelete")
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionUp)
        self.menuEdit.addAction(self.actionDown)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionDelete)
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "※出力済みの音声に適応するには、スクリプトのRebuildが必要です。", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("MainWindow", "add", None, -1))
        self.setButton.setText(QtWidgets.QApplication.translate("MainWindow", "set", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("MainWindow", "cancel", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("MainWindow", "Edit", None, -1))
        self.actionCopy.setText(QtWidgets.QApplication.translate("MainWindow", "Copy", None, -1))
        self.actionCopy.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+C", None, -1))
        self.actionPaste.setText(QtWidgets.QApplication.translate("MainWindow", "Paste", None, -1))
        self.actionPaste.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+V", None, -1))
        self.actionUp.setText(QtWidgets.QApplication.translate("MainWindow", "Up", None, -1))
        self.actionUp.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+Up", None, -1))
        self.actionDown.setText(QtWidgets.QApplication.translate("MainWindow", "Down", None, -1))
        self.actionDown.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Alt+Down", None, -1))
        self.actionDelete.setText(QtWidgets.QApplication.translate("MainWindow", "Delete", None, -1))
        self.actionDelete.setShortcut(QtWidgets.QApplication.translate("MainWindow", "Ctrl+Del", None, -1))

from rs.gui.basic_table import View

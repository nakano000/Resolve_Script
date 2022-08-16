# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\resolve_launcher\resolve_launcher.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\resolve_launcher\resolve_launcher.ui' applies.
#
# Created: Tue Aug 16 17:41:46 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(684, 282)
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
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout.addWidget(self.checkBox)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(653, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.dragButton = DragButton(self.centralwidget)
        self.dragButton.setMinimumSize(QtCore.QSize(100, 100))
        self.dragButton.setObjectName("dragButton")
        self.horizontalLayout_2.addWidget(self.dragButton)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setMaximumSize(QtCore.QSize(16777215, 100))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.horizontalLayout_2.addWidget(self.plainTextEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.resolveButton = QtWidgets.QPushButton(self.centralwidget)
        self.resolveButton.setMinimumSize(QtCore.QSize(100, 40))
        self.resolveButton.setObjectName("resolveButton")
        self.horizontalLayout.addWidget(self.resolveButton)
        self.fusionButton = QtWidgets.QPushButton(self.centralwidget)
        self.fusionButton.setMinimumSize(QtCore.QSize(100, 40))
        self.fusionButton.setObjectName("fusionButton")
        self.horizontalLayout.addWidget(self.fusionButton)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
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
        self.checkBox.setText(QtWidgets.QApplication.translate("MainWindow", "DaVinciResolve または Fusion 起動時に自動で閉じる", None, -1))
        self.dragButton.setText(QtWidgets.QApplication.translate("MainWindow", "設定", None, -1))
        self.plainTextEdit.setPlainText(QtWidgets.QApplication.translate("MainWindow", "初回起動時、またはスクリプトがメニューに表示されない場合\n"
"左の設定ボタンをDaVinci Resolveのコンソールへドラッグアンドドロップしてください。\n"
"Path MapのUserPaths:へ$(RS_FUSION_USER_PATH)を追加します。", None, -1))
        self.resolveButton.setText(QtWidgets.QApplication.translate("MainWindow", "Resolve", None, -1))
        self.fusionButton.setText(QtWidgets.QApplication.translate("MainWindow", "Fusion", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))

from rs.tool.resolve_launcher.drag_button import DragButton

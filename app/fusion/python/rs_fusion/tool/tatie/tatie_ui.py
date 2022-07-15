# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\tatie\tatie.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\tatie\tatie.ui' applies.
#
# Created: Fri Jul 15 20:38:34 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(354, 218)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.multiplyCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.multiplyCheckBox.setObjectName("multiplyCheckBox")
        self.verticalLayout.addWidget(self.multiplyCheckBox)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.cbGroupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.cbGroupBox.setCheckable(True)
        self.cbGroupBox.setObjectName("cbGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.cbGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.cbGroupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.cbNameLineEdit = QtWidgets.QLineEdit(self.cbGroupBox)
        self.cbNameLineEdit.setObjectName("cbNameLineEdit")
        self.horizontalLayout_3.addWidget(self.cbNameLineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addWidget(self.cbGroupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 2, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.loaderButton = QtWidgets.QPushButton(self.centralwidget)
        self.loaderButton.setMinimumSize(QtCore.QSize(100, 40))
        self.loaderButton.setObjectName("loaderButton")
        self.horizontalLayout_2.addWidget(self.loaderButton)
        self.margeButton = QtWidgets.QPushButton(self.centralwidget)
        self.margeButton.setMinimumSize(QtCore.QSize(100, 40))
        self.margeButton.setObjectName("margeButton")
        self.horizontalLayout_2.addWidget(self.margeButton)
        spacerItem3 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 40))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_2.addWidget(self.closeButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "静止画読み込み(Loader)", None, -1))
        self.multiplyCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "Post-Multiply by Alpha", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", " マージ", None, -1))
        self.cbGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "コンボボックスを使用", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "コンボボックス名", None, -1))
        self.loaderButton.setText(QtWidgets.QApplication.translate("MainWindow", "読み込み", None, -1))
        self.margeButton.setText(QtWidgets.QApplication.translate("MainWindow", "マージ", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


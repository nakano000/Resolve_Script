# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\tool\text_plus2srt\text_plus2srt.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\tool\text_plus2srt\text_plus2srt.ui' applies.
#
# Created: Thu Jul 13 08:28:38 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(244, 94)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.videoComboBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoComboBox.sizePolicy().hasHeightForWidth())
        self.videoComboBox.setSizePolicy(sizePolicy)
        self.videoComboBox.setObjectName("videoComboBox")
        self.horizontalLayout_2.addWidget(self.videoComboBox)
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setMinimumSize(QtCore.QSize(50, 30))
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_2.addWidget(self.updateButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setMinimumSize(QtCore.QSize(50, 30))
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(50, 30))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Video Track", None, -1))
        self.updateButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "トラック更新", None, -1))
        self.updateButton.setText(QtWidgets.QApplication.translate("MainWindow", "update", None, -1))
        self.saveButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "トラック更新", None, -1))
        self.saveButton.setText(QtWidgets.QApplication.translate("MainWindow", "save", None, -1))
        self.closeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


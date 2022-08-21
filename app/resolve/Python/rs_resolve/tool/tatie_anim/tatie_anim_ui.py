# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\tool\tatie_anim\tatie_anim.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\tool\tatie_anim\tatie_anim.ui' applies.
#
# Created: Sat Aug 20 18:26:11 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(236, 233)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(30, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.videoIndexListView = QtWidgets.QListView(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoIndexListView.sizePolicy().hasHeightForWidth())
        self.videoIndexListView.setSizePolicy(sizePolicy)
        self.videoIndexListView.setMinimumSize(QtCore.QSize(0, 0))
        self.videoIndexListView.setBaseSize(QtCore.QSize(0, 0))
        self.videoIndexListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.videoIndexListView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.videoIndexListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.videoIndexListView.setObjectName("videoIndexListView")
        self.verticalLayout_2.addWidget(self.videoIndexListView)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.copyButton = QtWidgets.QPushButton(self.groupBox)
        self.copyButton.setMinimumSize(QtCore.QSize(100, 40))
        self.copyButton.setObjectName("copyButton")
        self.verticalLayout.addWidget(self.copyButton)
        self.refreshButton = QtWidgets.QPushButton(self.groupBox)
        self.refreshButton.setMinimumSize(QtCore.QSize(100, 40))
        self.refreshButton.setObjectName("refreshButton")
        self.verticalLayout.addWidget(self.refreshButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.minimizeButton = QtWidgets.QToolButton(self.centralwidget)
        self.minimizeButton.setMinimumSize(QtCore.QSize(40, 40))
        self.minimizeButton.setArrowType(QtCore.Qt.DownArrow)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 40))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "index", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "コマンド", None, -1))
        self.copyButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.copyButton.setText(QtWidgets.QApplication.translate("MainWindow", "copy", None, -1))
        self.refreshButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.refreshButton.setText(QtWidgets.QApplication.translate("MainWindow", "refresh", None, -1))
        self.minimizeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "最小化", None, -1))
        self.minimizeButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.closeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


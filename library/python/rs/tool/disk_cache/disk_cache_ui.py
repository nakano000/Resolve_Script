# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\disk_cache\disk_cache.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\disk_cache\disk_cache.ui' applies.
#
# Created: Wed Jul  6 03:02:59 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(226, 387)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cacheDragButton = DragButton(self.centralwidget)
        self.cacheDragButton.setMinimumSize(QtCore.QSize(100, 100))
        self.cacheDragButton.setObjectName("cacheDragButton")
        self.horizontalLayout_2.addWidget(self.cacheDragButton)
        spacerItem = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.clearDragButton = DragButton(self.centralwidget)
        self.clearDragButton.setMinimumSize(QtCore.QSize(100, 100))
        self.clearDragButton.setObjectName("clearDragButton")
        self.horizontalLayout_2.addWidget(self.clearDragButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.markerListView = QtWidgets.QListView(self.groupBox)
        self.markerListView.setBaseSize(QtCore.QSize(0, 0))
        self.markerListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.markerListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.markerListView.setObjectName("markerListView")
        self.verticalLayout.addWidget(self.markerListView)
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.videoIndexListView = QtWidgets.QListView(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoIndexListView.sizePolicy().hasHeightForWidth())
        self.videoIndexListView.setSizePolicy(sizePolicy)
        self.videoIndexListView.setBaseSize(QtCore.QSize(0, 0))
        self.videoIndexListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.videoIndexListView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.videoIndexListView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.videoIndexListView.setObjectName("videoIndexListView")
        self.verticalLayout_2.addWidget(self.videoIndexListView)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.cacheDragButton.setText(QtWidgets.QApplication.translate("MainWindow", " cache", None, -1))
        self.clearDragButton.setText(QtWidgets.QApplication.translate("MainWindow", " clear", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "marker", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "index", None, -1))

from rs.tool.disk_cache.drag_button import DragButton

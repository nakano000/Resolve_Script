# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\font_tool\font_tool.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\font_tool\font_tool.ui' applies.
#
# Created: Tue Apr  4 10:18:45 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(405, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.sampleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.sampleLineEdit.setObjectName("sampleLineEdit")
        self.horizontalLayout_2.addWidget(self.sampleLineEdit)
        self.readButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readButton.sizePolicy().hasHeightForWidth())
        self.readButton.setSizePolicy(sizePolicy)
        self.readButton.setMinimumSize(QtCore.QSize(40, 20))
        self.readButton.setObjectName("readButton")
        self.horizontalLayout_2.addWidget(self.readButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.autoCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.autoCheckBox.setObjectName("autoCheckBox")
        self.verticalLayout.addWidget(self.autoCheckBox)
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setExpandsOnDoubleClick(False)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.applyButton = QtWidgets.QPushButton(self.centralwidget)
        self.applyButton.setMinimumSize(QtCore.QSize(80, 30))
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout.addWidget(self.applyButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.favoritesButton = QtWidgets.QPushButton(self.centralwidget)
        self.favoritesButton.setMinimumSize(QtCore.QSize(80, 30))
        self.favoritesButton.setObjectName("favoritesButton")
        self.horizontalLayout.addWidget(self.favoritesButton)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.minimizeButton = QtWidgets.QToolButton(self.centralwidget)
        self.minimizeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.minimizeButton.setArrowType(QtCore.Qt.DownArrow)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout.addWidget(self.minimizeButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "SampleText", None, -1))
        self.readButton.setText(QtWidgets.QApplication.translate("MainWindow", "read", None, -1))
        self.autoCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "auto apply", None, -1))
        self.applyButton.setText(QtWidgets.QApplication.translate("MainWindow", "apply", None, -1))
        self.favoritesButton.setText(QtWidgets.QApplication.translate("MainWindow", "Favorites", None, -1))
        self.minimizeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "最小化", None, -1))
        self.minimizeButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.closeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


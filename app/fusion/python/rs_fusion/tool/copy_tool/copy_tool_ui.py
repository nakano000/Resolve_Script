# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\copy_tool\copy_tool.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\fusion\python\rs_fusion\tool\copy_tool\copy_tool.ui' applies.
#
# Created: Thu Feb  9 17:03:24 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(314, 452)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.stepLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.stepLineEdit.setObjectName("stepLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.stepLineEdit)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.jitterInfLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.jitterInfLineEdit.setObjectName("jitterInfLineEdit")
        self.horizontalLayout.addWidget(self.jitterInfLineEdit)
        self.jitterSupLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.jitterSupLineEdit.setObjectName("jitterSupLineEdit")
        self.horizontalLayout.addWidget(self.jitterSupLineEdit)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.sourceButton = QtWidgets.QPushButton(self.centralwidget)
        self.sourceButton.setMinimumSize(QtCore.QSize(80, 30))
        self.sourceButton.setObjectName("sourceButton")
        self.horizontalLayout_4.addWidget(self.sourceButton)
        self.setButton = QtWidgets.QPushButton(self.centralwidget)
        self.setButton.setMinimumSize(QtCore.QSize(80, 30))
        self.setButton.setObjectName("setButton")
        self.horizontalLayout_4.addWidget(self.setButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.minimizeButton = QtWidgets.QToolButton(self.centralwidget)
        self.minimizeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.minimizeButton.setArrowType(QtCore.Qt.DownArrow)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout_4.addWidget(self.minimizeButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_4.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "Animation Shift", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Step", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Jitter", None, -1))
        self.sourceButton.setText(QtWidgets.QApplication.translate("MainWindow", "source", None, -1))
        self.setButton.setText(QtWidgets.QApplication.translate("MainWindow", "set", None, -1))
        self.minimizeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "最小化", None, -1))
        self.minimizeButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


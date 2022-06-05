# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\voice_bin\voice_bin.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\voice_bin\voice_bin.ui' applies.
#
# Created: Sun Jun  5 16:31:16 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(495, 598)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeView = QtWidgets.QTreeView(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setMinimumSize(QtCore.QSize(350, 0))
        self.treeView.setDragEnabled(True)
        self.treeView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.folderLineEdit = QtWidgets.QLineEdit(Form)
        self.folderLineEdit.setObjectName("folderLineEdit")
        self.horizontalLayout_2.addWidget(self.folderLineEdit)
        self.folderToolButton = QtWidgets.QToolButton(Form)
        self.folderToolButton.setObjectName("folderToolButton")
        self.horizontalLayout_2.addWidget(self.folderToolButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.closeButton = QtWidgets.QPushButton(Form)
        self.closeButton.setMinimumSize(QtCore.QSize(100, 40))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "声フォルダ: ", None, -1))
        self.folderToolButton.setText(QtWidgets.QApplication.translate("Form", "...", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("Form", "close", None, -1))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\gui\shortcut\shortcut.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\gui\shortcut\shortcut.ui' applies.
#
# Created: Sun Jun 11 07:02:18 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(331, 146)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.deselectAllLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.deselectAllLineEdit.setObjectName("deselectAllLineEdit")
        self.gridLayout.addWidget(self.deselectAllLineEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.razorLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.razorLineEdit.setObjectName("razorLineEdit")
        self.gridLayout.addWidget(self.razorLineEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.activeTimelinePanelLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.activeTimelinePanelLineEdit.setObjectName("activeTimelinePanelLineEdit")
        self.gridLayout.addWidget(self.activeTimelinePanelLineEdit, 2, 1, 1, 1)
        self.razorTestButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.razorTestButton.sizePolicy().hasHeightForWidth())
        self.razorTestButton.setSizePolicy(sizePolicy)
        self.razorTestButton.setMinimumSize(QtCore.QSize(0, 0))
        self.razorTestButton.setObjectName("razorTestButton")
        self.gridLayout.addWidget(self.razorTestButton, 0, 2, 1, 1)
        self.activeTimelinePanelTestButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activeTimelinePanelTestButton.sizePolicy().hasHeightForWidth())
        self.activeTimelinePanelTestButton.setSizePolicy(sizePolicy)
        self.activeTimelinePanelTestButton.setObjectName("activeTimelinePanelTestButton")
        self.gridLayout.addWidget(self.activeTimelinePanelTestButton, 2, 2, 1, 1)
        self.deselectAllTestButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deselectAllTestButton.sizePolicy().hasHeightForWidth())
        self.deselectAllTestButton.setSizePolicy(sizePolicy)
        self.deselectAllTestButton.setObjectName("deselectAllTestButton")
        self.gridLayout.addWidget(self.deselectAllTestButton, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.setButton = QtWidgets.QPushButton(self.centralwidget)
        self.setButton.setMinimumSize(QtCore.QSize(80, 30))
        self.setButton.setObjectName("setButton")
        self.horizontalLayout.addWidget(self.setButton)
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setMinimumSize(QtCore.QSize(80, 30))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Active Panel Selection\n"
"-> Timeline", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Deselect All", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Razor", None, -1))
        self.razorTestButton.setText(QtWidgets.QApplication.translate("MainWindow", "Test", None, -1))
        self.activeTimelinePanelTestButton.setText(QtWidgets.QApplication.translate("MainWindow", "Test", None, -1))
        self.deselectAllTestButton.setText(QtWidgets.QApplication.translate("MainWindow", "Test", None, -1))
        self.setButton.setText(QtWidgets.QApplication.translate("MainWindow", "set", None, -1))
        self.cancelButton.setText(QtWidgets.QApplication.translate("MainWindow", "cancel", None, -1))


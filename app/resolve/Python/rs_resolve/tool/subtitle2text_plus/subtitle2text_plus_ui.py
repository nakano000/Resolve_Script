# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\tool\subtitle2text_plus\subtitle2text_plus.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\app\resolve\Python\rs_resolve\tool\subtitle2text_plus\subtitle2text_plus.ui' applies.
#
# Created: Tue Dec 27 14:06:01 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(210, 140)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.waitTimeSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waitTimeSpinBox.sizePolicy().hasHeightForWidth())
        self.waitTimeSpinBox.setSizePolicy(sizePolicy)
        self.waitTimeSpinBox.setMaximum(999.99)
        self.waitTimeSpinBox.setObjectName("waitTimeSpinBox")
        self.horizontalLayout_3.addWidget(self.waitTimeSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.subtitleComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.subtitleComboBox.setObjectName("subtitleComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.subtitleComboBox)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.videoComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.videoComboBox.setObjectName("videoComboBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.videoComboBox)
        self.horizontalLayout_2.addLayout(self.formLayout)
        self.updateButton = QtWidgets.QPushButton(self.centralwidget)
        self.updateButton.setMinimumSize(QtCore.QSize(50, 30))
        self.updateButton.setObjectName("updateButton")
        self.horizontalLayout_2.addWidget(self.updateButton)
        self.horizontalLayout_2.setStretch(0, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setMinimumSize(QtCore.QSize(50, 30))
        self.convertButton.setObjectName("convertButton")
        self.horizontalLayout.addWidget(self.convertButton)
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
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "待ち時間(秒)", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Subtitle", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Video", None, -1))
        self.updateButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "トラック更新", None, -1))
        self.updateButton.setText(QtWidgets.QApplication.translate("MainWindow", "update", None, -1))
        self.convertButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "トラック更新", None, -1))
        self.convertButton.setText(QtWidgets.QApplication.translate("MainWindow", "convert", None, -1))
        self.closeButton.setToolTip(QtWidgets.QApplication.translate("MainWindow", "閉じる", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\yr\tool\text2wave\softalk2wave\softalk.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\yr\tool\text2wave\softalk2wave\softalk.ui' applies.
#
# Created: Sat Feb  5 18:38:33 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(164, 112)
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.voiceComboBox = QtWidgets.QComboBox(Form)
        self.voiceComboBox.setMaximumSize(QtCore.QSize(120, 16777215))
        self.voiceComboBox.setObjectName("voiceComboBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.voiceComboBox)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.volumeSpinBox = QtWidgets.QSpinBox(Form)
        self.volumeSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.volumeSpinBox.setMaximum(100)
        self.volumeSpinBox.setObjectName("volumeSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.volumeSpinBox)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.speedSpinBox = QtWidgets.QSpinBox(Form)
        self.speedSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.speedSpinBox.setMinimum(1)
        self.speedSpinBox.setMaximum(300)
        self.speedSpinBox.setObjectName("speedSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.speedSpinBox)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.pitchSpinBox = QtWidgets.QSpinBox(Form)
        self.pitchSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pitchSpinBox.setMaximum(300)
        self.pitchSpinBox.setObjectName("pitchSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pitchSpinBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Form", "声", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "音量", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "速度", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "音程", None, -1))


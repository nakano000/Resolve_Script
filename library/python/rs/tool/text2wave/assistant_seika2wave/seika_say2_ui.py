# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\text2wave\assistantseika2wave\seika_say2.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\text2wave\assistantseika2wave\seika_say2.ui' applies.
#
# Created: Sat Feb  5 23:13:40 2022
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(187, 215)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cidLineEdit = QtWidgets.QLineEdit(Form)
        self.cidLineEdit.setObjectName("cidLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cidLineEdit)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.volumeLineEdit = QtWidgets.QLineEdit(Form)
        self.volumeLineEdit.setObjectName("volumeLineEdit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.volumeLineEdit)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.speedLineEdit = QtWidgets.QLineEdit(Form)
        self.speedLineEdit.setObjectName("speedLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.speedLineEdit)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.pitchLineEdit = QtWidgets.QLineEdit(Form)
        self.pitchLineEdit.setObjectName("pitchLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pitchLineEdit)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.alphaLineEdit = QtWidgets.QLineEdit(Form)
        self.alphaLineEdit.setObjectName("alphaLineEdit")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.alphaLineEdit)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.intonationLineEdit = QtWidgets.QLineEdit(Form)
        self.intonationLineEdit.setObjectName("intonationLineEdit")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.intonationLineEdit)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.emotion01LineEdit = QtWidgets.QLineEdit(Form)
        self.emotion01LineEdit.setObjectName("emotion01LineEdit")
        self.horizontalLayout.addWidget(self.emotion01LineEdit)
        self.emotion02LineEdit = QtWidgets.QLineEdit(Form)
        self.emotion02LineEdit.setObjectName("emotion02LineEdit")
        self.horizontalLayout.addWidget(self.emotion02LineEdit)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout.addLayout(self.formLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.templateButton = QtWidgets.QPushButton(Form)
        self.templateButton.setMinimumSize(QtCore.QSize(200, 0))
        self.templateButton.setObjectName("templateButton")
        self.verticalLayout.addWidget(self.templateButton)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Form", "cid", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Form", "volume", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Form", "speed", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Form", "pitch", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Form", "alpha", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Form", "intonation", None, -1))
        self.label_7.setText(QtWidgets.QApplication.translate("Form", "emotion", None, -1))
        self.templateButton.setText(QtWidgets.QApplication.translate("Form", "Template", None, -1))


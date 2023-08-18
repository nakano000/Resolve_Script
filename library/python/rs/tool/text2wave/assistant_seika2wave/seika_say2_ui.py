# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'seika_say2.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(200, 230)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.cidLineEdit = QLineEdit(Form)
        self.cidLineEdit.setObjectName(u"cidLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.cidLineEdit)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.volumeLineEdit = QLineEdit(Form)
        self.volumeLineEdit.setObjectName(u"volumeLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.volumeLineEdit)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.speedLineEdit = QLineEdit(Form)
        self.speedLineEdit.setObjectName(u"speedLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.speedLineEdit)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.pitchLineEdit = QLineEdit(Form)
        self.pitchLineEdit.setObjectName(u"pitchLineEdit")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.pitchLineEdit)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.alphaLineEdit = QLineEdit(Form)
        self.alphaLineEdit.setObjectName(u"alphaLineEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.alphaLineEdit)

        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.intonationLineEdit = QLineEdit(Form)
        self.intonationLineEdit.setObjectName(u"intonationLineEdit")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.intonationLineEdit)

        self.label_7 = QLabel(Form)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.emotion01LineEdit = QLineEdit(Form)
        self.emotion01LineEdit.setObjectName(u"emotion01LineEdit")

        self.horizontalLayout.addWidget(self.emotion01LineEdit)

        self.emotion02LineEdit = QLineEdit(Form)
        self.emotion02LineEdit.setObjectName(u"emotion02LineEdit")

        self.horizontalLayout.addWidget(self.emotion02LineEdit)


        self.formLayout.setLayout(6, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.templateButton = QPushButton(Form)
        self.templateButton.setObjectName(u"templateButton")
        self.templateButton.setMinimumSize(QSize(200, 0))

        self.verticalLayout.addWidget(self.templateButton)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"cid", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"volume", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"speed", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"pitch", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"alpha", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"intonation", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"emotion", None))
        self.templateButton.setText(QCoreApplication.translate("Form", u"Template", None))
    # retranslateUi


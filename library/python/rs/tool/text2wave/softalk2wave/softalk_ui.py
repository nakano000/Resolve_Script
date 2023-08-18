# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'softalk.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QLabel,
    QSizePolicy, QSpinBox, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(164, 112)
        self.formLayout = QFormLayout(Form)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.voiceComboBox = QComboBox(Form)
        self.voiceComboBox.setObjectName(u"voiceComboBox")
        self.voiceComboBox.setMaximumSize(QSize(120, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.voiceComboBox)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.volumeSpinBox = QSpinBox(Form)
        self.volumeSpinBox.setObjectName(u"volumeSpinBox")
        self.volumeSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.volumeSpinBox.setMaximum(100)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.volumeSpinBox)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.speedSpinBox = QSpinBox(Form)
        self.speedSpinBox.setObjectName(u"speedSpinBox")
        self.speedSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.speedSpinBox.setMinimum(1)
        self.speedSpinBox.setMaximum(300)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.speedSpinBox)

        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_5)

        self.pitchSpinBox = QSpinBox(Form)
        self.pitchSpinBox.setObjectName(u"pitchSpinBox")
        self.pitchSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.pitchSpinBox.setMaximum(300)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.pitchSpinBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u58f0", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u97f3\u91cf", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u901f\u5ea6", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u97f3\u7a0b", None))
    # retranslateUi


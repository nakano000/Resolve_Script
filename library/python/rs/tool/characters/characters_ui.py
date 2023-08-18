# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'characters.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(739, 677)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit = QLineEdit(self.tab)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setReadOnly(True)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_2 = QLineEdit(self.tab)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setReadOnly(True)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_2)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_3 = QLineEdit(self.tab)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setReadOnly(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_3)

        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.lineEdit_4 = QLineEdit(self.tab)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        self.lineEdit_4.setReadOnly(True)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.lineEdit_4)

        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.lineEdit_5 = QLineEdit(self.tab)
        self.lineEdit_5.setObjectName(u"lineEdit_5")
        self.lineEdit_5.setReadOnly(True)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.lineEdit_5)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.lineEdit_6 = QLineEdit(self.tab)
        self.lineEdit_6.setObjectName(u"lineEdit_6")
        self.lineEdit_6.setReadOnly(True)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.lineEdit_6)

        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label_7)

        self.lineEdit_7 = QLineEdit(self.tab)
        self.lineEdit_7.setObjectName(u"lineEdit_7")
        self.lineEdit_7.setReadOnly(True)

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.lineEdit_7)

        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_8)

        self.lineEdit_8 = QLineEdit(self.tab)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setReadOnly(True)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.lineEdit_8)

        self.label_30 = QLabel(self.tab)
        self.label_30.setObjectName(u"label_30")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_30)

        self.lineEdit_44 = QLineEdit(self.tab)
        self.lineEdit_44.setObjectName(u"lineEdit_44")
        self.lineEdit_44.setReadOnly(True)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.lineEdit_44)

        self.label_29 = QLabel(self.tab)
        self.label_29.setObjectName(u"label_29")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_29)

        self.lineEdit_33 = QLineEdit(self.tab)
        self.lineEdit_33.setObjectName(u"lineEdit_33")
        self.lineEdit_33.setStyleSheet(u"font: 12pt \"\u30e1\u30a4\u30ea\u30aa\";")
        self.lineEdit_33.setReadOnly(True)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.lineEdit_33)

        self.label_31 = QLabel(self.tab)
        self.label_31.setObjectName(u"label_31")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.label_31)

        self.arrowPlainTextEdit = QPlainTextEdit(self.tab)
        self.arrowPlainTextEdit.setObjectName(u"arrowPlainTextEdit")

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.arrowPlainTextEdit)

        self.label_33 = QLabel(self.tab)
        self.label_33.setObjectName(u"label_33")

        self.formLayout.setWidget(12, QFormLayout.LabelRole, self.label_33)

        self.lineEdit_45 = QLineEdit(self.tab)
        self.lineEdit_45.setObjectName(u"lineEdit_45")
        self.lineEdit_45.setReadOnly(True)

        self.formLayout.setWidget(12, QFormLayout.FieldRole, self.lineEdit_45)

        self.arrowCPlainTextEdit = QPlainTextEdit(self.tab)
        self.arrowCPlainTextEdit.setObjectName(u"arrowCPlainTextEdit")

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.arrowCPlainTextEdit)

        self.label_32 = QLabel(self.tab)
        self.label_32.setObjectName(u"label_32")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.label_32)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 274, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_4 = QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_9 = QLabel(self.tab_2)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_3.addWidget(self.label_9)

        self.plainTextEdit = QPlainTextEdit(self.tab_2)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.plainTextEdit)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_7 = QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lineEdit_17 = QLineEdit(self.groupBox)
        self.lineEdit_17.setObjectName(u"lineEdit_17")
        self.lineEdit_17.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.lineEdit_17)

        self.lineEdit_9 = QLineEdit(self.groupBox)
        self.lineEdit_9.setObjectName(u"lineEdit_9")
        self.lineEdit_9.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.lineEdit_9)

        self.lineEdit_18 = QLineEdit(self.groupBox)
        self.lineEdit_18.setObjectName(u"lineEdit_18")
        self.lineEdit_18.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.lineEdit_18)

        self.lineEdit_10 = QLineEdit(self.groupBox)
        self.lineEdit_10.setObjectName(u"lineEdit_10")
        self.lineEdit_10.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.lineEdit_10)


        self.verticalLayout_7.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lineEdit_19 = QLineEdit(self.groupBox_2)
        self.lineEdit_19.setObjectName(u"lineEdit_19")
        self.lineEdit_19.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.lineEdit_19)

        self.lineEdit_11 = QLineEdit(self.groupBox_2)
        self.lineEdit_11.setObjectName(u"lineEdit_11")
        self.lineEdit_11.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.lineEdit_11)

        self.lineEdit_20 = QLineEdit(self.groupBox_2)
        self.lineEdit_20.setObjectName(u"lineEdit_20")
        self.lineEdit_20.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.lineEdit_20)

        self.lineEdit_12 = QLineEdit(self.groupBox_2)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.lineEdit_12)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.verticalSpacer_2 = QSpacerItem(20, 212, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_8 = QVBoxLayout(self.tab_4)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_10 = QLabel(self.tab_4)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.lineEdit_13 = QLineEdit(self.tab_4)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setAutoFillBackground(True)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.lineEdit_13)

        self.label_11 = QLabel(self.tab_4)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_11)

        self.lineEdit_14 = QLineEdit(self.tab_4)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setAutoFillBackground(True)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.lineEdit_14)

        self.label_12 = QLabel(self.tab_4)
        self.label_12.setObjectName(u"label_12")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_12)

        self.lineEdit_15 = QLineEdit(self.tab_4)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setAutoFillBackground(True)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.lineEdit_15)

        self.label_13 = QLabel(self.tab_4)
        self.label_13.setObjectName(u"label_13")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_13)

        self.lineEdit_16 = QLineEdit(self.tab_4)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setAutoFillBackground(True)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.lineEdit_16)

        self.label_15 = QLabel(self.tab_4)
        self.label_15.setObjectName(u"label_15")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.label_15)

        self.lineEdit_22 = QLineEdit(self.tab_4)
        self.lineEdit_22.setObjectName(u"lineEdit_22")
        self.lineEdit_22.setReadOnly(True)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.lineEdit_22)

        self.label_14 = QLabel(self.tab_4)
        self.label_14.setObjectName(u"label_14")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.label_14)

        self.lineEdit_21 = QLineEdit(self.tab_4)
        self.lineEdit_21.setObjectName(u"lineEdit_21")
        self.lineEdit_21.setReadOnly(True)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.lineEdit_21)

        self.label_16 = QLabel(self.tab_4)
        self.label_16.setObjectName(u"label_16")

        self.formLayout_2.setWidget(6, QFormLayout.LabelRole, self.label_16)

        self.lineEdit_23 = QLineEdit(self.tab_4)
        self.lineEdit_23.setObjectName(u"lineEdit_23")
        self.lineEdit_23.setReadOnly(True)

        self.formLayout_2.setWidget(6, QFormLayout.FieldRole, self.lineEdit_23)

        self.label_20 = QLabel(self.tab_4)
        self.label_20.setObjectName(u"label_20")

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.label_20)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.italy1LineEdit = QLineEdit(self.tab_4)
        self.italy1LineEdit.setObjectName(u"italy1LineEdit")
        self.italy1LineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.italy1LineEdit)

        self.italy2LineEdit = QLineEdit(self.tab_4)
        self.italy2LineEdit.setObjectName(u"italy2LineEdit")
        self.italy2LineEdit.setReadOnly(True)

        self.horizontalLayout.addWidget(self.italy2LineEdit)

        self.horizontalLayout.setStretch(0, 8)
        self.horizontalLayout.setStretch(1, 1)

        self.formLayout_2.setLayout(7, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_21 = QLabel(self.tab_4)
        self.label_21.setObjectName(u"label_21")

        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.label_21)

        self.lycianLineEdit = QLineEdit(self.tab_4)
        self.lycianLineEdit.setObjectName(u"lycianLineEdit")
        self.lycianLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.lycianLineEdit)

        self.label_22 = QLabel(self.tab_4)
        self.label_22.setObjectName(u"label_22")

        self.formLayout_2.setWidget(10, QFormLayout.LabelRole, self.label_22)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.phoenician1LineEdit = QLineEdit(self.tab_4)
        self.phoenician1LineEdit.setObjectName(u"phoenician1LineEdit")
        self.phoenician1LineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.phoenician1LineEdit)

        self.phoenician2LineEdit = QLineEdit(self.tab_4)
        self.phoenician2LineEdit.setObjectName(u"phoenician2LineEdit")
        self.phoenician2LineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.phoenician2LineEdit)

        self.horizontalLayout_2.setStretch(0, 8)
        self.horizontalLayout_2.setStretch(1, 1)

        self.formLayout_2.setLayout(10, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_23 = QLabel(self.tab_4)
        self.label_23.setObjectName(u"label_23")

        self.formLayout_2.setWidget(12, QFormLayout.LabelRole, self.label_23)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.persian1LineEdit = QLineEdit(self.tab_4)
        self.persian1LineEdit.setObjectName(u"persian1LineEdit")
        self.persian1LineEdit.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.persian1LineEdit)

        self.persian2LineEdit = QLineEdit(self.tab_4)
        self.persian2LineEdit.setObjectName(u"persian2LineEdit")
        self.persian2LineEdit.setReadOnly(True)

        self.horizontalLayout_3.addWidget(self.persian2LineEdit)

        self.horizontalLayout_3.setStretch(0, 2)
        self.horizontalLayout_3.setStretch(1, 1)

        self.formLayout_2.setLayout(12, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_24 = QLabel(self.tab_4)
        self.label_24.setObjectName(u"label_24")

        self.formLayout_2.setWidget(11, QFormLayout.LabelRole, self.label_24)

        self.cypriotLineEdit = QLineEdit(self.tab_4)
        self.cypriotLineEdit.setObjectName(u"cypriotLineEdit")
        self.cypriotLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(11, QFormLayout.FieldRole, self.cypriotLineEdit)

        self.label_25 = QLabel(self.tab_4)
        self.label_25.setObjectName(u"label_25")

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.label_25)

        self.gothicLineEdit = QLineEdit(self.tab_4)
        self.gothicLineEdit.setObjectName(u"gothicLineEdit")
        self.gothicLineEdit.setReadOnly(True)

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.gothicLineEdit)


        self.verticalLayout_8.addLayout(self.formLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 282, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.label_17 = QLabel(self.tab_4)
        self.label_17.setObjectName(u"label_17")

        self.verticalLayout_8.addWidget(self.label_17)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_9 = QVBoxLayout(self.tab_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.cuneiform1PlainTextEdit = QPlainTextEdit(self.tab_5)
        self.cuneiform1PlainTextEdit.setObjectName(u"cuneiform1PlainTextEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.cuneiform1PlainTextEdit.sizePolicy().hasHeightForWidth())
        self.cuneiform1PlainTextEdit.setSizePolicy(sizePolicy)
        self.cuneiform1PlainTextEdit.setReadOnly(True)

        self.verticalLayout_9.addWidget(self.cuneiform1PlainTextEdit)

        self.cuneiform2PlainTextEdit = QPlainTextEdit(self.tab_5)
        self.cuneiform2PlainTextEdit.setObjectName(u"cuneiform2PlainTextEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.cuneiform2PlainTextEdit.sizePolicy().hasHeightForWidth())
        self.cuneiform2PlainTextEdit.setSizePolicy(sizePolicy1)
        self.cuneiform2PlainTextEdit.setReadOnly(True)

        self.verticalLayout_9.addWidget(self.cuneiform2PlainTextEdit)

        self.label_18 = QLabel(self.tab_5)
        self.label_18.setObjectName(u"label_18")

        self.verticalLayout_9.addWidget(self.label_18)

        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QWidget()
        self.tab_6.setObjectName(u"tab_6")
        self.verticalLayout_10 = QVBoxLayout(self.tab_6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.hieroglyph1PlainTextEdit = QPlainTextEdit(self.tab_6)
        self.hieroglyph1PlainTextEdit.setObjectName(u"hieroglyph1PlainTextEdit")
        sizePolicy.setHeightForWidth(self.hieroglyph1PlainTextEdit.sizePolicy().hasHeightForWidth())
        self.hieroglyph1PlainTextEdit.setSizePolicy(sizePolicy)
        self.hieroglyph1PlainTextEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.hieroglyph1PlainTextEdit)

        self.hieroglyph2PlainTextEdit = QPlainTextEdit(self.tab_6)
        self.hieroglyph2PlainTextEdit.setObjectName(u"hieroglyph2PlainTextEdit")
        sizePolicy1.setHeightForWidth(self.hieroglyph2PlainTextEdit.sizePolicy().hasHeightForWidth())
        self.hieroglyph2PlainTextEdit.setSizePolicy(sizePolicy1)
        self.hieroglyph2PlainTextEdit.setReadOnly(True)

        self.verticalLayout_10.addWidget(self.hieroglyph2PlainTextEdit)

        self.label_19 = QLabel(self.tab_6)
        self.label_19.setObjectName(u"label_19")

        self.verticalLayout_10.addWidget(self.label_19)

        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QWidget()
        self.tab_7.setObjectName(u"tab_7")
        self.verticalLayout_11 = QVBoxLayout(self.tab_7)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.ma01LineEdit = QLineEdit(self.tab_7)
        self.ma01LineEdit.setObjectName(u"ma01LineEdit")
        self.ma01LineEdit.setReadOnly(True)

        self.verticalLayout_11.addWidget(self.ma01LineEdit)

        self.ma02LineEdit = QLineEdit(self.tab_7)
        self.ma02LineEdit.setObjectName(u"ma02LineEdit")
        self.ma02LineEdit.setReadOnly(True)

        self.verticalLayout_11.addWidget(self.ma02LineEdit)

        self.ma03LineEdit = QLineEdit(self.tab_7)
        self.ma03LineEdit.setObjectName(u"ma03LineEdit")
        self.ma03LineEdit.setReadOnly(True)

        self.verticalLayout_11.addWidget(self.ma03LineEdit)

        self.ma04LineEdit = QLineEdit(self.tab_7)
        self.ma04LineEdit.setObjectName(u"ma04LineEdit")
        self.ma04LineEdit.setReadOnly(True)

        self.verticalLayout_11.addWidget(self.ma04LineEdit)

        self.ma05LineEdit = QLineEdit(self.tab_7)
        self.ma05LineEdit.setObjectName(u"ma05LineEdit")
        self.ma05LineEdit.setReadOnly(True)

        self.verticalLayout_11.addWidget(self.ma05LineEdit)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_11.addItem(self.verticalSpacer_5)

        self.label_26 = QLabel(self.tab_7)
        self.label_26.setObjectName(u"label_26")

        self.verticalLayout_11.addWidget(self.label_26)

        self.tabWidget.addTab(self.tab_7, "")
        self.tab_8 = QWidget()
        self.tab_8.setObjectName(u"tab_8")
        self.verticalLayout_13 = QVBoxLayout(self.tab_8)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.cards01LineEdit = QLineEdit(self.tab_8)
        self.cards01LineEdit.setObjectName(u"cards01LineEdit")
        self.cards01LineEdit.setReadOnly(True)

        self.verticalLayout_13.addWidget(self.cards01LineEdit)

        self.cards02LineEdit = QLineEdit(self.tab_8)
        self.cards02LineEdit.setObjectName(u"cards02LineEdit")
        self.cards02LineEdit.setReadOnly(True)

        self.verticalLayout_13.addWidget(self.cards02LineEdit)

        self.cards03LineEdit = QLineEdit(self.tab_8)
        self.cards03LineEdit.setObjectName(u"cards03LineEdit")
        self.cards03LineEdit.setReadOnly(True)

        self.verticalLayout_13.addWidget(self.cards03LineEdit)

        self.cards04LineEdit = QLineEdit(self.tab_8)
        self.cards04LineEdit.setObjectName(u"cards04LineEdit")
        self.cards04LineEdit.setReadOnly(True)

        self.verticalLayout_13.addWidget(self.cards04LineEdit)

        self.cards05LineEdit = QLineEdit(self.tab_8)
        self.cards05LineEdit.setObjectName(u"cards05LineEdit")
        self.cards05LineEdit.setReadOnly(True)

        self.verticalLayout_13.addWidget(self.cards05LineEdit)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_4)

        self.label_27 = QLabel(self.tab_8)
        self.label_27.setObjectName(u"label_27")

        self.verticalLayout_13.addWidget(self.label_27)

        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QWidget()
        self.tab_9.setObjectName(u"tab_9")
        self.verticalLayout_12 = QVBoxLayout(self.tab_9)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.alchemyPlainTextEdit = QPlainTextEdit(self.tab_9)
        self.alchemyPlainTextEdit.setObjectName(u"alchemyPlainTextEdit")

        self.verticalLayout_12.addWidget(self.alchemyPlainTextEdit)

        self.verticalSpacer_6 = QSpacerItem(20, 197, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_6)

        self.label_28 = QLabel(self.tab_9)
        self.label_28.setObjectName(u"label_28")

        self.verticalLayout_12.addWidget(self.label_28)

        self.tabWidget.addTab(self.tab_9, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u534a\u89d2", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"0123456789", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5168\u89d2", None))
        self.lineEdit_2.setText(QCoreApplication.translate("MainWindow", u"\uff10\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6f22\u6570\u5b57", None))
        self.lineEdit_3.setText(QCoreApplication.translate("MainWindow", u"\u3007\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341\u767e\u5343\u4e07", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5b57", None))
        self.lineEdit_4.setText(QCoreApplication.translate("MainWindow", u"\u96f6\u58f1\u5f10\u53c2\u8086\u4f0d\u9678\u6f06\u634c\u7396\u62fe\u964c\u9621\u842c", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u30ed\u30fc\u30de\u6570\u5b57", None))
        self.lineEdit_5.setText(QCoreApplication.translate("MainWindow", u"\u2160\u2161\u2162\u2163\u2164\u2165\u2166\u2167\u2168\u2169\u216a\u216b", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u4e38\u56f2\u307f\u6570\u5b57", None))
        self.lineEdit_6.setText(QCoreApplication.translate("MainWindow", u"\u24ea\u2460\u2461\u2462\u2463\u2464\u2465\u2466\u2467\u2468\u2469\u246a\u246b\u246c\u246d\u246e\u246f\u2470\u2471\u2472\u2473", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u4e38\u56f2\u307f\u6570\u5b57", None))
        self.lineEdit_7.setText(QCoreApplication.translate("MainWindow", u"\u24ff\u2776\u2777\u2778\u2779\u277a\u277b\u277c\u277d\u277e\u277f\u24eb\u24ec\u24ed\u24ee\u24ef\u24f0\u24f1\u24f2\u24f3\u24f4", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\u4e38\u56f2\u307f\u6f22\u6570\u5b57", None))
        self.lineEdit_8.setText(QCoreApplication.translate("MainWindow", u"\u3280\u3281\u3282\u3283\u3284\u3285\u3286\u3287\u3288\u3289", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"\u534a\u89d2\u8a18\u53f7", None))
        self.lineEdit_44.setText(QCoreApplication.translate("MainWindow", u"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"\u5168\u89d2\u8a18\u53f7", None))
        self.lineEdit_33.setText(QCoreApplication.translate("MainWindow", u"\u3000\u3001\u3002\uff0c\uff0e\u30fb\uff1a\uff1b\uff1f\uff01\u309b\u309c\u00b4\uff40\u00a8\uff3e\uffe3\uff3f\u30fd\u30fe\u309d\u309e\u3003\u4edd\u3005\u3006", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"\u77e2\u5370", None))
        self.arrowPlainTextEdit.setPlainText("")
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"\u56f3\u5f62", None))
        self.lineEdit_45.setText(QCoreApplication.translate("MainWindow", u"\u25b2\u25b6\u25bc\u25c0\u25e4\u25e5\u25e3\u25e2\u25c6 \u25b3\u25b7\u25bd\u25c1\u25f8\u25f9\u25fa\u25ff\u25c7 \u2b12\u25e7\u2b13\u25e8\u25e9\u2b14\u2b15\u25ea\u2b16\u2b17\u2b18\u2b19", None))
        self.arrowCPlainTextEdit.setPlainText("")
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"\u88dc\u52a9\u77e2\u5370C", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u6570\u5b57\u3001\u8a18\u53f7", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u5e38\u7528\u6f22\u5b57", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"\u4e9c\u54c0\u611b\u60aa\u63e1\u5727\u6271\u5b89\u6697\u6848\u4ee5\u4f4d\u4f9d\u5049\u56f2\u59d4\u5a01\u5c09\u610f\u6170\u6613\u70ba\u7570\u79fb\u7dad\u7def\u80c3\u8863\u9055\u907a\u533b\u4e95\u57df\u80b2\u4e00\u58f1\u9038\u7a32\u828b\u5370\u54e1\u56e0\u59fb\u5f15\u98f2\u9662\u9670\u96a0\u97fb\u53f3\u5b87\u7fbd\u96e8\u6e26\u6d66\u904b\u96f2\u55b6\u5f71\u6620\u6804\u6c38\u6cf3\u82f1\u885b\u8a60\u92ed\u6db2\u75ab\u76ca\u99c5\u60a6\u8b01\u8d8a\u95b2\u5186\u5712\u5bb4\u5ef6\u63f4\u6cbf\u6f14\u708e\u7159\u733f\u7e01\u9060\u925b\u5869\u6c5a\u51f9\u592e\u5965\u5f80\u5fdc\u62bc\u6a2a\u6b27\u6bb4\u738b\u7fc1\u9ec4\u6c96\u5104\u5c4b\u61b6\u4e59\u5378\u6069\u6e29\u7a4f\u97f3\u4e0b\u5316\u4eee\u4f55\u4fa1\u4f73\u52a0\u53ef\u590f\u5ac1\u5bb6\u5be1\u79d1\u6687\u679c\u67b6\u6b4c\u6cb3\u706b\u798d\u7a3c\u7b87\u82b1\u8377\u83ef\u83d3\u8ab2\u8ca8\u904e\u868a\u6211\u753b\u82bd\u8cc0\u96c5\u9913\u4ecb\u4f1a\u89e3\u56de\u584a\u58ca\u5feb\u602a\u6094\u61d0\u6212\u62d0\u6539\u68b0\u6d77\u7070\u754c\u7686\u7d75\u958b\u968e\u8c9d\u52be"
                        "\u5916\u5bb3\u6168\u6982\u6daf\u8857\u8a72\u57a3\u5687\u5404\u62e1\u683c\u6838\u6bbb\u7372\u78ba\u7a6b\u899a\u89d2\u8f03\u90ed\u95a3\u9694\u9769\u5b66\u5cb3\u697d\u984d\u639b\u6f5f\u5272\u559d\u62ec\u6d3b\u6e07\u6ed1\u8910\u8f44\u4e14\u682a\u5208\u4e7e\u51a0\u5bd2\u520a\u52d8\u52e7\u5dfb\u559a\u582a\u5b8c\u5b98\u5bdb\u5e72\u5e79\u60a3\u611f\u6163\u61be\u63db\u6562\u68fa\u6b3e\u6b53\u6c57\u6f22\u74b0\u7518\u76e3\u770b\u7ba1\u7c21\u7de9\u7f36\u809d\u8266\u89b3\u8cab\u9084\u9451\u9593\u9591\u95a2\u9665\u9928\u4e38\u542b\u5cb8\u773c\u5ca9\u9811\u9854\u9858\u4f01\u5371\u559c\u5668\u57fa\u5947\u5bc4\u5c90\u5e0c\u5e7e\u5fcc\u63ee\u673a\u65d7\u65e2\u671f\u68cb\u68c4\u6a5f\u5e30\u6c17\u6c7d\u7948\u5b63\u7d00\u898f\u8a18\u8cb4\u8d77\u8ecc\u8f1d\u98e2\u9a0e\u9b3c\u507d\u5100\u5b9c\u622f\u6280\u64ec\u6b3a\u72a0\u7591\u7fa9\u8b70\u83ca\u5409\u55ab\u8a70\u5374\u5ba2\u811a\u8650\u9006\u4e18\u4e45\u4f11\u53ca\u5438\u5bae\u5f13\u6025\u6551\u673d\u6c42\u6ce3\u7403\u7a76\u7aae\u7d1a\u7cfe\u7d66\u65e7\u725b\u53bb\u5c45\u5de8\u62d2"
                        "\u62e0\u6319\u865a\u8a31\u8ddd\u6f01\u9b5a\u4eab\u4eac\u4f9b\u7af6\u5171\u51f6\u5354\u53eb\u5883\u5ce1\u5f37\u6050\u606d\u631f\u6559\u6a4b\u6cc1\u72c2\u72ed\u77ef\u80f8\u8105\u8208\u90f7\u93e1\u97ff\u9a5a\u4ef0\u51dd\u6681\u696d\u5c40\u66f2\u6975\u7389\u52e4\u5747\u65a4\u7434\u7981\u7b4b\u7dca\u83cc\u895f\u8b39\u8fd1\u91d1\u541f\u9280\u4e5d\u53e5\u533a\u82e6\u99c6\u5177\u611a\u865e\u7a7a\u5076\u9047\u9685\u5c48\u6398\u9774\u7e70\u6851\u52f2\u541b\u85ab\u8a13\u7fa4\u8ecd\u90e1\u4fc2\u50be\u5211\u5144\u5553\u578b\u5951\u5f62\u5f84\u6075\u6176\u61a9\u63b2\u643a\u656c\u666f\u6e13\u7cfb\u7d4c\u7d99\u830e\u86cd\u8a08\u8b66\u8efd\u9d8f\u82b8\u8fce\u9be8\u5287\u6483\u6fc0\u5091\u6b20\u6c7a\u6f54\u7a74\u7d50\u8840\u6708\u4ef6\u5039\u5065\u517c\u5238\u5263\u570f\u5805\u5acc\u5efa\u61b2\u61f8\u691c\u6a29\u72ac\u732e\u7814\u7d79\u770c\u80a9\u898b\u8b19\u8ce2\u8ed2\u9063\u967a\u9855\u9a13\u5143\u539f\u53b3\u5e7b\u5f26\u6e1b\u6e90\u7384\u73fe\u8a00\u9650\u500b\u53e4\u547c\u56fa\u5b64\u5df1\u5eab\u5f27\u6238\u6545\u67af\u6e56"
                        "\u8a87\u96c7\u9867\u9f13\u4e94\u4e92\u5348\u5449\u5a2f\u5f8c\u5fa1\u609f\u7881\u8a9e\u8aa4\u8b77\u4ea4\u4faf\u5019\u5149\u516c\u529f\u52b9\u539a\u53e3\u5411\u540e\u5751\u597d\u5b54\u5b5d\u5de5\u5de7\u5e78\u5e83\u5eb7\u6052\u614c\u6297\u62d8\u63a7\u653b\u66f4\u6821\u69cb\u6c5f\u6d2a\u6e2f\u6e9d\u7532\u7687\u786c\u7a3f\u7d05\u7d5e\u7db1\u8015\u8003\u80af\u822a\u8352\u884c\u8861\u8b1b\u8ca2\u8cfc\u90ca\u9175\u9271\u92fc\u964d\u9805\u9999\u9ad8\u525b\u53f7\u5408\u62f7\u8c6a\u514b\u523b\u544a\u56fd\u7a40\u9177\u9ed2\u7344\u8170\u9aa8\u8fbc\u4eca\u56f0\u58be\u5a5a\u6068\u61c7\u6606\u6839\u6df7\u7d3a\u9b42\u4f50\u5506\u5de6\u5dee\u67fb\u7802\u8a50\u9396\u5ea7\u50b5\u50ac\u518d\u6700\u59bb\u5bb0\u5f69\u624d\u63a1\u683d\u6b73\u6e08\u707d\u7815\u796d\u658e\u7d30\u83dc\u88c1\u8f09\u969b\u5264\u5728\u6750\u7f6a\u8ca1\u5742\u54b2\u5d0e\u4f5c\u524a\u643e\u6628\u7b56\u7d22\u932f\u685c\u518a\u5237\u5bdf\u64ae\u64e6\u672d\u6bba\u96d1\u76bf\u4e09\u5098\u53c2\u5c71\u60e8\u6563\u685f\u7523\u7b97\u8695\u8cdb\u9178\u66ab\u6b8b\u4ed5"
                        "\u4f3a\u4f7f\u523a\u53f8\u53f2\u55e3\u56db\u58eb\u59cb\u59c9\u59ff\u5b50\u5e02\u5e2b\u5fd7\u601d\u6307\u652f\u65bd\u65e8\u679d\u6b62\u6b7b\u6c0f\u7949\u79c1\u7cf8\u7d19\u7d2b\u80a2\u8102\u81f3\u8996\u8a5e\u8a69\u8a66\u8a8c\u8aee\u8cc7\u8cdc\u96cc\u98fc\u6b6f\u4e8b\u4f3c\u4f8d\u5150\u5b57\u5bfa\u6148\u6301\u6642\u6b21\u6ecb\u6cbb\u74bd\u78c1\u793a\u8033\u81ea\u8f9e\u5f0f\u8b58\u8ef8\u4e03\u57f7\u5931\u5ba4\u6e7f\u6f06\u75be\u8cea\u5b9f\u829d\u820e\u5199\u5c04\u6368\u8d66\u659c\u716e\u793e\u8005\u8b1d\u8eca\u906e\u86c7\u90aa\u501f\u52fa\u5c3a\u7235\u914c\u91c8\u82e5\u5bc2\u5f31\u4e3b\u53d6\u5b88\u624b\u6731\u6b8a\u72e9\u73e0\u7a2e\u8da3\u9152\u9996\u5112\u53d7\u5bff\u6388\u6a39\u9700\u56da\u53ce\u5468\u5b97\u5c31\u5dde\u4fee\u6101\u62fe\u79c0\u79cb\u7d42\u7fd2\u81ed\u821f\u8846\u8972\u9031\u916c\u96c6\u919c\u4f4f\u5145\u5341\u5f93\u67d4\u6c41\u6e0b\u7363\u7e26\u91cd\u9283\u53d4\u5bbf\u6dd1\u795d\u7e2e\u7c9b\u587e\u719f\u51fa\u8853\u8ff0\u4fca\u6625\u77ac\u51c6\u5faa\u65ec\u6b89\u6e96\u6f64\u76fe\u7d14\u5de1\u9075"
                        "\u9806\u51e6\u521d\u6240\u6691\u5eb6\u7dd2\u7f72\u66f8\u8af8\u52a9\u53d9\u5973\u5e8f\u5f90\u9664\u50b7\u511f\u52dd\u5320\u5347\u53ec\u5546\u5531\u5968\u5bb5\u5c06\u5c0f\u5c11\u5c1a\u5e8a\u5f70\u627f\u6284\u62db\u638c\u6607\u662d\u6676\u677e\u6cbc\u6d88\u6e09\u713c\u7126\u7167\u75c7\u7701\u785d\u7901\u7965\u79f0\u7ae0\u7b11\u7ca7\u7d39\u8096\u885d\u8a1f\u8a3c\u8a54\u8a73\u8c61\u8cde\u9418\u969c\u4e0a\u4e08\u4e57\u5197\u5270\u57ce\u5834\u58cc\u5b22\u5e38\u60c5\u6761\u6d44\u72b6\u7573\u84b8\u8b72\u91b8\u9320\u5631\u98fe\u690d\u6b96\u7e54\u8077\u8272\u89e6\u98df\u8fb1\u4f38\u4fe1\u4fb5\u5507\u5a20\u5bdd\u5be9\u5fc3\u614e\u632f\u65b0\u68ee\u6d78\u6df1\u7533\u771f\u795e\u7d33\u81e3\u85aa\u89aa\u8a3a\u8eab\u8f9b\u9032\u91dd\u9707\u4eba\u4ec1\u5203\u5c0b\u751a\u5c3d\u8fc5\u9663\u9162\u56f3\u5439\u5782\u5e25\u63a8\u6c34\u708a\u7761\u7c8b\u8870\u9042\u9154\u9318\u968f\u9ac4\u5d07\u6570\u67a2\u636e\u6749\u6f84\u5bf8\u4e16\u702c\u755d\u662f\u5236\u52e2\u59d3\u5f81\u6027\u6210\u653f\u6574\u661f\u6674\u6b63\u6e05\u7272\u751f"
                        "\u76db\u7cbe\u8056\u58f0\u88fd\u897f\u8aa0\u8a93\u8acb\u901d\u9752\u9759\u6589\u7a0e\u96bb\u5e2d\u60dc\u65a5\u6614\u6790\u77f3\u7a4d\u7c4d\u7e3e\u8cac\u8d64\u8de1\u5207\u62d9\u63a5\u6442\u6298\u8a2d\u7a83\u7bc0\u8aac\u96ea\u7d76\u820c\u4ed9\u5148\u5343\u5360\u5ba3\u5c02\u5ddd\u6226\u6247\u6813\u6cc9\u6d45\u6d17\u67d3\u6f5c\u65cb\u7dda\u7e4a\u8239\u85a6\u8df5\u9078\u9077\u92ad\u9291\u9bae\u524d\u5584\u6f38\u7136\u5168\u7985\u7e55\u5851\u63aa\u758e\u790e\u7956\u79df\u7c97\u7d20\u7d44\u8a34\u963b\u50e7\u5275\u53cc\u5009\u55aa\u58ee\u594f\u5c64\u60f3\u635c\u6383\u633f\u64cd\u65e9\u66f9\u5de3\u69fd\u71e5\u4e89\u76f8\u7a93\u7dcf\u8349\u8358\u846c\u85fb\u88c5\u8d70\u9001\u906d\u971c\u9a12\u50cf\u5897\u618e\u81d3\u8535\u8d08\u9020\u4fc3\u5074\u5247\u5373\u606f\u675f\u6e2c\u8db3\u901f\u4fd7\u5c5e\u8cca\u65cf\u7d9a\u5352\u5b58\u5b6b\u5c0a\u640d\u6751\u4ed6\u591a\u592a\u5815\u59a5\u60f0\u6253\u99c4\u4f53\u5bfe\u8010\u5e2f\u5f85\u6020\u614b\u66ff\u6cf0\u6ede\u80ce\u888b\u8cb8\u9000\u902e\u968a\u4ee3\u53f0\u5927\u7b2c\u984c"
                        "\u6edd\u5353\u5b85\u629e\u62d3\u6ca2\u6fef\u8a17\u6fc1\u8afe\u4f46\u9054\u596a\u8131\u68da\u8c37\u4e39\u5358\u5606\u62c5\u63a2\u6de1\u70ad\u77ed\u7aef\u80c6\u8a95\u935b\u56e3\u58c7\u5f3e\u65ad\u6696\u6bb5\u7537\u8ac7\u5024\u77e5\u5730\u6065\u6c60\u75f4\u7a1a\u7f6e\u81f4\u9045\u7bc9\u755c\u7af9\u84c4\u9010\u79e9\u7a92\u8336\u5ae1\u7740\u4e2d\u4ef2\u5b99\u5fe0\u62bd\u663c\u67f1\u6ce8\u866b\u8877\u92f3\u99d0\u8457\u8caf\u4e01\u5146\u5e33\u5e81\u5f14\u5f35\u5f6b\u5fb4\u61f2\u6311\u671d\u6f6e\u753a\u773a\u8074\u8139\u8178\u8abf\u8d85\u8df3\u9577\u9802\u9ce5\u52c5\u76f4\u6715\u6c88\u73cd\u8cc3\u93ae\u9673\u6d25\u589c\u8ffd\u75db\u901a\u585a\u6f2c\u576a\u91e3\u4ead\u4f4e\u505c\u5075\u8c9e\u5448\u5824\u5b9a\u5e1d\u5e95\u5ead\u5ef7\u5f1f\u62b5\u63d0\u7a0b\u7de0\u8247\u8a02\u9013\u90b8\u6ce5\u6458\u6575\u6ef4\u7684\u7b1b\u9069\u54f2\u5fb9\u64a4\u8fed\u9244\u5178\u5929\u5c55\u5e97\u6dfb\u8ee2\u70b9\u4f1d\u6bbf\u7530\u96fb\u5410\u5857\u5f92\u6597\u6e21\u767b\u9014\u90fd\u52aa\u5ea6\u571f\u5974\u6012\u5012\u515a\u51ac\u51cd"
                        "\u5200\u5510\u5854\u5cf6\u60bc\u6295\u642d\u6771\u6843\u68df\u76d7\u6e6f\u706f\u5f53\u75d8\u7b49\u7b54\u7b52\u7cd6\u7d71\u5230\u8a0e\u8b04\u8c46\u8e0f\u9003\u900f\u9676\u982d\u9a30\u95d8\u50cd\u52d5\u540c\u5802\u5c0e\u6d1e\u7ae5\u80f4\u9053\u9285\u5ce0\u533f\u5f97\u5fb3\u7279\u7763\u7be4\u6bd2\u72ec\u8aad\u51f8\u7a81\u5c4a\u5c6f\u8c5a\u66c7\u920d\u5185\u7e04\u5357\u8edf\u96e3\u4e8c\u5c3c\u5f10\u8089\u65e5\u4e73\u5165\u5982\u5c3f\u4efb\u598a\u5fcd\u8a8d\u5be7\u732b\u71b1\u5e74\u5ff5\u71c3\u7c98\u60a9\u6fc3\u7d0d\u80fd\u8133\u8fb2\u628a\u8987\u6ce2\u6d3e\u7834\u5a46\u99ac\u4ff3\u5ec3\u62dd\u6392\u6557\u676f\u80cc\u80ba\u8f29\u914d\u500d\u57f9\u5a92\u6885\u8cb7\u58f2\u8ce0\u966a\u4f2f\u535a\u62cd\u6cca\u767d\u8236\u8584\u8feb\u6f20\u7206\u7e1b\u9ea6\u7bb1\u808c\u7551\u516b\u9262\u767a\u9aea\u4f10\u7f70\u629c\u95a5\u4f34\u5224\u534a\u53cd\u5e06\u642c\u677f\u7248\u72af\u73ed\u7554\u7e41\u822c\u85e9\u8ca9\u7bc4\u7169\u9812\u98ef\u6669\u756a\u76e4\u86ee\u5351\u5426\u5983\u5f7c\u60b2\u6249\u6279\u62ab\u6bd4\u6ccc\u75b2"
                        "\u76ae\u7891\u79d8\u7f77\u80a5\u88ab\u8cbb\u907f\u975e\u98db\u5099\u5c3e\u5fae\u7f8e\u9f3b\u5339\u5fc5\u7b46\u59eb\u767e\u4ff5\u6a19\u6c37\u6f02\u7968\u8868\u8a55\u63cf\u75c5\u79d2\u82d7\u54c1\u6d5c\u8ca7\u8cd3\u983b\u654f\u74f6\u4e0d\u4ed8\u592b\u5a66\u5bcc\u5e03\u5e9c\u6016\u6276\u6577\u666e\u6d6e\u7236\u7b26\u8150\u819a\u8b5c\u8ca0\u8ce6\u8d74\u9644\u4fae\u6b66\u821e\u90e8\u5c01\u98a8\u4f0f\u526f\u5fa9\u5e45\u670d\u798f\u8179\u8907\u8986\u6255\u6cb8\u4ecf\u7269\u5206\u5674\u58b3\u61a4\u596e\u7c89\u7d1b\u96f0\u6587\u805e\u4e19\u4f75\u5175\u5840\u5e63\u5e73\u5f0a\u67c4\u4e26\u9589\u965b\u7c73\u58c1\u7656\u5225\u504f\u5909\u7247\u7de8\u8fba\u8fd4\u904d\u4fbf\u52c9\u5f01\u4fdd\u8217\u6355\u6b69\u88dc\u7a42\u52df\u5893\u6155\u66ae\u6bcd\u7c3f\u5023\u4ff8\u5305\u5831\u5949\u5b9d\u5cf0\u5d29\u62b1\u653e\u65b9\u6cd5\u6ce1\u7832\u7e2b\u80de\u82b3\u8912\u8a2a\u8c4a\u90a6\u98fd\u4e4f\u4ea1\u508d\u5256\u574a\u59a8\u5e3d\u5fd8\u5fd9\u623f\u66b4\u671b\u67d0\u68d2\u5192\u7d21\u80aa\u81a8\u8b00\u8cbf\u9632\u5317\u50d5\u58a8"
                        "\u64b2\u6734\u7267\u6ca1\u5800\u5954\u672c\u7ffb\u51e1\u76c6\u6469\u78e8\u9b54\u9ebb\u57cb\u59b9\u679a\u6bce\u5e55\u819c\u53c8\u62b9\u672b\u7e6d\u4e07\u6162\u6e80\u6f2b\u5473\u672a\u9b45\u5cac\u5bc6\u8108\u5999\u6c11\u7720\u52d9\u5922\u7121\u77db\u9727\u5a7f\u5a18\u540d\u547d\u660e\u76df\u8ff7\u9298\u9cf4\u6ec5\u514d\u7dbf\u9762\u6a21\u8302\u5984\u6bdb\u731b\u76f2\u7db2\u8017\u6728\u9ed9\u76ee\u623b\u554f\u7d0b\u9580\u5301\u591c\u91ce\u77e2\u5384\u5f79\u7d04\u85ac\u8a33\u8e8d\u67f3\u6109\u6cb9\u7652\u8aed\u8f38\u552f\u512a\u52c7\u53cb\u5e7d\u60a0\u6182\u6709\u7336\u7531\u88d5\u8a98\u904a\u90f5\u96c4\u878d\u5915\u4e88\u4f59\u4e0e\u8a89\u9810\u5e7c\u5bb9\u5eb8\u63da\u63fa\u64c1\u66dc\u69d8\u6d0b\u6eb6\u7528\u7aaf\u7f8a\u8449\u8981\u8b21\u8e0a\u967d\u990a\u6291\u6b32\u6d74\u7fcc\u7ffc\u7f85\u88f8\u6765\u983c\u96f7\u7d61\u843d\u916a\u4e71\u5375\u6b04\u6feb\u89a7\u5229\u540f\u5c65\u7406\u75e2\u88cf\u91cc\u96e2\u9678\u5f8b\u7387\u7acb\u7565\u6d41\u7559\u786b\u7c92\u9686\u7adc\u616e\u65c5\u865c\u4e86\u50da\u4e21\u5bee"
                        "\u6599\u6dbc\u731f\u7642\u7ce7\u826f\u91cf\u9675\u9818\u529b\u7dd1\u502b\u5398\u6797\u81e8\u8f2a\u96a3\u5841\u6d99\u7d2f\u985e\u4ee4\u4f8b\u51b7\u52b1\u793c\u9234\u96b7\u96f6\u970a\u9e97\u9f62\u66a6\u6b74\u5217\u52a3\u70c8\u88c2\u5ec9\u604b\u7df4\u9023\u932c\u7089\u8def\u9732\u52b4\u5eca\u6717\u697c\u6d6a\u6f0f\u8001\u90ce\u516d\u9332\u8ad6\u548c\u8a71\u8cc4\u60d1\u67a0\u6e7e\u8155", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u6f22\u5b57", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u3072\u3089\u304c\u306a", None))
        self.lineEdit_17.setText(QCoreApplication.translate("MainWindow", u"\u3042\u3044\u3046\u3048\u304a\u304b\u304d\u304f\u3051\u3053\u3055\u3057\u3059\u305b\u305d\u305f\u3061\u3064\u3066\u3068\u306a\u306b\u306c\u306d\u306e\u306f\u3072\u3075\u3078\u307b\u307e\u307f\u3080\u3081\u3082\u3084\u3086\u3088\u3089\u308a\u308b\u308c\u308d\u308f\u3092\u3093", None))
        self.lineEdit_9.setText(QCoreApplication.translate("MainWindow", u"\u3090\u3091", None))
        self.lineEdit_18.setText(QCoreApplication.translate("MainWindow", u"\u304c\u304e\u3050\u3052\u3054\u3056\u3058\u305a\u305c\u305e\u3060\u3062\u3065\u3067\u3069\u3070\u3073\u3076\u3079\u307c\u3071\u3074\u3077\u307a\u307d", None))
        self.lineEdit_10.setText(QCoreApplication.translate("MainWindow", u"\u3041\u3043\u3045\u3047\u3049\u3063\u3083\u3085\u3087\u308e", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u30ab\u30bf\u30ab\u30ca", None))
        self.lineEdit_19.setText(QCoreApplication.translate("MainWindow", u"\u30a2\u30a4\u30a6\u30a8\u30aa\u30ab\u30ad\u30af\u30b1\u30b3\u30b5\u30b7\u30b9\u30bb\u30bd\u30bf\u30c1\u30c4\u30c6\u30c8\u30ca\u30cb\u30cc\u30cd\u30ce\u30cf\u30d2\u30d5\u30d8\u30db\u30de\u30df\u30e0\u30e1\u30e2\u30e4\u30e6\u30e8\u30e9\u30ea\u30eb\u30ec\u30ed\u30ef\u30f2\u30f3", None))
        self.lineEdit_11.setText(QCoreApplication.translate("MainWindow", u"\u30f0\u30f1", None))
        self.lineEdit_20.setText(QCoreApplication.translate("MainWindow", u"\u30f4\u30ac\u30ae\u30b0\u30b2\u30b4\u30b6\u30b8\u30ba\u30bc\u30be\u30c0\u30c2\u30c5\u30c7\u30c9\u30d0\u30d3\u30d6\u30d9\u30dc\u30d1\u30d4\u30d7\u30da\u30dd", None))
        self.lineEdit_12.setText(QCoreApplication.translate("MainWindow", u"\u30a1\u30a3\u30a5\u30a7\u30a9\u30f5\u30f6\u30c3\u30e3\u30e5\u30e7\u30ee", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u3072\u3089\u304c\u306a \u30ab\u30bf\u30ab\u30ca", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u6587\u5b57(\u534a\u89d2)", None))
        self.lineEdit_13.setText(QCoreApplication.translate("MainWindow", u"abcdefghijklmnopqrstuvwxyz", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u5927\u6587\u5b57(\u534a\u89d2)", None))
        self.lineEdit_14.setText(QCoreApplication.translate("MainWindow", u"ABCDEFGHIJKLMNOPQRSTUVWXYZ", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\u5c0f\u6587\u5b57(\u5168\u89d2)", None))
        self.lineEdit_15.setText(QCoreApplication.translate("MainWindow", u"\uff41\uff42\uff43\uff44\uff45\uff46\uff47\uff48\uff49\uff4a\uff4b\uff4c\uff4d\uff4e\uff4f\uff50\uff51\uff52\uff53\uff54\uff55\uff56\uff57\uff58\uff59\uff5a", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"\u5927\u6587\u5b57(\u5168\u89d2)", None))
        self.lineEdit_16.setText(QCoreApplication.translate("MainWindow", u"\uff21\uff22\uff23\uff24\uff25\uff26\uff27\uff28\uff29\uff2a\uff2b\uff2c\uff2d\uff2e\uff2f\uff30\uff31\uff32\uff33\uff34\uff35\uff36\uff37\uff38\uff39\uff3a", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"\u30ae\u30ea\u30b7\u30e3\u5c0f\u6587\u5b57", None))
        self.lineEdit_22.setText(QCoreApplication.translate("MainWindow", u"\u03b1\u03b2\u03b3\u03b4\u03b5\u03b6\u03b7\u03b8\u03b9\u03ba\u03bb\u03bc\u03bd\u03be\u03bf\u03c0\u03c1\u03c3\u03c4\u03c5\u03c6\u03c7\u03c8\u03c9", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"\u30ae\u30ea\u30b7\u30e3\u5927\u6587\u5b57", None))
        self.lineEdit_21.setText(QCoreApplication.translate("MainWindow", u"\u0391\u0392\u0393\u0394\u0395\u0396\u0397\u0398\u0399\u039a\u039b\u039c\u039d\u039e\u039f\u03a0\u03a1\u03a3\u03a4\u03a5\u03a6\u03a7\u03a8\u03a9", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"\u30eb\u30fc\u30f3\u6587\u5b57", None))
        self.lineEdit_23.setText(QCoreApplication.translate("MainWindow", u"\u16a0\u16a2\u16a6\u16a8\u16b1\u16b2\u16b7\u16b9\u16ba\u16be\u16c1\u16c3\u16c7\u16c8\u16c9\u16ca\u16cf\u16d2\u16d6\u16d7\u16da\u16dc\u16df\u16de", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"\u53e4\u30a4\u30bf\u30ea\u30a2\u6587\u5b57", None))
        self.italy1LineEdit.setText("")
        self.italy2LineEdit.setText("")
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"\u30ea\u30e5\u30ad\u30a2\u6587\u5b57", None))
        self.lycianLineEdit.setText("")
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"\u30d5\u30a7\u30cb\u30ad\u30a2\u6587\u5b57", None))
#if QT_CONFIG(tooltip)
        self.phoenician1LineEdit.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.phoenician1LineEdit.setText("")
        self.phoenician2LineEdit.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"\u53e4\u4ee3\u30da\u30eb\u30b7\u30a2\u6587\u5b57", None))
        self.persian1LineEdit.setText("")
        self.persian2LineEdit.setText("")
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"\u30ad\u30e5\u30d7\u30ed\u30b9\u6587\u5b57", None))
        self.cypriotLineEdit.setText("")
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"\u30b4\u30fc\u30c8\u6587\u5b57", None))
        self.gothicLineEdit.setText("")
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"\u203b \u5f8c\u534a\u306e\u6587\u5b57\u306f Segoe UI Historic \u3067\u8868\u793a\u3057\u3066\u3044\u307e\u3059\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\u30a2\u30eb\u30d5\u30a1\u30d9\u30c3\u30c8\u7b49", None))
        self.cuneiform1PlainTextEdit.setPlainText("")
        self.cuneiform2PlainTextEdit.setPlainText("")
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"\u203bSegoe UI Historic \u3067\u8868\u793a\u3057\u3066\u3044\u307e\u3059\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"\u6954\u5f62\u6587\u5b57", None))
        self.hieroglyph1PlainTextEdit.setPlainText("")
        self.hieroglyph2PlainTextEdit.setPlainText("")
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"\u203bSegoe UI Historic \u3067\u8868\u793a\u3057\u3066\u3044\u307e\u3059\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), QCoreApplication.translate("MainWindow", u"\u30d2\u30a8\u30ed\u30b0\u30ea\u30d5", None))
        self.ma01LineEdit.setText("")
        self.ma02LineEdit.setText("")
        self.ma03LineEdit.setText("")
        self.ma04LineEdit.setText("")
        self.ma05LineEdit.setText("")
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"\u203b\u3000Segoe UI Symbol \u3067\u8868\u793a\u51fa\u6765\u307e\u3059\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), QCoreApplication.translate("MainWindow", u"\u9ebb\u96c0", None))
        self.cards01LineEdit.setText("")
        self.cards02LineEdit.setText("")
        self.cards03LineEdit.setText("")
        self.cards04LineEdit.setText("")
        self.cards05LineEdit.setText("")
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"\u203b\u3000Segoe UI Symbol \u3067\u8868\u793a\u51fa\u6765\u307e\u3059\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30f3\u30d7", None))
        self.alchemyPlainTextEdit.setPlainText("")
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"\u203b\u3000Segoe UI Symbol \u3067\u8868\u793a\u51fa\u6765\u307e\u3059\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), QCoreApplication.translate("MainWindow", u"\u932c\u91d1\u8853\u8a18\u53f7", None))
    # retranslateUi


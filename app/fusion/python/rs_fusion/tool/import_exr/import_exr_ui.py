# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_exr.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(374, 122)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.fileGroupBox = QGroupBox(self.centralwidget)
        self.fileGroupBox.setObjectName(u"fileGroupBox")
        self.formLayout = QFormLayout(self.fileGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.fileGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.exrLineEdit = QLineEdit(self.fileGroupBox)
        self.exrLineEdit.setObjectName(u"exrLineEdit")

        self.horizontalLayout_2.addWidget(self.exrLineEdit)

        self.exrToolButton = QToolButton(self.fileGroupBox)
        self.exrToolButton.setObjectName(u"exrToolButton")

        self.horizontalLayout_2.addWidget(self.exrToolButton)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)


        self.verticalLayout_7.addWidget(self.fileGroupBox)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.importButton = QPushButton(self.centralwidget)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.importButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.fileGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"EXR", None))
        self.exrToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.importButton.setText(QCoreApplication.translate("MainWindow", u"import", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


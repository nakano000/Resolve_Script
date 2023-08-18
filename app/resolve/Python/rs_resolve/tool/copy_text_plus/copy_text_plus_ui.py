# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'copy_text_plus.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(358, 417)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.trackGroupBox = QGroupBox(self.centralwidget)
        self.trackGroupBox.setObjectName(u"trackGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trackGroupBox.sizePolicy().hasHeightForWidth())
        self.trackGroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.trackGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.trackGroupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sourceComboBox = QComboBox(self.trackGroupBox)
        self.sourceComboBox.setObjectName(u"sourceComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sourceComboBox)

        self.label_2 = QLabel(self.trackGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.destinationComboBox = QComboBox(self.trackGroupBox)
        self.destinationComboBox.setObjectName(u"destinationComboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.destinationComboBox)

        self.swapButton = QPushButton(self.trackGroupBox)
        self.swapButton.setObjectName(u"swapButton")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.swapButton)


        self.horizontalLayout_2.addLayout(self.formLayout)

        self.updateButton = QPushButton(self.trackGroupBox)
        self.updateButton.setObjectName(u"updateButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.updateButton.sizePolicy().hasHeightForWidth())
        self.updateButton.setSizePolicy(sizePolicy1)
        self.updateButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout_2.addWidget(self.updateButton)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addWidget(self.trackGroupBox)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.plainTextEdit = QPlainTextEdit(self.groupBox)
        self.plainTextEdit.setObjectName(u"plainTextEdit")

        self.verticalLayout_2.addWidget(self.plainTextEdit)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.saveButton = QPushButton(self.groupBox)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.saveButton)

        self.loadButton = QPushButton(self.groupBox)
        self.loadButton.setObjectName(u"loadButton")
        self.loadButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.loadButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.copyButton = QPushButton(self.centralwidget)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.copyButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.trackGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Video Track", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Destination", None))
        self.swapButton.setText(QCoreApplication.translate("MainWindow", u"\u25b2\u25bc", None))
#if QT_CONFIG(tooltip)
        self.updateButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"update", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"exclusion", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"save", None))
        self.loadButton.setText(QCoreApplication.translate("MainWindow", u"load", None))
#if QT_CONFIG(tooltip)
        self.copyButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"copy", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


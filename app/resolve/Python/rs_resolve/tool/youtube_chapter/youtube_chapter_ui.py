# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'youtube_chapter.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QListView, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(465, 441)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.titleLabel = QLabel(self.centralwidget)
        self.titleLabel.setObjectName(u"titleLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.titleLabel)

        self.titleLineEdit = QLineEdit(self.centralwidget)
        self.titleLineEdit.setObjectName(u"titleLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.titleLineEdit)

        self.delimiterLabel = QLabel(self.centralwidget)
        self.delimiterLabel.setObjectName(u"delimiterLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.delimiterLabel)

        self.delimiterLineEdit = QLineEdit(self.centralwidget)
        self.delimiterLineEdit.setObjectName(u"delimiterLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.delimiterLineEdit)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.niconicoCheckBox = QCheckBox(self.centralwidget)
        self.niconicoCheckBox.setObjectName(u"niconicoCheckBox")

        self.verticalLayout_2.addWidget(self.niconicoCheckBox)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.markerListView = QListView(self.groupBox)
        self.markerListView.setObjectName(u"markerListView")
        self.markerListView.setBaseSize(QSize(0, 0))
        self.markerListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.markerListView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout.addWidget(self.markerListView)


        self.verticalLayout_2.addWidget(self.groupBox)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.chapterPlainTextEdit = QPlainTextEdit(self.centralwidget)
        self.chapterPlainTextEdit.setObjectName(u"chapterPlainTextEdit")

        self.horizontalLayout_2.addWidget(self.chapterPlainTextEdit)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.makeButton = QPushButton(self.centralwidget)
        self.makeButton.setObjectName(u"makeButton")
        self.makeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.makeButton)

        self.copyButton = QPushButton(self.centralwidget)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.copyButton)

        self.horizontalSpacer = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"\u984c\u540d", None))
        self.delimiterLabel.setText(QCoreApplication.translate("MainWindow", u"\u533a\u5207\u308a\u6587\u5b57", None))
        self.niconicoCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u30cb\u30b3\u30cb\u30b3\u52d5\u753b\u7528\u306b#\u3092\u4ed8\u3051\u308b", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"marker", None))
        self.makeButton.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210", None))
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"\u30b3\u30d4\u30fc", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'voice_bin_assistant.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QDoubleSpinBox,
    QFormLayout, QGroupBox, QHBoxLayout, QLabel,
    QListView, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTextEdit, QVBoxLayout,
    QWidget)

from rs.gui.log import LogTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(367, 665)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.importWaitSpinBox = QDoubleSpinBox(self.groupBox)
        self.importWaitSpinBox.setObjectName(u"importWaitSpinBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.importWaitSpinBox)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.offsetSpinBox = QSpinBox(self.groupBox)
        self.offsetSpinBox.setObjectName(u"offsetSpinBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.offsetSpinBox)

        self.referTrackCheckBox = QCheckBox(self.groupBox)
        self.referTrackCheckBox.setObjectName(u"referTrackCheckBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.referTrackCheckBox)


        self.verticalLayout_6.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.tatieWaitSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.tatieWaitSpinBox.setObjectName(u"tatieWaitSpinBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.tatieWaitSpinBox)


        self.verticalLayout_4.addLayout(self.formLayout_2)

        self.rebuildCheckBox = QCheckBox(self.groupBox_3)
        self.rebuildCheckBox.setObjectName(u"rebuildCheckBox")

        self.verticalLayout_4.addWidget(self.rebuildCheckBox)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.groupBox_6 = QGroupBox(self.centralwidget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_4 = QGroupBox(self.groupBox_6)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy1)
        self.groupBox_4.setMinimumSize(QSize(30, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.videoListView = QListView(self.groupBox_4)
        self.videoListView.setObjectName(u"videoListView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.videoListView.sizePolicy().hasHeightForWidth())
        self.videoListView.setSizePolicy(sizePolicy2)
        self.videoListView.setMinimumSize(QSize(0, 0))
        self.videoListView.setBaseSize(QSize(0, 0))
        self.videoListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.videoListView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_2.addWidget(self.videoListView)


        self.horizontalLayout_2.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.groupBox_6)
        self.groupBox_5.setObjectName(u"groupBox_5")
        sizePolicy1.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy1)
        self.groupBox_5.setMinimumSize(QSize(30, 0))
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.audioListView = QListView(self.groupBox_5)
        self.audioListView.setObjectName(u"audioListView")
        sizePolicy2.setHeightForWidth(self.audioListView.sizePolicy().hasHeightForWidth())
        self.audioListView.setSizePolicy(sizePolicy2)
        self.audioListView.setMinimumSize(QSize(0, 0))
        self.audioListView.setBaseSize(QSize(1, 0))
        self.audioListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.audioListView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_3.addWidget(self.audioListView)


        self.horizontalLayout_2.addWidget(self.groupBox_5)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.copyTextButton = QPushButton(self.groupBox_6)
        self.copyTextButton.setObjectName(u"copyTextButton")

        self.horizontalLayout_4.addWidget(self.copyTextButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.updateTrackButton = QPushButton(self.groupBox_6)
        self.updateTrackButton.setObjectName(u"updateTrackButton")

        self.horizontalLayout_4.addWidget(self.updateTrackButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_6.addWidget(self.groupBox_6)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy3)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logTextEdit = LogTextEdit(self.groupBox_2)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy2.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy2)
        self.logTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.logTextEdit)


        self.verticalLayout_6.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textPlusButton = QPushButton(self.centralwidget)
        self.textPlusButton.setObjectName(u"textPlusButton")
        self.textPlusButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.textPlusButton)

        self.tatieButton = QPushButton(self.centralwidget)
        self.tatieButton.setObjectName(u"tatieButton")
        self.tatieButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.tatieButton)

        self.textPlusTatieButton = QPushButton(self.centralwidget)
        self.textPlusTatieButton.setObjectName(u"textPlusTatieButton")
        self.textPlusTatieButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout.addWidget(self.textPlusTatieButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_6.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.importButton = QPushButton(self.centralwidget)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_3.addWidget(self.importButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u3061\u6642\u9593", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9593\u9694(\u30d5\u30ec\u30fc\u30e0)", None))
        self.referTrackCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u30d3\u30c7\u30aa\u30c8\u30e9\u30c3\u30af\u3092\u53c2\u7167\u3059\u308b", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"TEXT+ \u7acb\u3061\u7d75", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u3061\u6642\u9593", None))
        self.rebuildCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u6bce\u56de\u30b9\u30af\u30ea\u30d7\u30c8\u3092\u4f5c\u308b", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u9078\u629e", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u30d3\u30c7\u30aa \u30c8\u30e9\u30c3\u30af", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u30aa\u30fc\u30c7\u30a3\u30aa \u30c8\u30e9\u30c3\u30af", None))
        self.copyTextButton.setText(QCoreApplication.translate("MainWindow", u"TEXT+ \u30b3\u30d4\u30fc", None))
        self.updateTrackButton.setText(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af \u66f4\u65b0", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u30ed\u30b0", None))
        self.textPlusButton.setText(QCoreApplication.translate("MainWindow", u"TEXT+", None))
        self.tatieButton.setText(QCoreApplication.translate("MainWindow", u"\u7acb\u3061\u7d75", None))
        self.textPlusTatieButton.setText(QCoreApplication.translate("MainWindow", u"TEXT+ \u7acb\u3061\u7d75", None))
        self.importButton.setText(QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f(wav)", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lip_sync_window.ui'
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
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(272, 313)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.tatieTimeOutSpinBox = QDoubleSpinBox(self.centralwidget)
        self.tatieTimeOutSpinBox.setObjectName(u"tatieTimeOutSpinBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.tatieTimeOutSpinBox)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.autoLockCheckBox = QCheckBox(self.centralwidget)
        self.autoLockCheckBox.setObjectName(u"autoLockCheckBox")

        self.verticalLayout.addWidget(self.autoLockCheckBox)

        self.useDeleteCheckBox = QCheckBox(self.centralwidget)
        self.useDeleteCheckBox.setObjectName(u"useDeleteCheckBox")

        self.verticalLayout.addWidget(self.useDeleteCheckBox)

        self.shortcutButton = QPushButton(self.centralwidget)
        self.shortcutButton.setObjectName(u"shortcutButton")

        self.verticalLayout.addWidget(self.shortcutButton)

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
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.updateTrackButton = QPushButton(self.groupBox_6)
        self.updateTrackButton.setObjectName(u"updateTrackButton")

        self.horizontalLayout_4.addWidget(self.updateTrackButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout.addWidget(self.groupBox_6)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.applyButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"time out", None))
        self.autoLockCheckBox.setText(QCoreApplication.translate("MainWindow", u"Auto Lock", None))
        self.useDeleteCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u58f0\u304c\u306a\u3044\u90e8\u5206\u306e\u7acb\u3061\u7d75\u3092\u524a\u9664", None))
        self.shortcutButton.setText(QCoreApplication.translate("MainWindow", u"shortcut", None))
        self.groupBox_6.setTitle("")
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Video Track", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Audio Track", None))
        self.updateTrackButton.setText(QCoreApplication.translate("MainWindow", u"update", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"apply", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


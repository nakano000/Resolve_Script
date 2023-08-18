# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'disk_cache.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGroupBox, QHBoxLayout,
    QListView, QMainWindow, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from rs.tool.disk_cache.drag_button import DragButton

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(230, 387)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cacheDragButton = DragButton(self.centralwidget)
        self.cacheDragButton.setObjectName(u"cacheDragButton")
        self.cacheDragButton.setMinimumSize(QSize(100, 100))

        self.horizontalLayout_2.addWidget(self.cacheDragButton)

        self.horizontalSpacer_2 = QSpacerItem(10, 10, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.clearDragButton = DragButton(self.centralwidget)
        self.clearDragButton.setObjectName(u"clearDragButton")
        self.clearDragButton.setMinimumSize(QSize(100, 100))

        self.horizontalLayout_2.addWidget(self.clearDragButton)

        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
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


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.videoIndexListView = QListView(self.groupBox_2)
        self.videoIndexListView.setObjectName(u"videoIndexListView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.videoIndexListView.sizePolicy().hasHeightForWidth())
        self.videoIndexListView.setSizePolicy(sizePolicy2)
        self.videoIndexListView.setBaseSize(QSize(0, 0))
        self.videoIndexListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.videoIndexListView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.videoIndexListView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_2.addWidget(self.videoIndexListView)


        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.cacheDragButton.setText(QCoreApplication.translate("MainWindow", u" cache", None))
        self.clearDragButton.setText(QCoreApplication.translate("MainWindow", u" clear", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"marker", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"index", None))
    # retranslateUi


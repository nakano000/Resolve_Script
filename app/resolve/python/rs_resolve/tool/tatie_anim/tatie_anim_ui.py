# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tatie_anim.ui'
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
    QListView, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(236, 233)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QSize(30, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.videoIndexListView = QListView(self.groupBox_2)
        self.videoIndexListView.setObjectName(u"videoIndexListView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.videoIndexListView.sizePolicy().hasHeightForWidth())
        self.videoIndexListView.setSizePolicy(sizePolicy1)
        self.videoIndexListView.setMinimumSize(QSize(0, 0))
        self.videoIndexListView.setBaseSize(QSize(0, 0))
        self.videoIndexListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.videoIndexListView.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.videoIndexListView.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.verticalLayout_2.addWidget(self.videoIndexListView)


        self.horizontalLayout_2.addWidget(self.groupBox_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.copyButton = QPushButton(self.groupBox)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout.addWidget(self.copyButton)

        self.refreshButton = QPushButton(self.groupBox)
        self.refreshButton.setObjectName(u"refreshButton")
        self.refreshButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout.addWidget(self.refreshButton)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(40, 40))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"index", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u30b3\u30de\u30f3\u30c9", None))
#if QT_CONFIG(tooltip)
        self.copyButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"copy", None))
#if QT_CONFIG(tooltip)
        self.refreshButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.refreshButton.setText(QCoreApplication.translate("MainWindow", u"refresh", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


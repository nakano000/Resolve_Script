# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'playhead.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QToolButton, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(199, 212)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.num02SpinBox = QSpinBox(self.centralwidget)
        self.num02SpinBox.setObjectName(u"num02SpinBox")
        self.num02SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.num02SpinBox.setMaximum(999999999)

        self.gridLayout.addWidget(self.num02SpinBox, 1, 0, 1, 1)

        self.subtitleLeftButton = QToolButton(self.centralwidget)
        self.subtitleLeftButton.setObjectName(u"subtitleLeftButton")
        self.subtitleLeftButton.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.subtitleLeftButton, 2, 1, 1, 1)

        self.n02RightButton = QToolButton(self.centralwidget)
        self.n02RightButton.setObjectName(u"n02RightButton")
        self.n02RightButton.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.n02RightButton, 1, 2, 1, 1)

        self.subtitleComboBox = QComboBox(self.centralwidget)
        self.subtitleComboBox.setObjectName(u"subtitleComboBox")

        self.gridLayout.addWidget(self.subtitleComboBox, 2, 0, 1, 1)

        self.num01SpinBox = QSpinBox(self.centralwidget)
        self.num01SpinBox.setObjectName(u"num01SpinBox")
        self.num01SpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.num01SpinBox.setMaximum(999999999)

        self.gridLayout.addWidget(self.num01SpinBox, 0, 0, 1, 1)

        self.audioRightButton = QToolButton(self.centralwidget)
        self.audioRightButton.setObjectName(u"audioRightButton")
        self.audioRightButton.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.audioRightButton, 4, 2, 1, 1)

        self.vidioRightButton = QToolButton(self.centralwidget)
        self.vidioRightButton.setObjectName(u"vidioRightButton")
        self.vidioRightButton.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.vidioRightButton, 3, 2, 1, 1)

        self.n01LeftButton = QToolButton(self.centralwidget)
        self.n01LeftButton.setObjectName(u"n01LeftButton")
        self.n01LeftButton.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.n01LeftButton, 0, 1, 1, 1)

        self.subtitleRightButton = QToolButton(self.centralwidget)
        self.subtitleRightButton.setObjectName(u"subtitleRightButton")
        self.subtitleRightButton.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.subtitleRightButton, 2, 2, 1, 1)

        self.audioLeftButton = QToolButton(self.centralwidget)
        self.audioLeftButton.setObjectName(u"audioLeftButton")
        self.audioLeftButton.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.audioLeftButton, 4, 1, 1, 1)

        self.n02LeftButton = QToolButton(self.centralwidget)
        self.n02LeftButton.setObjectName(u"n02LeftButton")
        self.n02LeftButton.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.n02LeftButton, 1, 1, 1, 1)

        self.vidioLeftButton = QToolButton(self.centralwidget)
        self.vidioLeftButton.setObjectName(u"vidioLeftButton")
        self.vidioLeftButton.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.vidioLeftButton, 3, 1, 1, 1)

        self.audioComboBox = QComboBox(self.centralwidget)
        self.audioComboBox.setObjectName(u"audioComboBox")

        self.gridLayout.addWidget(self.audioComboBox, 4, 0, 1, 1)

        self.n01RightButton = QToolButton(self.centralwidget)
        self.n01RightButton.setObjectName(u"n01RightButton")
        self.n01RightButton.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.n01RightButton, 0, 2, 1, 1)

        self.videoComboBox = QComboBox(self.centralwidget)
        self.videoComboBox.setObjectName(u"videoComboBox")

        self.gridLayout.addWidget(self.videoComboBox, 3, 0, 1, 1)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 5, 0, 1, 1)

        self.timelineLeftButton = QToolButton(self.centralwidget)
        self.timelineLeftButton.setObjectName(u"timelineLeftButton")
        self.timelineLeftButton.setArrowType(Qt.LeftArrow)

        self.gridLayout.addWidget(self.timelineLeftButton, 5, 1, 1, 1)

        self.timelineRightButton = QToolButton(self.centralwidget)
        self.timelineRightButton.setObjectName(u"timelineRightButton")
        self.timelineRightButton.setArrowType(Qt.RightArrow)

        self.gridLayout.addWidget(self.timelineRightButton, 5, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.updateButton = QPushButton(self.centralwidget)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.updateButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(30, 30))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.subtitleLeftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.n02RightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.audioRightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.vidioRightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.n01LeftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.subtitleRightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.audioLeftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.n02LeftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.vidioLeftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.n01RightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Timeline", None))
        self.timelineLeftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.timelineRightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.updateButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"update", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'text_plus2srt.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QVBoxLayout, QWidget)

from rs.gui.log import LogTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(289, 233)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.videoComboBox = QComboBox(self.centralwidget)
        self.videoComboBox.setObjectName(u"videoComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoComboBox.sizePolicy().hasHeightForWidth())
        self.videoComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.videoComboBox)

        self.updateButton = QPushButton(self.centralwidget)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout_2.addWidget(self.updateButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.logTextEdit = LogTextEdit(self.groupBox_2)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy2)
        self.logTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.logTextEdit)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveButton = QPushButton(self.centralwidget)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.saveButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

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
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Video Track", None))
#if QT_CONFIG(tooltip)
        self.updateButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"update", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
#if QT_CONFIG(tooltip)
        self.saveButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"save", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


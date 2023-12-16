# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'subtitle2textPlus_typeB.ui'
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
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QTextEdit,
    QToolButton, QVBoxLayout, QWidget)

from rs.gui.log import LogTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(341, 372)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.settingFileLineEdit = QLineEdit(self.groupBox)
        self.settingFileLineEdit.setObjectName(u"settingFileLineEdit")

        self.horizontalLayout_3.addWidget(self.settingFileLineEdit)

        self.settingFileToolButton = QToolButton(self.groupBox)
        self.settingFileToolButton.setObjectName(u"settingFileToolButton")

        self.horizontalLayout_3.addWidget(self.settingFileToolButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.trackGroupBox = QGroupBox(self.centralwidget)
        self.trackGroupBox.setObjectName(u"trackGroupBox")
        self.verticalLayout = QVBoxLayout(self.trackGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.trackGroupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.subtitleComboBox = QComboBox(self.trackGroupBox)
        self.subtitleComboBox.setObjectName(u"subtitleComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.subtitleComboBox)

        self.label_2 = QLabel(self.trackGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.videoComboBox = QComboBox(self.trackGroupBox)
        self.videoComboBox.setObjectName(u"videoComboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.videoComboBox)


        self.horizontalLayout_2.addLayout(self.formLayout)

        self.updateButton = QPushButton(self.trackGroupBox)
        self.updateButton.setObjectName(u"updateButton")
        self.updateButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout_2.addWidget(self.updateButton)

        self.horizontalLayout_2.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_4.addWidget(self.trackGroupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(4, 4, 4, 4)
        self.logTextEdit = LogTextEdit(self.groupBox_2)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy1)
        self.logTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.logTextEdit)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.convertButton = QPushButton(self.centralwidget)
        self.convertButton.setObjectName(u"convertButton")
        self.convertButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.convertButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(50, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Setting File", None))
        self.settingFileToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.trackGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Track", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Subtitle", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Video", None))
#if QT_CONFIG(tooltip)
        self.updateButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"update", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
#if QT_CONFIG(tooltip)
        self.convertButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.convertButton.setText(QCoreApplication.translate("MainWindow", u"convert", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


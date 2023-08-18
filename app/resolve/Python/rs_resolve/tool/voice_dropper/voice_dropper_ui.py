# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'voice_dropper.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

from rs.gui.log import LogTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(340, 604)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.voiceDirLineEdit = QLineEdit(self.groupBox_3)
        self.voiceDirLineEdit.setObjectName(u"voiceDirLineEdit")

        self.horizontalLayout_2.addWidget(self.voiceDirLineEdit)

        self.voiceDirToolButton = QToolButton(self.groupBox_3)
        self.voiceDirToolButton.setObjectName(u"voiceDirToolButton")

        self.horizontalLayout_2.addWidget(self.voiceDirToolButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.statusLabel = QLabel(self.groupBox_3)
        self.statusLabel.setObjectName(u"statusLabel")
        self.statusLabel.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_3.addWidget(self.statusLabel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.startButton = QPushButton(self.groupBox_3)
        self.startButton.setObjectName(u"startButton")

        self.horizontalLayout_3.addWidget(self.startButton)

        self.stopButton = QPushButton(self.groupBox_3)
        self.stopButton.setObjectName(u"stopButton")

        self.horizontalLayout_3.addWidget(self.stopButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_4.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.timeOutSpinBox = QSpinBox(self.groupBox)
        self.timeOutSpinBox.setObjectName(u"timeOutSpinBox")
        self.timeOutSpinBox.setMaximum(999)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.timeOutSpinBox)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.offsetSpinBox = QSpinBox(self.groupBox)
        self.offsetSpinBox.setObjectName(u"offsetSpinBox")
        self.offsetSpinBox.setMaximum(999999999)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.offsetSpinBox)

        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.extendSpinBox = QSpinBox(self.groupBox)
        self.extendSpinBox.setObjectName(u"extendSpinBox")
        self.extendSpinBox.setMaximum(999999999)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.extendSpinBox)

        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.videoIndexSpinBox = QSpinBox(self.groupBox)
        self.videoIndexSpinBox.setObjectName(u"videoIndexSpinBox")
        self.videoIndexSpinBox.setMinimum(1)
        self.videoIndexSpinBox.setMaximum(50)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.videoIndexSpinBox)

        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label)

        self.audioIndexSpinBox = QSpinBox(self.groupBox)
        self.audioIndexSpinBox.setObjectName(u"audioIndexSpinBox")
        self.audioIndexSpinBox.setMinimum(1)
        self.audioIndexSpinBox.setMaximum(50)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.audioIndexSpinBox)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.makeTextCheckBox = QCheckBox(self.groupBox)
        self.makeTextCheckBox.setObjectName(u"makeTextCheckBox")

        self.verticalLayout_3.addWidget(self.makeTextCheckBox)

        self.useCharaCheckBox = QCheckBox(self.groupBox)
        self.useCharaCheckBox.setObjectName(u"useCharaCheckBox")

        self.verticalLayout_3.addWidget(self.useCharaCheckBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.charaButton = QPushButton(self.groupBox)
        self.charaButton.setObjectName(u"charaButton")

        self.horizontalLayout_4.addWidget(self.charaButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logTextEdit = LogTextEdit(self.groupBox_2)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy2)
        self.logTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.logTextEdit)


        self.verticalLayout_4.addWidget(self.groupBox_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.importButton = QPushButton(self.centralwidget)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.importButton)

        self.lipSyncButton = QPushButton(self.centralwidget)
        self.lipSyncButton.setObjectName(u"lipSyncButton")
        self.lipSyncButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.lipSyncButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(30, 30))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u58f0\u30d5\u30a9\u30eb\u30c0", None))
        self.voiceDirToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u4e2d", None))
        self.startButton.setText(QCoreApplication.translate("MainWindow", u"start", None))
        self.stopButton.setText(QCoreApplication.translate("MainWindow", u"stop", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u30bf\u30a4\u30e0\u30a2\u30a6\u30c8(\u79d2)", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u9593\u9694(\u30d5\u30ec\u30fc\u30e0)", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5b57\u5e55\u5ef6\u9577(\u30d5\u30ec\u30fc\u30e0)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u30d3\u30c7\u30aa\u30c8\u30e9\u30c3\u30af", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u30aa\u30fc\u30c7\u30a3\u30aa\u30c8\u30e9\u30c3\u30af", None))
        self.makeTextCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u30c6\u30ad\u30b9\u30c8\u30d5\u30a1\u30a4\u30eb\u304c\u306a\u3051\u308c\u3070\u3001\u30af\u30ea\u30c3\u30d7\u30dc\u30fc\u30c9\u304b\u3089\u4f5c\u308b", None))
        self.useCharaCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u30ad\u30e3\u30e9\u30af\u30bf\u30fc\u8a2d\u5b9a\u3092\u4f7f\u3063\u3066\u914d\u7f6e", None))
        self.charaButton.setText(QCoreApplication.translate("MainWindow", u"\u30ad\u30e3\u30e9\u30af\u30bf\u30fc\u8a2d\u5b9a", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u30ed\u30b0", None))
        self.importButton.setText(QCoreApplication.translate("MainWindow", u"import", None))
        self.lipSyncButton.setText(QCoreApplication.translate("MainWindow", u"\u53e3\u30d1\u30af", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


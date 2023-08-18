# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'subtitle2text_plus.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFormLayout, QGroupBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(217, 302)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.settingGroupBox = QGroupBox(self.centralwidget)
        self.settingGroupBox.setObjectName(u"settingGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.settingGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.waitLabel = QLabel(self.settingGroupBox)
        self.waitLabel.setObjectName(u"waitLabel")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.waitLabel)

        self.waitTimeSpinBox = QDoubleSpinBox(self.settingGroupBox)
        self.waitTimeSpinBox.setObjectName(u"waitTimeSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.waitTimeSpinBox.sizePolicy().hasHeightForWidth())
        self.waitTimeSpinBox.setSizePolicy(sizePolicy)
        self.waitTimeSpinBox.setMaximum(999.990000000000009)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.waitTimeSpinBox)

        self.clipCplorLabel = QLabel(self.settingGroupBox)
        self.clipCplorLabel.setObjectName(u"clipCplorLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.clipCplorLabel)

        self.colorComboBox = QComboBox(self.settingGroupBox)
        self.colorComboBox.setObjectName(u"colorComboBox")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.colorComboBox)


        self.verticalLayout_3.addLayout(self.formLayout_2)

        self.autoLockCheckBox = QCheckBox(self.settingGroupBox)
        self.autoLockCheckBox.setObjectName(u"autoLockCheckBox")

        self.verticalLayout_3.addWidget(self.autoLockCheckBox)

        self.shortcutButton = QPushButton(self.settingGroupBox)
        self.shortcutButton.setObjectName(u"shortcutButton")

        self.verticalLayout_3.addWidget(self.shortcutButton)


        self.verticalLayout_2.addWidget(self.settingGroupBox)

        self.trackGroupBox = QGroupBox(self.centralwidget)
        self.trackGroupBox.setObjectName(u"trackGroupBox")
        self.verticalLayout = QVBoxLayout(self.trackGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
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


        self.verticalLayout_2.addWidget(self.trackGroupBox)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

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


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.settingGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8a2d\u5b9a", None))
        self.waitLabel.setText(QCoreApplication.translate("MainWindow", u"\u5f85\u3061\u6642\u9593(\u79d2)", None))
        self.clipCplorLabel.setText(QCoreApplication.translate("MainWindow", u"\u30af\u30ea\u30c3\u30d7\u30ab\u30e9\u30fc", None))
        self.autoLockCheckBox.setText(QCoreApplication.translate("MainWindow", u"Auto Lock", None))
        self.shortcutButton.setText(QCoreApplication.translate("MainWindow", u"shortcut", None))
        self.trackGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Subtitle", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Video", None))
#if QT_CONFIG(tooltip)
        self.updateButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.updateButton.setText(QCoreApplication.translate("MainWindow", u"update", None))
#if QT_CONFIG(tooltip)
        self.convertButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u30c8\u30e9\u30c3\u30af\u66f4\u65b0", None))
#endif // QT_CONFIG(tooltip)
        self.convertButton.setText(QCoreApplication.translate("MainWindow", u"convert", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


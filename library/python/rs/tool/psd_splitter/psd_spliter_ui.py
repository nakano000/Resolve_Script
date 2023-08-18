# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'psd_spliter.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QToolButton, QVBoxLayout,
    QWidget)

from rs.gui.log import LogTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(588, 537)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.settingGroupBox = QGroupBox(self.centralwidget)
        self.settingGroupBox.setObjectName(u"settingGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.settingGroupBox.sizePolicy().hasHeightForWidth())
        self.settingGroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.settingGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.settingGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.srcLineEdit = QLineEdit(self.settingGroupBox)
        self.srcLineEdit.setObjectName(u"srcLineEdit")

        self.horizontalLayout_2.addWidget(self.srcLineEdit)

        self.srcToolButton = QToolButton(self.settingGroupBox)
        self.srcToolButton.setObjectName(u"srcToolButton")

        self.horizontalLayout_2.addWidget(self.srcToolButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.destLabel = QLabel(self.settingGroupBox)
        self.destLabel.setObjectName(u"destLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.destLabel)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dstLineEdit = QLineEdit(self.settingGroupBox)
        self.dstLineEdit.setObjectName(u"dstLineEdit")

        self.horizontalLayout.addWidget(self.dstLineEdit)

        self.dstToolButton = QToolButton(self.settingGroupBox)
        self.dstToolButton.setObjectName(u"dstToolButton")

        self.horizontalLayout.addWidget(self.dstToolButton)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.useCp932CheckBox = QCheckBox(self.settingGroupBox)
        self.useCp932CheckBox.setObjectName(u"useCp932CheckBox")

        self.verticalLayout_2.addWidget(self.useCp932CheckBox)


        self.verticalLayout_3.addWidget(self.settingGroupBox)

        self.logGroupBox = QGroupBox(self.centralwidget)
        self.logGroupBox.setObjectName(u"logGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logGroupBox.sizePolicy().hasHeightForWidth())
        self.logGroupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.logGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logTextEdit = LogTextEdit(self.logGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy2)
        self.logTextEdit.setLineWrapMode(QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.logTextEdit)


        self.verticalLayout_3.addWidget(self.logGroupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.splitButton = QPushButton(self.centralwidget)
        self.splitButton.setObjectName(u"splitButton")
        self.splitButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout_3.addWidget(self.splitButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 588, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.settingGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8a2d\u5b9a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PSD", None))
        self.srcToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.destLabel.setText(QCoreApplication.translate("MainWindow", u"\u51fa\u529b\u5148", None))
        self.dstToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.useCp932CheckBox.setText(QCoreApplication.translate("MainWindow", u"\u5f37\u5236\u7684\u306b\u3001\u6587\u5b57\u30b3\u30fc\u30c9 cp932 \u3092\u4f7f\u3046 (\u6587\u5b57\u5316\u3051\u3059\u308b\u5834\u5408\u306b\u4f7f\u3063\u3066\u307f\u3066\u4e0b\u3055\u3044\u3002)", None))
        self.logGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u30ed\u30b0", None))
        self.splitButton.setText(QCoreApplication.translate("MainWindow", u"split", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


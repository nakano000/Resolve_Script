# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pivot_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(167, 434)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(167, 380))
        self.groupBox = QGroupBox(self.widget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 0, 167, 175))
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(167, 175))
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.nwButton = QPushButton(self.groupBox)
        self.nwButton.setObjectName(u"nwButton")
        sizePolicy.setHeightForWidth(self.nwButton.sizePolicy().hasHeightForWidth())
        self.nwButton.setSizePolicy(sizePolicy)
        self.nwButton.setMinimumSize(QSize(45, 45))
        self.nwButton.setMaximumSize(QSize(45, 45))
        font = QFont()
        font.setFamilies([u"\u30e1\u30a4\u30ea\u30aa"])
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        self.nwButton.setFont(font)

        self.gridLayout.addWidget(self.nwButton, 0, 0, 1, 1)

        self.nButton = QPushButton(self.groupBox)
        self.nButton.setObjectName(u"nButton")
        sizePolicy.setHeightForWidth(self.nButton.sizePolicy().hasHeightForWidth())
        self.nButton.setSizePolicy(sizePolicy)
        self.nButton.setMinimumSize(QSize(45, 45))
        self.nButton.setMaximumSize(QSize(45, 45))
        self.nButton.setFont(font)

        self.gridLayout.addWidget(self.nButton, 0, 1, 1, 1)

        self.neButton = QPushButton(self.groupBox)
        self.neButton.setObjectName(u"neButton")
        sizePolicy.setHeightForWidth(self.neButton.sizePolicy().hasHeightForWidth())
        self.neButton.setSizePolicy(sizePolicy)
        self.neButton.setMinimumSize(QSize(45, 45))
        self.neButton.setMaximumSize(QSize(45, 45))
        self.neButton.setFont(font)

        self.gridLayout.addWidget(self.neButton, 0, 2, 1, 1)

        self.wButton = QPushButton(self.groupBox)
        self.wButton.setObjectName(u"wButton")
        sizePolicy.setHeightForWidth(self.wButton.sizePolicy().hasHeightForWidth())
        self.wButton.setSizePolicy(sizePolicy)
        self.wButton.setMinimumSize(QSize(45, 45))
        self.wButton.setMaximumSize(QSize(45, 45))
        self.wButton.setFont(font)

        self.gridLayout.addWidget(self.wButton, 1, 0, 1, 1)

        self.centerButton = QPushButton(self.groupBox)
        self.centerButton.setObjectName(u"centerButton")
        sizePolicy.setHeightForWidth(self.centerButton.sizePolicy().hasHeightForWidth())
        self.centerButton.setSizePolicy(sizePolicy)
        self.centerButton.setMinimumSize(QSize(45, 45))
        self.centerButton.setMaximumSize(QSize(45, 45))
        self.centerButton.setFont(font)

        self.gridLayout.addWidget(self.centerButton, 1, 1, 1, 1)

        self.eButton = QPushButton(self.groupBox)
        self.eButton.setObjectName(u"eButton")
        sizePolicy.setHeightForWidth(self.eButton.sizePolicy().hasHeightForWidth())
        self.eButton.setSizePolicy(sizePolicy)
        self.eButton.setMinimumSize(QSize(45, 45))
        self.eButton.setMaximumSize(QSize(45, 45))
        self.eButton.setFont(font)

        self.gridLayout.addWidget(self.eButton, 1, 2, 1, 1)

        self.swButton = QPushButton(self.groupBox)
        self.swButton.setObjectName(u"swButton")
        sizePolicy.setHeightForWidth(self.swButton.sizePolicy().hasHeightForWidth())
        self.swButton.setSizePolicy(sizePolicy)
        self.swButton.setMinimumSize(QSize(45, 45))
        self.swButton.setMaximumSize(QSize(45, 45))
        self.swButton.setFont(font)

        self.gridLayout.addWidget(self.swButton, 2, 0, 1, 1)

        self.sButton = QPushButton(self.groupBox)
        self.sButton.setObjectName(u"sButton")
        sizePolicy.setHeightForWidth(self.sButton.sizePolicy().hasHeightForWidth())
        self.sButton.setSizePolicy(sizePolicy)
        self.sButton.setMinimumSize(QSize(45, 45))
        self.sButton.setMaximumSize(QSize(45, 45))
        self.sButton.setFont(font)

        self.gridLayout.addWidget(self.sButton, 2, 1, 1, 1)

        self.seButton = QPushButton(self.groupBox)
        self.seButton.setObjectName(u"seButton")
        sizePolicy.setHeightForWidth(self.seButton.sizePolicy().hasHeightForWidth())
        self.seButton.setSizePolicy(sizePolicy)
        self.seButton.setMinimumSize(QSize(45, 45))
        self.seButton.setMaximumSize(QSize(45, 45))
        self.seButton.setFont(font)

        self.gridLayout.addWidget(self.seButton, 2, 2, 1, 1)

        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(0, 295, 167, 84))
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_2 = QLabel(self.groupBox_2)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.setButton = QPushButton(self.groupBox_2)
        self.setButton.setObjectName(u"setButton")
        sizePolicy.setHeightForWidth(self.setButton.sizePolicy().hasHeightForWidth())
        self.setButton.setSizePolicy(sizePolicy)
        self.setButton.setMinimumSize(QSize(50, 50))
        self.setButton.setMaximumSize(QSize(50, 50))

        self.gridLayout_2.addWidget(self.setButton, 0, 2, 2, 1)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.xLineEdit = QLineEdit(self.groupBox_2)
        self.xLineEdit.setObjectName(u"xLineEdit")

        self.gridLayout_2.addWidget(self.xLineEdit, 0, 1, 1, 1)

        self.yLineEdit = QLineEdit(self.groupBox_2)
        self.yLineEdit.setObjectName(u"yLineEdit")

        self.gridLayout_2.addWidget(self.yLineEdit, 1, 1, 1, 1)

        self.gridLayout_2.setColumnStretch(0, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(0, 175, 167, 120))
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(167, 120))
        self.gridLayout_3 = QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.alignLButton = QPushButton(self.groupBox_3)
        self.alignLButton.setObjectName(u"alignLButton")
        sizePolicy.setHeightForWidth(self.alignLButton.sizePolicy().hasHeightForWidth())
        self.alignLButton.setSizePolicy(sizePolicy)
        self.alignLButton.setMinimumSize(QSize(45, 45))
        self.alignLButton.setMaximumSize(QSize(45, 45))
        self.alignLButton.setFont(font)
        self.alignLButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_3.addWidget(self.alignLButton, 0, 0, 1, 1)

        self.alignVCButton = QPushButton(self.groupBox_3)
        self.alignVCButton.setObjectName(u"alignVCButton")
        sizePolicy.setHeightForWidth(self.alignVCButton.sizePolicy().hasHeightForWidth())
        self.alignVCButton.setSizePolicy(sizePolicy)
        self.alignVCButton.setMinimumSize(QSize(45, 45))
        self.alignVCButton.setMaximumSize(QSize(45, 45))
        font1 = QFont()
        font1.setFamilies([u"\u30e1\u30a4\u30ea\u30aa"])
        font1.setPointSize(16)
        font1.setBold(False)
        font1.setItalic(False)
        self.alignVCButton.setFont(font1)
        self.alignVCButton.setStyleSheet(u"font: 16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_3.addWidget(self.alignVCButton, 0, 1, 1, 1)

        self.alignRButton = QPushButton(self.groupBox_3)
        self.alignRButton.setObjectName(u"alignRButton")
        sizePolicy.setHeightForWidth(self.alignRButton.sizePolicy().hasHeightForWidth())
        self.alignRButton.setSizePolicy(sizePolicy)
        self.alignRButton.setMinimumSize(QSize(45, 45))
        self.alignRButton.setMaximumSize(QSize(45, 45))
        self.alignRButton.setFont(font)
        self.alignRButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_3.addWidget(self.alignRButton, 0, 2, 1, 1)

        self.alignTButton = QPushButton(self.groupBox_3)
        self.alignTButton.setObjectName(u"alignTButton")
        sizePolicy.setHeightForWidth(self.alignTButton.sizePolicy().hasHeightForWidth())
        self.alignTButton.setSizePolicy(sizePolicy)
        self.alignTButton.setMinimumSize(QSize(45, 45))
        self.alignTButton.setMaximumSize(QSize(45, 45))
        self.alignTButton.setFont(font)
        self.alignTButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_3.addWidget(self.alignTButton, 1, 0, 1, 1)

        self.alignHCButton = QPushButton(self.groupBox_3)
        self.alignHCButton.setObjectName(u"alignHCButton")
        sizePolicy.setHeightForWidth(self.alignHCButton.sizePolicy().hasHeightForWidth())
        self.alignHCButton.setSizePolicy(sizePolicy)
        self.alignHCButton.setMinimumSize(QSize(45, 45))
        self.alignHCButton.setMaximumSize(QSize(45, 45))
        self.alignHCButton.setFont(font1)
        self.alignHCButton.setStyleSheet(u"font: 16pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_3.addWidget(self.alignHCButton, 1, 1, 1, 1)

        self.alignBButton = QPushButton(self.groupBox_3)
        self.alignBButton.setObjectName(u"alignBButton")
        sizePolicy.setHeightForWidth(self.alignBButton.sizePolicy().hasHeightForWidth())
        self.alignBButton.setSizePolicy(sizePolicy)
        self.alignBButton.setMinimumSize(QSize(45, 45))
        self.alignBButton.setMaximumSize(QSize(45, 45))
        self.alignBButton.setFont(font)
        self.alignBButton.setStyleSheet(u"font:24pt \"\u30e1\u30a4\u30ea\u30aa\";")

        self.gridLayout_3.addWidget(self.alignBButton, 1, 2, 1, 1)


        self.verticalLayout_2.addWidget(self.widget)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.xIsLockCheckBox = QCheckBox(self.centralwidget)
        self.xIsLockCheckBox.setObjectName(u"xIsLockCheckBox")

        self.horizontalLayout_3.addWidget(self.xIsLockCheckBox)

        self.yIsLockCheckBox = QCheckBox(self.centralwidget)
        self.yIsLockCheckBox.setObjectName(u"yIsLockCheckBox")

        self.horizontalLayout_3.addWidget(self.yIsLockCheckBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
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


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle("")
        self.groupBox_2.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.setButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.groupBox_3.setTitle("")
        self.alignLButton.setText(QCoreApplication.translate("MainWindow", u"\u21e4", None))
        self.alignVCButton.setText(QCoreApplication.translate("MainWindow", u"\u2503", None))
        self.alignRButton.setText(QCoreApplication.translate("MainWindow", u"\u21e5", None))
        self.alignTButton.setText(QCoreApplication.translate("MainWindow", u"\u2912", None))
        self.alignHCButton.setText(QCoreApplication.translate("MainWindow", u"\u2501", None))
        self.alignBButton.setText(QCoreApplication.translate("MainWindow", u"\u2913", None))
        self.xIsLockCheckBox.setText(QCoreApplication.translate("MainWindow", u"Lock X", None))
        self.yIsLockCheckBox.setText(QCoreApplication.translate("MainWindow", u"Lock Y", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


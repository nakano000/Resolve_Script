# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nudge_tool.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QGridLayout, QHBoxLayout,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(179, 271)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.zero2RadioButton = QRadioButton(self.centralwidget)
        self.zero2RadioButton.setObjectName(u"zero2RadioButton")
        self.zero2RadioButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.zero2RadioButton)

        self.zero3RadioButton = QRadioButton(self.centralwidget)
        self.zero3RadioButton.setObjectName(u"zero3RadioButton")

        self.horizontalLayout_2.addWidget(self.zero3RadioButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.num03Button = QToolButton(self.centralwidget)
        self.num03Button.setObjectName(u"num03Button")

        self.gridLayout.addWidget(self.num03Button, 0, 1, 1, 1)

        self.num08Button = QToolButton(self.centralwidget)
        self.num08Button.setObjectName(u"num08Button")

        self.gridLayout.addWidget(self.num08Button, 1, 3, 1, 1)

        self.num06Button = QToolButton(self.centralwidget)
        self.num06Button.setObjectName(u"num06Button")

        self.gridLayout.addWidget(self.num06Button, 1, 2, 1, 1)

        self.num05Button = QToolButton(self.centralwidget)
        self.num05Button.setObjectName(u"num05Button")

        self.gridLayout.addWidget(self.num05Button, 0, 2, 1, 1)

        self.num09Button = QToolButton(self.centralwidget)
        self.num09Button.setObjectName(u"num09Button")

        self.gridLayout.addWidget(self.num09Button, 0, 4, 1, 1)

        self.num10Button = QToolButton(self.centralwidget)
        self.num10Button.setObjectName(u"num10Button")

        self.gridLayout.addWidget(self.num10Button, 1, 4, 1, 1)

        self.num01Button = QToolButton(self.centralwidget)
        self.num01Button.setObjectName(u"num01Button")

        self.gridLayout.addWidget(self.num01Button, 0, 0, 1, 1)

        self.num07Button = QToolButton(self.centralwidget)
        self.num07Button.setObjectName(u"num07Button")

        self.gridLayout.addWidget(self.num07Button, 0, 3, 1, 1)

        self.num04Button = QToolButton(self.centralwidget)
        self.num04Button.setObjectName(u"num04Button")

        self.gridLayout.addWidget(self.num04Button, 1, 1, 1, 1)

        self.num02Button = QToolButton(self.centralwidget)
        self.num02Button.setObjectName(u"num02Button")

        self.gridLayout.addWidget(self.num02Button, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 5, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.doubleSpinBox = QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setMinimum(0.001000000000000)
        self.doubleSpinBox.setSingleStep(0.010000000000000)

        self.verticalLayout_2.addWidget(self.doubleSpinBox)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.upButton = QToolButton(self.centralwidget)
        self.upButton.setObjectName(u"upButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upButton.sizePolicy().hasHeightForWidth())
        self.upButton.setSizePolicy(sizePolicy)
        self.upButton.setMinimumSize(QSize(30, 30))
        self.upButton.setArrowType(Qt.UpArrow)

        self.verticalLayout.addWidget(self.upButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.leftButton = QToolButton(self.centralwidget)
        self.leftButton.setObjectName(u"leftButton")
        sizePolicy.setHeightForWidth(self.leftButton.sizePolicy().hasHeightForWidth())
        self.leftButton.setSizePolicy(sizePolicy)
        self.leftButton.setMinimumSize(QSize(30, 30))
        self.leftButton.setArrowType(Qt.LeftArrow)

        self.horizontalLayout.addWidget(self.leftButton)

        self.rightButton = QToolButton(self.centralwidget)
        self.rightButton.setObjectName(u"rightButton")
        sizePolicy.setHeightForWidth(self.rightButton.sizePolicy().hasHeightForWidth())
        self.rightButton.setSizePolicy(sizePolicy)
        self.rightButton.setMinimumSize(QSize(30, 30))
        self.rightButton.setArrowType(Qt.RightArrow)

        self.horizontalLayout.addWidget(self.rightButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.downButton = QToolButton(self.centralwidget)
        self.downButton.setObjectName(u"downButton")
        sizePolicy.setHeightForWidth(self.downButton.sizePolicy().hasHeightForWidth())
        self.downButton.setSizePolicy(sizePolicy)
        self.downButton.setMinimumSize(QSize(30, 30))
        self.downButton.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.downButton)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout_2.addWidget(self.closeButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.zero2RadioButton.setText(QCoreApplication.translate("MainWindow", u"0.0X", None))
        self.zero3RadioButton.setText(QCoreApplication.translate("MainWindow", u"0.00X", None))
        self.num03Button.setText(QCoreApplication.translate("MainWindow", u"3", None))
        self.num08Button.setText(QCoreApplication.translate("MainWindow", u"8", None))
        self.num06Button.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.num05Button.setText(QCoreApplication.translate("MainWindow", u"5", None))
        self.num09Button.setText(QCoreApplication.translate("MainWindow", u"9", None))
        self.num10Button.setText(QCoreApplication.translate("MainWindow", u"10", None))
        self.num01Button.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.num07Button.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.num04Button.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.num02Button.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.upButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.leftButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.rightButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.downButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


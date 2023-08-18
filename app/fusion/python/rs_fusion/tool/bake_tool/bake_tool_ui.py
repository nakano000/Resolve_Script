# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bake_tool.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFormLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QToolButton, QTreeView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(314, 487)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout_3.addWidget(self.treeView)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.connectedCheckBox = QCheckBox(self.groupBox_2)
        self.connectedCheckBox.setObjectName(u"connectedCheckBox")

        self.horizontalLayout_3.addWidget(self.connectedCheckBox)

        self.expressionCheckBox = QCheckBox(self.groupBox_2)
        self.expressionCheckBox.setObjectName(u"expressionCheckBox")

        self.horizontalLayout_3.addWidget(self.expressionCheckBox)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sfSpinBox = QSpinBox(self.groupBox)
        self.sfSpinBox.setObjectName(u"sfSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sfSpinBox.sizePolicy().hasHeightForWidth())
        self.sfSpinBox.setSizePolicy(sizePolicy)
        self.sfSpinBox.setMinimum(-999999999)
        self.sfSpinBox.setMaximum(999999999)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sfSpinBox)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.efSpinBox = QSpinBox(self.groupBox)
        self.efSpinBox.setObjectName(u"efSpinBox")
        sizePolicy.setHeightForWidth(self.efSpinBox.sizePolicy().hasHeightForWidth())
        self.efSpinBox.setSizePolicy(sizePolicy)
        self.efSpinBox.setMinimum(-999999999)
        self.efSpinBox.setMaximum(999999999)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.efSpinBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.globalRangeButton = QPushButton(self.groupBox)
        self.globalRangeButton.setObjectName(u"globalRangeButton")
        self.globalRangeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.globalRangeButton)

        self.renderRangeButton = QPushButton(self.groupBox)
        self.renderRangeButton.setObjectName(u"renderRangeButton")
        self.renderRangeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout.addWidget(self.renderRangeButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.readButton = QPushButton(self.centralwidget)
        self.readButton.setObjectName(u"readButton")
        self.readButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.readButton)

        self.bakeButton = QPushButton(self.centralwidget)
        self.bakeButton.setObjectName(u"bakeButton")
        self.bakeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.bakeButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(30, 30))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout_4.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Option", None))
        self.connectedCheckBox.setText(QCoreApplication.translate("MainWindow", u"Connected", None))
        self.expressionCheckBox.setText(QCoreApplication.translate("MainWindow", u"Expression", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Range", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Start Frame", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"End Frame", None))
        self.globalRangeButton.setText(QCoreApplication.translate("MainWindow", u"Global Range", None))
        self.renderRangeButton.setText(QCoreApplication.translate("MainWindow", u"Render Range", None))
        self.readButton.setText(QCoreApplication.translate("MainWindow", u"read", None))
        self.bakeButton.setText(QCoreApplication.translate("MainWindow", u"bake", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


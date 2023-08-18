# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'copy_tool.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFormLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QToolButton, QTreeView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(314, 452)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.treeView)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.l2rRadioButton = QRadioButton(self.groupBox_3)
        self.l2rRadioButton.setObjectName(u"l2rRadioButton")
        self.l2rRadioButton.setChecked(True)

        self.horizontalLayout_3.addWidget(self.l2rRadioButton)

        self.randomRadioButton = QRadioButton(self.groupBox_3)
        self.randomRadioButton.setObjectName(u"randomRadioButton")

        self.horizontalLayout_3.addWidget(self.randomRadioButton)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.stepLineEdit = QLineEdit(self.groupBox)
        self.stepLineEdit.setObjectName(u"stepLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.stepLineEdit)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.jitterInfLineEdit = QLineEdit(self.groupBox)
        self.jitterInfLineEdit.setObjectName(u"jitterInfLineEdit")

        self.horizontalLayout.addWidget(self.jitterInfLineEdit)

        self.jitterSupLineEdit = QLineEdit(self.groupBox)
        self.jitterSupLineEdit.setObjectName(u"jitterSupLineEdit")

        self.horizontalLayout.addWidget(self.jitterSupLineEdit)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_3)

        self.offsetLineEdit = QLineEdit(self.groupBox)
        self.offsetLineEdit.setObjectName(u"offsetLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.offsetLineEdit)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.sourceButton = QPushButton(self.centralwidget)
        self.sourceButton.setObjectName(u"sourceButton")
        self.sourceButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.sourceButton)

        self.setButton = QPushButton(self.centralwidget)
        self.setButton.setObjectName(u"setButton")
        self.setButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.setButton)

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


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Oder", None))
        self.l2rRadioButton.setText(QCoreApplication.translate("MainWindow", u"LtoR", None))
        self.randomRadioButton.setText(QCoreApplication.translate("MainWindow", u"random", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Animation Shift", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Step", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Jitter", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Offset", None))
        self.sourceButton.setText(QCoreApplication.translate("MainWindow", u"source", None))
        self.setButton.setText(QCoreApplication.translate("MainWindow", u"set", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'importer.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QRadioButton, QSizePolicy,
    QSpacerItem, QSpinBox, QTabWidget, QToolButton,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(285, 500)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.fileGroupBox = QGroupBox(self.centralwidget)
        self.fileGroupBox.setObjectName(u"fileGroupBox")
        self.formLayout = QFormLayout(self.fileGroupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.fileGroupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.jsonLineEdit = QLineEdit(self.fileGroupBox)
        self.jsonLineEdit.setObjectName(u"jsonLineEdit")

        self.horizontalLayout_2.addWidget(self.jsonLineEdit)

        self.jsonToolButton = QToolButton(self.fileGroupBox)
        self.jsonToolButton.setObjectName(u"jsonToolButton")

        self.horizontalLayout_2.addWidget(self.jsonToolButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)


        self.verticalLayout_7.addWidget(self.fileGroupBox)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_2 = QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tatieFormatGroupBox = QGroupBox(self.tab)
        self.tatieFormatGroupBox.setObjectName(u"tatieFormatGroupBox")
        self.verticalLayout_3 = QVBoxLayout(self.tatieFormatGroupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.expRadioButton = QRadioButton(self.tatieFormatGroupBox)
        self.expRadioButton.setObjectName(u"expRadioButton")

        self.verticalLayout_3.addWidget(self.expRadioButton)

        self.connectRadioButton = QRadioButton(self.tatieFormatGroupBox)
        self.connectRadioButton.setObjectName(u"connectRadioButton")

        self.verticalLayout_3.addWidget(self.connectRadioButton)

        self.connectLabelRadioButton = QRadioButton(self.tatieFormatGroupBox)
        self.connectLabelRadioButton.setObjectName(u"connectLabelRadioButton")

        self.verticalLayout_3.addWidget(self.connectLabelRadioButton)

        self.label = QLabel(self.tatieFormatGroupBox)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)


        self.verticalLayout_2.addWidget(self.tatieFormatGroupBox)

        self.connectOptionGroupBox = QGroupBox(self.tab)
        self.connectOptionGroupBox.setObjectName(u"connectOptionGroupBox")
        self.verticalLayout_6 = QVBoxLayout(self.connectOptionGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btnSizeLabel = QLabel(self.connectOptionGroupBox)
        self.btnSizeLabel.setObjectName(u"btnSizeLabel")

        self.horizontalLayout_4.addWidget(self.btnSizeLabel)

        self.btnSizeSpinBox = QDoubleSpinBox(self.connectOptionGroupBox)
        self.btnSizeSpinBox.setObjectName(u"btnSizeSpinBox")

        self.horizontalLayout_4.addWidget(self.btnSizeSpinBox)


        self.verticalLayout_6.addLayout(self.horizontalLayout_4)


        self.verticalLayout_2.addWidget(self.connectOptionGroupBox)

        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.useMaskCheckBox = QCheckBox(self.groupBox)
        self.useMaskCheckBox.setObjectName(u"useMaskCheckBox")

        self.verticalLayout_4.addWidget(self.useMaskCheckBox)

        self.expandGroupBox = QGroupBox(self.groupBox)
        self.expandGroupBox.setObjectName(u"expandGroupBox")
        self.verticalLayout = QVBoxLayout(self.expandGroupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.expandGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.xSpinBox = QSpinBox(self.expandGroupBox)
        self.xSpinBox.setObjectName(u"xSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xSpinBox.sizePolicy().hasHeightForWidth())
        self.xSpinBox.setSizePolicy(sizePolicy)
        self.xSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.xSpinBox.setMaximum(999999999)

        self.horizontalLayout.addWidget(self.xSpinBox)

        self.label_3 = QLabel(self.expandGroupBox)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.ySpinBox = QSpinBox(self.expandGroupBox)
        self.ySpinBox.setObjectName(u"ySpinBox")
        sizePolicy.setHeightForWidth(self.ySpinBox.sizePolicy().hasHeightForWidth())
        self.ySpinBox.setSizePolicy(sizePolicy)
        self.ySpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.ySpinBox.setMaximum(999999999)

        self.horizontalLayout.addWidget(self.ySpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addWidget(self.expandGroupBox)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.tabWidget.addTab(self.tab, "")
        self.tab2 = QWidget()
        self.tab2.setObjectName(u"tab2")
        self.verticalLayout_5 = QVBoxLayout(self.tab2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.useMMCheckBox = QCheckBox(self.tab2)
        self.useMMCheckBox.setObjectName(u"useMMCheckBox")

        self.verticalLayout_5.addWidget(self.useMMCheckBox)

        self.useMask2CheckBox = QCheckBox(self.tab2)
        self.useMask2CheckBox.setObjectName(u"useMask2CheckBox")

        self.verticalLayout_5.addWidget(self.useMask2CheckBox)

        self.verticalSpacer = QSpacerItem(20, 146, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab2, "")

        self.verticalLayout_7.addWidget(self.tabWidget)

        self.verticalSpacer_2 = QSpacerItem(20, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.importButton = QPushButton(self.centralwidget)
        self.importButton.setObjectName(u"importButton")
        self.importButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.importButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.fileGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u30d5\u30a1\u30a4\u30eb", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"JSON", None))
        self.jsonToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.tatieFormatGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u7acb\u3061\u7d75\u5f62\u5f0f", None))
        self.expRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u30a8\u30af\u30b9\u30d7\u30ec\u30c3\u30b7\u30e7\u30f3", None))
        self.connectRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u30b3\u30cd\u30af\u30b7\u30e7\u30f3\u5207\u308a\u66ff\u3048(Page)", None))
        self.connectLabelRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u30b3\u30cd\u30af\u30b7\u30e7\u30f3\u5207\u308a\u66ff\u3048(Label)", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u203b\u30a8\u30af\u30b9\u30d7\u30ec\u30c3\u30b7\u30e7\u30f3\u304c\u5f93\u6765\u306e\u3082\u306e\u3067\u3059\u3002", None))
        self.connectOptionGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u30b3\u30cd\u30af\u30b7\u30e7\u30f3\u5207\u308a\u66ff\u3048\u5f0f\u30aa\u30d7\u30b7\u30e7\u30f3", None))
        self.btnSizeLabel.setText(QCoreApplication.translate("MainWindow", u"\u901a\u5e38\u30dc\u30bf\u30f3 \u30b5\u30a4\u30ba", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Image", None))
        self.useMaskCheckBox.setText(QCoreApplication.translate("MainWindow", u"Use Mask", None))
        self.expandGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u62e1\u5f35 (\u30a2\u30cb\u30e1\u30fc\u30b7\u30e7\u30f3 \u30b9\u30da\u30fc\u30b9\u78ba\u4fdd)", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"X", None))
        self.xSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" px", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Y", None))
        self.ySpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" px", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u7acb\u3061\u7d75", None))
        self.useMMCheckBox.setText(QCoreApplication.translate("MainWindow", u"MultiMerge", None))
        self.useMask2CheckBox.setText(QCoreApplication.translate("MainWindow", u"Use Mask", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QCoreApplication.translate("MainWindow", u"\u901a\u5e38", None))
        self.importButton.setText(QCoreApplication.translate("MainWindow", u"import", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


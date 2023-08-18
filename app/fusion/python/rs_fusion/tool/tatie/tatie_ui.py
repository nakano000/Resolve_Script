# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tatie.ui'
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
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(437, 568)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.openDirButton = QPushButton(self.centralwidget)
        self.openDirButton.setObjectName(u"openDirButton")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openDirButton.sizePolicy().hasHeightForWidth())
        self.openDirButton.setSizePolicy(sizePolicy)
        self.openDirButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_7.addWidget(self.openDirButton)

        self.openSampleButton = QPushButton(self.centralwidget)
        self.openSampleButton.setObjectName(u"openSampleButton")
        self.openSampleButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_7.addWidget(self.openSampleButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.multiplyCheckBox = QCheckBox(self.groupBox)
        self.multiplyCheckBox.setObjectName(u"multiplyCheckBox")

        self.verticalLayout.addWidget(self.multiplyCheckBox)

        self.loaderButton = QPushButton(self.groupBox)
        self.loaderButton.setObjectName(u"loaderButton")
        self.loaderButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout.addWidget(self.loaderButton)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.addPoseToolsButton = QPushButton(self.groupBox_5)
        self.addPoseToolsButton.setObjectName(u"addPoseToolsButton")
        self.addPoseToolsButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout_9.addWidget(self.addPoseToolsButton)


        self.verticalLayout_3.addWidget(self.groupBox_5)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.pageNameLineEdit = QLineEdit(self.groupBox_2)
        self.pageNameLineEdit.setObjectName(u"pageNameLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pageNameLineEdit)

        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.ctrlNameLineEdit = QLineEdit(self.groupBox_2)
        self.ctrlNameLineEdit.setObjectName(u"ctrlNameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ctrlNameLineEdit)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.tabWidget = QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_7 = QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.widthSpinBox = QSpinBox(self.groupBox_3)
        self.widthSpinBox.setObjectName(u"widthSpinBox")
        self.widthSpinBox.setMinimumSize(QSize(100, 0))
        self.widthSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.widthSpinBox.setMinimum(1)
        self.widthSpinBox.setMaximum(999999)
        self.widthSpinBox.setDisplayIntegerBase(10)

        self.horizontalLayout.addWidget(self.widthSpinBox)

        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.label_3 = QLabel(self.groupBox_3)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.heightSpinBox = QSpinBox(self.groupBox_3)
        self.heightSpinBox.setObjectName(u"heightSpinBox")
        self.heightSpinBox.setMinimumSize(QSize(100, 0))
        self.heightSpinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.heightSpinBox.setMinimum(1)
        self.heightSpinBox.setMaximum(999999)

        self.horizontalLayout.addWidget(self.heightSpinBox)

        self.horizontalSpacer_4 = QSpacerItem(8, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.verticalLayout_7.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.chkRadioButton = QRadioButton(self.groupBox_4)
        self.chkRadioButton.setObjectName(u"chkRadioButton")

        self.horizontalLayout_4.addWidget(self.chkRadioButton)

        self.cmbRadioButton = QRadioButton(self.groupBox_4)
        self.cmbRadioButton.setObjectName(u"cmbRadioButton")
        self.cmbRadioButton.setChecked(True)

        self.horizontalLayout_4.addWidget(self.cmbRadioButton)

        self.sldRadioButton = QRadioButton(self.groupBox_4)
        self.sldRadioButton.setObjectName(u"sldRadioButton")

        self.horizontalLayout_4.addWidget(self.sldRadioButton)

        self.horizontalSpacer_5 = QSpacerItem(90, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)


        self.verticalLayout_7.addWidget(self.groupBox_4)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)

        self.margeButton = QPushButton(self.tab_2)
        self.margeButton.setObjectName(u"margeButton")
        self.margeButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout_7.addWidget(self.margeButton)

        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.verticalLayout_5 = QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_2 = QSpacerItem(20, 114, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.dissolveButton = QPushButton(self.tab_3)
        self.dissolveButton.setObjectName(u"dissolveButton")
        self.dissolveButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout_5.addWidget(self.dissolveButton)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_4 = QVBoxLayout(self.tab_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.openSiteButton = QPushButton(self.tab_4)
        self.openSiteButton.setObjectName(u"openSiteButton")
        self.openSiteButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout_8.addWidget(self.openSiteButton)

        self.openFuseDirButton = QPushButton(self.tab_4)
        self.openFuseDirButton.setObjectName(u"openFuseDirButton")
        self.openFuseDirButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout_8.addWidget(self.openFuseDirButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)

        self.verticalSpacer = QSpacerItem(20, 66, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.switchButton = QPushButton(self.tab_4)
        self.switchButton.setObjectName(u"switchButton")
        self.switchButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout_4.addWidget(self.switchButton)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.verticalLayout_8 = QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_4 = QSpacerItem(20, 114, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_4)

        self.addButtonButton = QPushButton(self.tab_5)
        self.addButtonButton.setObjectName(u"addButtonButton")
        self.addButtonButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout_8.addWidget(self.addButtonButton)

        self.tabWidget.addTab(self.tab_5, "")

        self.verticalLayout_2.addWidget(self.tabWidget)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(13, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_2.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.openDirButton.setText(QCoreApplication.translate("MainWindow", u"Generators \u30c6\u30f3\u30d7\u30ec\u30fc\u30c8\u30d5\u30a9\u30eb\u30c0\u3092\u958b\u304f", None))
        self.openSampleButton.setText(QCoreApplication.translate("MainWindow", u" \u308a\u305e\u308a\u3077\u3068\u30b5\u30f3\u30d7\u30eb\u30d5\u30a9\u30eb\u30c0\u3092\u958b\u304f ", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f(Loader)", None))
        self.multiplyCheckBox.setText(QCoreApplication.translate("MainWindow", u"Post-Multiply by Alpha", None))
        self.loaderButton.setText(QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"\u7acb\u3061\u7d75\u30de\u30af\u30ed\u7528", None))
        self.addPoseToolsButton.setText(QCoreApplication.translate("MainWindow", u"\u30dd\u30fc\u30ba\u95a2\u9023\u30c4\u30fc\u30eb\u8ffd\u52a0", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5408\u6210", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u30da\u30fc\u30b8\u540d", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u30d1\u30e9\u30e1\u30fc\u30bf\u540d", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"BG", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5e45", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u9ad8\u3055", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u30b3\u30f3\u30c8\u30ed\u30fc\u30e9 \u30bf\u30a4\u30d7", None))
        self.chkRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u30c1\u30a7\u30c3\u30af\u30dc\u30c3\u30af\u30b9", None))
        self.cmbRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u30b3\u30f3\u30dc\u30dc\u30c3\u30af\u30b9", None))
        self.sldRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u30b9\u30e9\u30a4\u30c0\u30fc", None))
        self.margeButton.setText(QCoreApplication.translate("MainWindow", u"\u30de\u30fc\u30b8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u30de\u30fc\u30b8", None))
        self.dissolveButton.setText(QCoreApplication.translate("MainWindow", u"\u30c7\u30a3\u30be\u30eb\u30d6", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u30c7\u30a3\u30be\u30eb\u30d6", None))
        self.openSiteButton.setText(QCoreApplication.translate("MainWindow", u" \u30c0\u30a6\u30f3\u30ed\u30fc\u30c9\u30da\u30fc\u30b8\u3092\u958b\u304f ", None))
        self.openFuseDirButton.setText(QCoreApplication.translate("MainWindow", u" \u30a4\u30f3\u30b9\u30c8\u30fc\u30eb\u30d5\u30a9\u30eb\u30c0\u3092\u958b\u304f ", None))
        self.switchButton.setText(QCoreApplication.translate("MainWindow", u"SwitchFuse", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"SwitchFuse", None))
        self.addButtonButton.setText(QCoreApplication.translate("MainWindow", u"\u30dc\u30bf\u30f3\u5207\u308a\u66ff\u3048", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"\u30dc\u30bf\u30f3\u5207\u308a\u66ff\u3048", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


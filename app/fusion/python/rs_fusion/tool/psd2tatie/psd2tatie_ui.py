# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'psd2tatie.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QTabWidget, QTextEdit, QToolButton, QTreeView,
    QVBoxLayout, QWidget)

from rs.gui.log import LogTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(755, 1046)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionPSD = QAction(MainWindow)
        self.actionPSD.setObjectName(u"actionPSD")
        self.actionGenerators_Dir_User = QAction(MainWindow)
        self.actionGenerators_Dir_User.setObjectName(u"actionGenerators_Dir_User")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.fileGroupBox = QGroupBox(self.centralwidget)
        self.fileGroupBox.setObjectName(u"fileGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileGroupBox.sizePolicy().hasHeightForWidth())
        self.fileGroupBox.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.fileGroupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.fileGroupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.psdLineEdit = QLineEdit(self.fileGroupBox)
        self.psdLineEdit.setObjectName(u"psdLineEdit")

        self.horizontalLayout_2.addWidget(self.psdLineEdit)

        self.psdToolButton = QToolButton(self.fileGroupBox)
        self.psdToolButton.setObjectName(u"psdToolButton")

        self.horizontalLayout_2.addWidget(self.psdToolButton)


        self.formLayout.setLayout(0, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_2)

        self.label_9 = QLabel(self.fileGroupBox)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.dstLineEdit = QLineEdit(self.fileGroupBox)
        self.dstLineEdit.setObjectName(u"dstLineEdit")

        self.horizontalLayout_4.addWidget(self.dstLineEdit)

        self.dstToolButton = QToolButton(self.fileGroupBox)
        self.dstToolButton.setObjectName(u"dstToolButton")

        self.horizontalLayout_4.addWidget(self.dstToolButton)


        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.horizontalLayout_4)

        self.label_10 = QLabel(self.fileGroupBox)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.outputLineEdit = QLineEdit(self.fileGroupBox)
        self.outputLineEdit.setObjectName(u"outputLineEdit")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.outputLineEdit)

        self.label_11 = QLabel(self.fileGroupBox)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.sizeSpinBox = QSpinBox(self.fileGroupBox)
        self.sizeSpinBox.setObjectName(u"sizeSpinBox")
        self.sizeSpinBox.setMinimum(10)
        self.sizeSpinBox.setMaximum(100)
        self.sizeSpinBox.setSingleStep(10)
        self.sizeSpinBox.setValue(100)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.sizeSpinBox)


        self.verticalLayout_2.addLayout(self.formLayout)

        self.clearPngCheckBox = QCheckBox(self.fileGroupBox)
        self.clearPngCheckBox.setObjectName(u"clearPngCheckBox")
        self.clearPngCheckBox.setChecked(True)

        self.verticalLayout_2.addWidget(self.clearPngCheckBox)


        self.verticalLayout_4.addWidget(self.fileGroupBox)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Vertical)
        self.groupBox = QGroupBox(self.splitter)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.treeView = QTreeView(self.groupBox)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.treeView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        self.horizontalLayout_5.addWidget(self.treeView)

        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy1)
        self.scrollArea.setMinimumSize(QSize(300, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 286, 632))
        self.horizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_4 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.setFrontmostButton = QPushButton(self.groupBox_4)
        self.setFrontmostButton.setObjectName(u"setFrontmostButton")
        self.setFrontmostButton.setMinimumSize(QSize(100, 40))
        self.setFrontmostButton.setStyleSheet(u"background: rgb(159, 125, 0); color: rgb(255, 255, 255)")

        self.verticalLayout.addWidget(self.setFrontmostButton)

        self.setEyetButton = QPushButton(self.groupBox_4)
        self.setEyetButton.setObjectName(u"setEyetButton")
        self.setEyetButton.setMinimumSize(QSize(100, 40))
        self.setEyetButton.setStyleSheet(u"background: rgb(0, 114, 184); color: rgb(255, 255, 255)")

        self.verticalLayout.addWidget(self.setEyetButton)

        self.setMouthButton = QPushButton(self.groupBox_4)
        self.setMouthButton.setObjectName(u"setMouthButton")
        self.setMouthButton.setMinimumSize(QSize(100, 40))
        self.setMouthButton.setStyleSheet(u"background: rgb(0, 121, 30); color: rgb(255, 255, 255)")

        self.verticalLayout.addWidget(self.setMouthButton)

        self.setRemoveButton = QPushButton(self.groupBox_4)
        self.setRemoveButton.setObjectName(u"setRemoveButton")
        self.setRemoveButton.setMinimumSize(QSize(100, 40))
        self.setRemoveButton.setStyleSheet(u"background: rgb(104, 104, 104); color: rgb(255, 255, 255)")

        self.verticalLayout.addWidget(self.setRemoveButton)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.clearButton = QPushButton(self.groupBox_4)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout.addWidget(self.clearButton)


        self.verticalLayout_3.addWidget(self.groupBox_4)

        self.groupBox_3 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout = QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)

        self.closeComboBox = QComboBox(self.groupBox_3)
        self.closeComboBox.setObjectName(u"closeComboBox")
        self.closeComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout.addWidget(self.closeComboBox, 0, 1, 1, 1)

        self.setCloseToolButton = QToolButton(self.groupBox_3)
        self.setCloseToolButton.setObjectName(u"setCloseToolButton")

        self.gridLayout.addWidget(self.setCloseToolButton, 0, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.tabWidget = QTabWidget(self.groupBox_2)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_2 = QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.setAToolButton = QToolButton(self.tab)
        self.setAToolButton.setObjectName(u"setAToolButton")

        self.gridLayout_2.addWidget(self.setAToolButton, 0, 2, 1, 1)

        self.setUToolButton = QToolButton(self.tab)
        self.setUToolButton.setObjectName(u"setUToolButton")

        self.gridLayout_2.addWidget(self.setUToolButton, 2, 2, 1, 1)

        self.label_5 = QLabel(self.tab)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)

        self.setIToolButton = QToolButton(self.tab)
        self.setIToolButton.setObjectName(u"setIToolButton")

        self.gridLayout_2.addWidget(self.setIToolButton, 1, 2, 1, 1)

        self.eComboBox = QComboBox(self.tab)
        self.eComboBox.setObjectName(u"eComboBox")
        self.eComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.eComboBox, 3, 1, 1, 1)

        self.setEToolButton = QToolButton(self.tab)
        self.setEToolButton.setObjectName(u"setEToolButton")

        self.gridLayout_2.addWidget(self.setEToolButton, 3, 2, 1, 1)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_2.addWidget(self.label_8, 5, 0, 1, 1)

        self.uComboBox = QComboBox(self.tab)
        self.uComboBox.setObjectName(u"uComboBox")
        self.uComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.uComboBox, 2, 1, 1, 1)

        self.setOToolButton = QToolButton(self.tab)
        self.setOToolButton.setObjectName(u"setOToolButton")

        self.gridLayout_2.addWidget(self.setOToolButton, 4, 2, 1, 1)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_2.addWidget(self.label_6, 4, 0, 1, 1)

        self.aComboBox = QComboBox(self.tab)
        self.aComboBox.setObjectName(u"aComboBox")
        self.aComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.aComboBox, 0, 1, 1, 1)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)

        self.setNToolButton = QToolButton(self.tab)
        self.setNToolButton.setObjectName(u"setNToolButton")

        self.gridLayout_2.addWidget(self.setNToolButton, 5, 2, 1, 1)

        self.nComboBox = QComboBox(self.tab)
        self.nComboBox.setObjectName(u"nComboBox")
        self.nComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.nComboBox, 5, 1, 1, 1)

        self.iComboBox = QComboBox(self.tab)
        self.iComboBox.setObjectName(u"iComboBox")
        self.iComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.iComboBox, 1, 1, 1, 1)

        self.oComboBox = QComboBox(self.tab)
        self.oComboBox.setObjectName(u"oComboBox")
        self.oComboBox.setMinimumSize(QSize(120, 0))

        self.gridLayout_2.addWidget(self.oComboBox, 4, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer_3, 6, 1, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_7.addWidget(self.tabWidget)


        self.verticalLayout_3.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_5.addWidget(self.scrollArea)

        self.splitter.addWidget(self.groupBox)
        self.logGroupBox = QGroupBox(self.splitter)
        self.logGroupBox.setObjectName(u"logGroupBox")
        sizePolicy1.setHeightForWidth(self.logGroupBox.sizePolicy().hasHeightForWidth())
        self.logGroupBox.setSizePolicy(sizePolicy1)
        self.verticalLayout_6 = QVBoxLayout(self.logGroupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.logTextEdit = LogTextEdit(self.logGroupBox)
        self.logTextEdit.setObjectName(u"logTextEdit")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy3)
        self.logTextEdit.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.logTextEdit.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.logTextEdit)

        self.splitter.addWidget(self.logGroupBox)

        self.verticalLayout_4.addWidget(self.splitter)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.convertButton = QPushButton(self.centralwidget)
        self.convertButton.setObjectName(u"convertButton")
        self.convertButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout_3.addWidget(self.convertButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 755, 33))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuDirectory = QMenu(self.menuBar)
        self.menuDirectory.setObjectName(u"menuDirectory")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuDirectory.menuAction())
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuDirectory.addAction(self.actionPSD)
        self.menuDirectory.addAction(self.actionGenerators_Dir_User)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


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
        self.actionPSD.setText(QCoreApplication.translate("MainWindow", u"PSD", None))
        self.actionGenerators_Dir_User.setText(QCoreApplication.translate("MainWindow", u"Generators Dir (User)", None))
        self.fileGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PSD", None))
        self.psdToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"PNG save loc.", None))
        self.dstToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Output Name", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Size", None))
        self.sizeSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u"%", None))
        self.clearPngCheckBox.setText(QCoreApplication.translate("MainWindow", u"Clear old PNG files", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Setting", None))
        self.groupBox_4.setTitle("")
        self.setFrontmostButton.setText(QCoreApplication.translate("MainWindow", u"Frontmost", None))
        self.setEyetButton.setText(QCoreApplication.translate("MainWindow", u"Eye", None))
        self.setMouthButton.setText(QCoreApplication.translate("MainWindow", u"Mouth", None))
        self.setRemoveButton.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Eye", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.setCloseToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Mouth", None))
        self.setAToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.setUToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"E", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"U", None))
        self.setIToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.setEToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"A", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"N", None))
        self.setOToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"O", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"I", None))
        self.setNToolButton.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"AIUEO", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Open", None))
        self.logGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Log", None))
        self.convertButton.setText(QCoreApplication.translate("MainWindow", u"convert", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuDirectory.setTitle(QCoreApplication.translate("MainWindow", u"Directory", None))
    # retranslateUi


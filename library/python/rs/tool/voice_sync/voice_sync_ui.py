# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'voice_sync.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QSplitter, QTabWidget, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

from rs.gui.log import LogTextEdit
from rs.tool.voice_sync.wav_table import View

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(626, 787)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_7 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.formLayout = QFormLayout(self.tab)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.srcLineEdit = QLineEdit(self.tab)
        self.srcLineEdit.setObjectName(u"srcLineEdit")

        self.horizontalLayout_5.addWidget(self.srcLineEdit)

        self.srcToolButton = QToolButton(self.tab)
        self.srcToolButton.setObjectName(u"srcToolButton")

        self.horizontalLayout_5.addWidget(self.srcToolButton)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_5)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.srcLabLineEdit = QLineEdit(self.tab)
        self.srcLabLineEdit.setObjectName(u"srcLabLineEdit")

        self.horizontalLayout_4.addWidget(self.srcLabLineEdit)

        self.srcLabToolButton = QToolButton(self.tab)
        self.srcLabToolButton.setObjectName(u"srcLabToolButton")

        self.horizontalLayout_4.addWidget(self.srcLabToolButton)


        self.formLayout.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_4)

        self.useAutoSetCheckBox = QCheckBox(self.tab)
        self.useAutoSetCheckBox.setObjectName(u"useAutoSetCheckBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.useAutoSetCheckBox)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_7 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lyricsTextEdit = QTextEdit(self.groupBox)
        self.lyricsTextEdit.setObjectName(u"lyricsTextEdit")

        self.verticalLayout_3.addWidget(self.lyricsTextEdit)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_3)

        self.readButton = QPushButton(self.groupBox)
        self.readButton.setObjectName(u"readButton")
        self.readButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_6.addWidget(self.readButton)

        self.copyButton = QPushButton(self.groupBox)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_6.addWidget(self.copyButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)


        self.horizontalLayout_7.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.wavTableView = View(self.groupBox_2)
        self.wavTableView.setObjectName(u"wavTableView")

        self.verticalLayout_4.addWidget(self.wavTableView)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.addButton = QPushButton(self.groupBox_2)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_8.addWidget(self.addButton)

        self.clearButton = QPushButton(self.groupBox_2)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_8.addWidget(self.clearButton)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_7.addWidget(self.groupBox_2)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.splitter.addWidget(self.tabWidget)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_6 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.refLabLineEdit = QLineEdit(self.groupBox_3)
        self.refLabLineEdit.setObjectName(u"refLabLineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refLabLineEdit.sizePolicy().hasHeightForWidth())
        self.refLabLineEdit.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.refLabLineEdit)

        self.refLabToolButton = QToolButton(self.groupBox_3)
        self.refLabToolButton.setObjectName(u"refLabToolButton")

        self.horizontalLayout_2.addWidget(self.refLabToolButton)


        self.formLayout_2.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_4)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.repeatSpinBox = QSpinBox(self.groupBox_3)
        self.repeatSpinBox.setObjectName(u"repeatSpinBox")
        self.repeatSpinBox.setMinimumSize(QSize(80, 0))

        self.horizontalLayout_10.addWidget(self.repeatSpinBox)

        self.excludeEndCheckBox = QCheckBox(self.groupBox_3)
        self.excludeEndCheckBox.setObjectName(u"excludeEndCheckBox")

        self.horizontalLayout_10.addWidget(self.excludeEndCheckBox)


        self.formLayout_2.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_10)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.usePauCompCheckBox = QCheckBox(self.groupBox_3)
        self.usePauCompCheckBox.setObjectName(u"usePauCompCheckBox")

        self.verticalLayout_2.addWidget(self.usePauCompCheckBox)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.useReplaceGroupBox = QGroupBox(self.layoutWidget)
        self.useReplaceGroupBox.setObjectName(u"useReplaceGroupBox")
        self.useReplaceGroupBox.setTitle(u"\u97f3\u7a0b\u3092\u7f6e\u304d\u63db\u3048\u305f\u30d5\u30a1\u30a4\u30eb\u3082\u4f5c\u308b")
        self.useReplaceGroupBox.setCheckable(True)
        self.formLayout_3 = QFormLayout(self.useReplaceGroupBox)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_5 = QLabel(self.useReplaceGroupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.pitchWavLineEdit = QLineEdit(self.useReplaceGroupBox)
        self.pitchWavLineEdit.setObjectName(u"pitchWavLineEdit")

        self.horizontalLayout_11.addWidget(self.pitchWavLineEdit)

        self.pitchWavToolButton = QToolButton(self.useReplaceGroupBox)
        self.pitchWavToolButton.setObjectName(u"pitchWavToolButton")

        self.horizontalLayout_11.addWidget(self.pitchWavToolButton)


        self.formLayout_3.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_11)

        self.label_6 = QLabel(self.useReplaceGroupBox)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.apValueSpinBox = QDoubleSpinBox(self.useReplaceGroupBox)
        self.apValueSpinBox.setObjectName(u"apValueSpinBox")
        self.apValueSpinBox.setMaximum(1.000000000000000)
        self.apValueSpinBox.setValue(1.000000000000000)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.apValueSpinBox)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.replacedWavLineEdit = QLineEdit(self.useReplaceGroupBox)
        self.replacedWavLineEdit.setObjectName(u"replacedWavLineEdit")

        self.horizontalLayout_13.addWidget(self.replacedWavLineEdit)

        self.replacedWavToolButton = QToolButton(self.useReplaceGroupBox)
        self.replacedWavToolButton.setObjectName(u"replacedWavToolButton")

        self.horizontalLayout_13.addWidget(self.replacedWavToolButton)


        self.formLayout_3.setLayout(2, QFormLayout.FieldRole, self.horizontalLayout_13)

        self.replaceWavLabel = QLabel(self.useReplaceGroupBox)
        self.replaceWavLabel.setObjectName(u"replaceWavLabel")

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.replaceWavLabel)


        self.verticalLayout_6.addWidget(self.useReplaceGroupBox)

        self.groupBox_4 = QGroupBox(self.layoutWidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setTitle(u"\u51fa\u529b\u5148")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.dstLineEdit = QLineEdit(self.groupBox_4)
        self.dstLineEdit.setObjectName(u"dstLineEdit")

        self.horizontalLayout.addWidget(self.dstLineEdit)

        self.dstToolButton = QToolButton(self.groupBox_4)
        self.dstToolButton.setObjectName(u"dstToolButton")

        self.horizontalLayout.addWidget(self.dstToolButton)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_6.addWidget(self.groupBox_4)

        self.logGroupBox = QGroupBox(self.layoutWidget)
        self.logGroupBox.setObjectName(u"logGroupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
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


        self.verticalLayout_6.addWidget(self.logGroupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.checkButton = QPushButton(self.layoutWidget)
        self.checkButton.setObjectName(u"checkButton")
        self.checkButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.checkButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.syncButton = QPushButton(self.layoutWidget)
        self.syncButton.setObjectName(u"syncButton")
        self.syncButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.syncButton)

        self.closeButton = QPushButton(self.layoutWidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_3.addWidget(self.closeButton)


        self.verticalLayout_6.addLayout(self.horizontalLayout_3)

        self.splitter.addWidget(self.layoutWidget)

        self.verticalLayout_7.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 626, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)

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
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u58f0(wav)", None))
        self.srcToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u7d20\u30bf\u30a4\u30df\u30f3\u30b0(lab)", None))
        self.srcLabToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.useAutoSetCheckBox.setText(QCoreApplication.translate("MainWindow", u"wav\u3068\u540c\u540d\u306elab\u30d5\u30a1\u30a4\u30eb\u304c\u3042\u308c\u3070\u3001\u540c\u6642\u306b\u8a2d\u5b9a\u3059\u308b\u3002", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Talk", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u6b4c\u8a5e", None))
        self.readButton.setText(QCoreApplication.translate("MainWindow", u"read", None))
        self.copyButton.setText(QCoreApplication.translate("MainWindow", u"copy", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u30d5\u30a1\u30a4\u30eb", None))
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"add", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Song", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u30ea\u30d5\u30a1\u30ec\u30f3\u30b9", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u5909\u63db\u30bf\u30a4\u30df\u30f3\u30b0 (lab)", None))
        self.refLabToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6bcd\u97f3\u3092\u7e70\u308a\u8fd4\u3059", None))
        self.excludeEndCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u4f11\u7b26\u306e\u524d\u3067\u306f\u7e70\u308a\u8fd4\u3055\u306a\u3044\u3002", None))
        self.usePauCompCheckBox.setText(QCoreApplication.translate("MainWindow", u"pau(\u4f11\u7b26)\u3001sil(\u5168\u4f11\u7b26)\u3001br(\u606f\u7d99\u304e)\u304c\u4e26\u3093\u3067\u3044\u305f\u3089\u3001\u4e00\u3064\u306epau\u306b\u3059\u308b\u3002", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u97f3\u7a0b(wav)", None))
        self.pitchWavToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u96d1\u5473(aperiodicity)", None))
        self.replacedWavToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.replaceWavLabel.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u5148", None))
        self.dstToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.logGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u30ed\u30b0", None))
        self.checkButton.setText(QCoreApplication.translate("MainWindow", u"check", None))
        self.syncButton.setText(QCoreApplication.translate("MainWindow", u"sync", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


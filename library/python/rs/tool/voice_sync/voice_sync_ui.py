# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\voice_sync\voice_sync.ui',
# licensing of 'C:\Users\yoshi\PycharmProjects\Resolve_Script\library\python\rs\tool\voice_sync\voice_sync.ui' applies.
#
# Created: Thu Jun 29 04:32:32 2023
#      by: pyside2-uic  running on PySide2 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(774, 492)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.srcLineEdit = QtWidgets.QLineEdit(self.tab)
        self.srcLineEdit.setObjectName("srcLineEdit")
        self.horizontalLayout_5.addWidget(self.srcLineEdit)
        self.srcToolButton = QtWidgets.QToolButton(self.tab)
        self.srcToolButton.setObjectName("srcToolButton")
        self.horizontalLayout_5.addWidget(self.srcToolButton)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.srcLabLineEdit = QtWidgets.QLineEdit(self.tab)
        self.srcLabLineEdit.setObjectName("srcLabLineEdit")
        self.horizontalLayout_4.addWidget(self.srcLabLineEdit)
        self.srcLabToolButton = QtWidgets.QToolButton(self.tab)
        self.srcLabToolButton.setObjectName("srcLabToolButton")
        self.horizontalLayout_4.addWidget(self.srcLabToolButton)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.useAutoSetCheckBox = QtWidgets.QCheckBox(self.tab)
        self.useAutoSetCheckBox.setObjectName("useAutoSetCheckBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.useAutoSetCheckBox)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lyricsTextEdit = QtWidgets.QTextEdit(self.groupBox)
        self.lyricsTextEdit.setObjectName("lyricsTextEdit")
        self.verticalLayout_3.addWidget(self.lyricsTextEdit)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.readButton = QtWidgets.QPushButton(self.groupBox)
        self.readButton.setMinimumSize(QtCore.QSize(80, 30))
        self.readButton.setObjectName("readButton")
        self.horizontalLayout_6.addWidget(self.readButton)
        self.copyButton = QtWidgets.QPushButton(self.groupBox)
        self.copyButton.setMinimumSize(QtCore.QSize(80, 30))
        self.copyButton.setObjectName("copyButton")
        self.horizontalLayout_6.addWidget(self.copyButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.wavTableView = View(self.groupBox_2)
        self.wavTableView.setObjectName("wavTableView")
        self.verticalLayout_4.addWidget(self.wavTableView)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.addButton = QtWidgets.QPushButton(self.groupBox_2)
        self.addButton.setMinimumSize(QtCore.QSize(80, 30))
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_8.addWidget(self.addButton)
        self.clearButton = QtWidgets.QPushButton(self.groupBox_2)
        self.clearButton.setMinimumSize(QtCore.QSize(80, 30))
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout_8.addWidget(self.clearButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_7.addWidget(self.groupBox_2)
        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.refLabLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refLabLineEdit.sizePolicy().hasHeightForWidth())
        self.refLabLineEdit.setSizePolicy(sizePolicy)
        self.refLabLineEdit.setObjectName("refLabLineEdit")
        self.horizontalLayout_2.addWidget(self.refLabLineEdit)
        self.refLabToolButton = QtWidgets.QToolButton(self.centralwidget)
        self.refLabToolButton.setObjectName("refLabToolButton")
        self.horizontalLayout_2.addWidget(self.refLabToolButton)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.destLabel = QtWidgets.QLabel(self.centralwidget)
        self.destLabel.setObjectName("destLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.destLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dstLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.dstLineEdit.setObjectName("dstLineEdit")
        self.horizontalLayout.addWidget(self.dstLineEdit)
        self.dstToolButton = QtWidgets.QToolButton(self.centralwidget)
        self.dstToolButton.setObjectName("dstToolButton")
        self.horizontalLayout.addWidget(self.dstToolButton)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.logGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.logGroupBox.sizePolicy().hasHeightForWidth())
        self.logGroupBox.setSizePolicy(sizePolicy)
        self.logGroupBox.setObjectName("logGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.logGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.logTextEdit = LogTextEdit(self.logGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logTextEdit.sizePolicy().hasHeightForWidth())
        self.logTextEdit.setSizePolicy(sizePolicy)
        self.logTextEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setObjectName("logTextEdit")
        self.verticalLayout.addWidget(self.logTextEdit)
        self.verticalLayout_2.addWidget(self.logGroupBox)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setMinimumSize(QtCore.QSize(80, 30))
        self.checkButton.setObjectName("checkButton")
        self.horizontalLayout_3.addWidget(self.checkButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.syncButton = QtWidgets.QPushButton(self.centralwidget)
        self.syncButton.setMinimumSize(QtCore.QSize(80, 30))
        self.syncButton.setObjectName("syncButton")
        self.horizontalLayout_3.addWidget(self.syncButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setMinimumSize(QtCore.QSize(80, 30))
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_3.addWidget(self.closeButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "音声(wav)", None, -1))
        self.srcToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "音素タイミング(lab)", None, -1))
        self.srcLabToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.useAutoSetCheckBox.setText(QtWidgets.QApplication.translate("MainWindow", "wavと同名のlabファイルがあれば、同時に設定する。", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtWidgets.QApplication.translate("MainWindow", "Talk", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "歌詞", None, -1))
        self.readButton.setText(QtWidgets.QApplication.translate("MainWindow", "read", None, -1))
        self.copyButton.setText(QtWidgets.QApplication.translate("MainWindow", "copy", None, -1))
        self.groupBox_2.setTitle(QtWidgets.QApplication.translate("MainWindow", "ファイル", None, -1))
        self.addButton.setText(QtWidgets.QApplication.translate("MainWindow", "add", None, -1))
        self.clearButton.setText(QtWidgets.QApplication.translate("MainWindow", "clear", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtWidgets.QApplication.translate("MainWindow", "Song", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "変換タイミング (lab)", None, -1))
        self.refLabToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.destLabel.setText(QtWidgets.QApplication.translate("MainWindow", "出力先", None, -1))
        self.dstToolButton.setText(QtWidgets.QApplication.translate("MainWindow", "...", None, -1))
        self.logGroupBox.setTitle(QtWidgets.QApplication.translate("MainWindow", "ログ", None, -1))
        self.checkButton.setText(QtWidgets.QApplication.translate("MainWindow", "check", None, -1))
        self.syncButton.setText(QtWidgets.QApplication.translate("MainWindow", "sync", None, -1))
        self.closeButton.setText(QtWidgets.QApplication.translate("MainWindow", "close", None, -1))

from rs.gui.log import LogTextEdit
from rs.tool.voice_sync.wav_table import View

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'make_macro.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

from rs_fusion.tool.make_macro.macro_table import View

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(765, 909)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave_As = QAction(MainWindow)
        self.actionSave_As.setObjectName(u"actionSave_As")
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName(u"actionNew")
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.treeView = QTreeView(self.layoutWidget)
        self.treeView.setObjectName(u"treeView")
        self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalLayout_5.addWidget(self.treeView)

        self.addNodeToolButton = QToolButton(self.layoutWidget)
        self.addNodeToolButton.setObjectName(u"addNodeToolButton")
        self.addNodeToolButton.setMinimumSize(QSize(30, 100))
        self.addNodeToolButton.setArrowType(Qt.RightArrow)

        self.horizontalLayout_5.addWidget(self.addNodeToolButton)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.nameLineEdit = QLineEdit(self.layoutWidget1)
        self.nameLineEdit.setObjectName(u"nameLineEdit")

        self.horizontalLayout_6.addWidget(self.nameLineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.useGroupCheckBox = QCheckBox(self.layoutWidget1)
        self.useGroupCheckBox.setObjectName(u"useGroupCheckBox")

        self.verticalLayout.addWidget(self.useGroupCheckBox)

        self.groupBox_3 = QGroupBox(self.layoutWidget1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.mainOutputTableView = View(self.groupBox_3)
        self.mainOutputTableView.setObjectName(u"mainOutputTableView")
        self.mainOutputTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.horizontalLayout_3.addWidget(self.mainOutputTableView)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.layoutWidget1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.mainInputTableView = View(self.groupBox_2)
        self.mainInputTableView.setObjectName(u"mainInputTableView")
        self.mainInputTableView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.horizontalLayout_2.addWidget(self.mainInputTableView)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.layoutWidget1)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.inputTableView = View(self.groupBox)
        self.inputTableView.setObjectName(u"inputTableView")
        self.inputTableView.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)

        self.horizontalLayout.addWidget(self.inputTableView)


        self.verticalLayout.addWidget(self.groupBox)

        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 2)
        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout_2.addWidget(self.splitter)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.readButton = QPushButton(self.centralwidget)
        self.readButton.setObjectName(u"readButton")
        self.readButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.readButton)

        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.clearButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.saveMacroFromJSONButton = QPushButton(self.centralwidget)
        self.saveMacroFromJSONButton.setObjectName(u"saveMacroFromJSONButton")
        self.saveMacroFromJSONButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.saveMacroFromJSONButton)

        self.saveMacroButton = QPushButton(self.centralwidget)
        self.saveMacroButton.setObjectName(u"saveMacroButton")
        self.saveMacroButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.saveMacroButton)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.minimizeButton = QToolButton(self.centralwidget)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(30, 30))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout_4.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.horizontalLayout_4.addWidget(self.closeButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 765, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave_As.setText(QCoreApplication.translate("MainWindow", u"Save As", None))
#if QT_CONFIG(shortcut)
        self.actionSave_As.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
#if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
#if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.addNodeToolButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Macro Name", None))
        self.useGroupCheckBox.setText(QCoreApplication.translate("MainWindow", u"Group\u3068\u3057\u3066\u4fdd\u5b58", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Main Outputs", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Main Inputs", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Inputs", None))
        self.readButton.setText(QCoreApplication.translate("MainWindow", u"\u8aad\u307f\u8fbc\u307f", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"\u30af\u30ea\u30a2", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Make Macro:", None))
        self.saveMacroFromJSONButton.setText(QCoreApplication.translate("MainWindow", u"JSON\u3068\u540c\u3058\u5834\u6240\u306b\u4fdd\u5b58", None))
        self.saveMacroButton.setText(QCoreApplication.translate("MainWindow", u"Resoleve\u7528\u306b\u4fdd\u5b58", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


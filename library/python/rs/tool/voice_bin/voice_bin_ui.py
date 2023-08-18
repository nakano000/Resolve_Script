# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'voice_bin.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDoubleSpinBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QToolButton,
    QTreeView, QVBoxLayout, QWidget)

from rs.tool.voice_bin.drag_button import DragButton

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(489, 696)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.stTab = QWidget()
        self.stTab.setObjectName(u"stTab")
        self.verticalLayout = QVBoxLayout(self.stTab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.treeView = QTreeView(self.stTab)
        self.treeView.setObjectName(u"treeView")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy)
        self.treeView.setMinimumSize(QSize(350, 0))
        self.treeView.setDragEnabled(True)
        self.treeView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.treeView)

        self.tabWidget.addTab(self.stTab, "")
        self.textTab = QWidget()
        self.textTab.setObjectName(u"textTab")
        self.verticalLayout_4 = QVBoxLayout(self.textTab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.dragButton = DragButton(self.textTab)
        self.dragButton.setObjectName(u"dragButton")
        self.dragButton.setMinimumSize(QSize(100, 100))

        self.horizontalLayout_3.addWidget(self.dragButton)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.tatieDragButton = DragButton(self.textTab)
        self.tatieDragButton.setObjectName(u"tatieDragButton")
        self.tatieDragButton.setMinimumSize(QSize(100, 100))

        self.horizontalLayout_3.addWidget(self.tatieDragButton)

        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.wDragButton = DragButton(self.textTab)
        self.wDragButton.setObjectName(u"wDragButton")
        self.wDragButton.setMinimumSize(QSize(100, 100))

        self.horizontalLayout_3.addWidget(self.wDragButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_2 = QLabel(self.textTab)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_4.addWidget(self.label_2)

        self.fpsSpinBox = QDoubleSpinBox(self.textTab)
        self.fpsSpinBox.setObjectName(u"fpsSpinBox")
        self.fpsSpinBox.setMinimum(0.100000000000000)
        self.fpsSpinBox.setMaximum(999.990000000000009)
        self.fpsSpinBox.setValue(30.000000000000000)

        self.horizontalLayout_4.addWidget(self.fpsSpinBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.charaButton = QPushButton(self.textTab)
        self.charaButton.setObjectName(u"charaButton")

        self.verticalLayout_2.addWidget(self.charaButton)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.wavTreeView = QTreeView(self.textTab)
        self.wavTreeView.setObjectName(u"wavTreeView")
        sizePolicy.setHeightForWidth(self.wavTreeView.sizePolicy().hasHeightForWidth())
        self.wavTreeView.setSizePolicy(sizePolicy)
        self.wavTreeView.setMinimumSize(QSize(350, 0))
        self.wavTreeView.setDragEnabled(True)

        self.verticalLayout_4.addWidget(self.wavTreeView)

        self.tabWidget.addTab(self.textTab, "")

        self.verticalLayout_3.addWidget(self.tabWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.folderLineEdit = QLineEdit(Form)
        self.folderLineEdit.setObjectName(u"folderLineEdit")

        self.horizontalLayout_2.addWidget(self.folderLineEdit)

        self.folderToolButton = QToolButton(Form)
        self.folderToolButton.setObjectName(u"folderToolButton")

        self.horizontalLayout_2.addWidget(self.folderToolButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rebuildButton = QPushButton(Form)
        self.rebuildButton.setObjectName(u"rebuildButton")
        self.rebuildButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.rebuildButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.minimizeButton = QToolButton(Form)
        self.minimizeButton.setObjectName(u"minimizeButton")
        self.minimizeButton.setMinimumSize(QSize(40, 40))
        self.minimizeButton.setArrowType(Qt.DownArrow)

        self.horizontalLayout.addWidget(self.minimizeButton)

        self.closeButton = QPushButton(Form)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 40))

        self.horizontalLayout.addWidget(self.closeButton)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stTab), QCoreApplication.translate("Form", u"\u5b57\u5e55", None))
        self.dragButton.setText(QCoreApplication.translate("Form", u" TEXT+", None))
        self.tatieDragButton.setText(QCoreApplication.translate("Form", u" \u7acb\u3061\u7d75", None))
        self.wDragButton.setText(QCoreApplication.translate("Form", u" TEXT+\n"
" \u7acb\u3061\u7d75", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"FPS", None))
        self.charaButton.setText(QCoreApplication.translate("Form", u"\u30ad\u30e3\u30e9\u30af\u30bf\u30fc\u8a2d\u5b9a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.textTab), QCoreApplication.translate("Form", u"\u30c6\u30ad\u30b9\u30c8+ \u7acb\u3061\u7d75", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u58f0\u30d5\u30a9\u30eb\u30c0: ", None))
        self.folderToolButton.setText(QCoreApplication.translate("Form", u"...", None))
        self.rebuildButton.setText(QCoreApplication.translate("Form", u"Rebuild", None))
#if QT_CONFIG(tooltip)
        self.minimizeButton.setToolTip(QCoreApplication.translate("Form", u"\u6700\u5c0f\u5316", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeButton.setText(QCoreApplication.translate("Form", u"...", None))
#if QT_CONFIG(tooltip)
        self.closeButton.setToolTip(QCoreApplication.translate("Form", u"\u9589\u3058\u308b", None))
#endif // QT_CONFIG(tooltip)
        self.closeButton.setText(QCoreApplication.translate("Form", u"close", None))
    # retranslateUi


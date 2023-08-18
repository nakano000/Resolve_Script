# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_form.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListView, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QSplitter,
    QVBoxLayout, QWidget)

from rs.tool.script_launcher.preset_form.drag_button import DragButton

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(552, 459)
        self.verticalLayout_5 = QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.splitter_2 = QSplitter(Form)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.groupBox = QGroupBox(self.splitter_2)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.splitter = QSplitter(self.groupBox)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Horizontal)
        self.dirListView = QListView(self.splitter)
        self.dirListView.setObjectName(u"dirListView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.dirListView.sizePolicy().hasHeightForWidth())
        self.dirListView.setSizePolicy(sizePolicy1)
        self.dirListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.splitter.addWidget(self.dirListView)
        self.fileListView = QListView(self.splitter)
        self.fileListView.setObjectName(u"fileListView")
        self.fileListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.splitter.addWidget(self.fileListView)

        self.verticalLayout_4.addWidget(self.splitter)

        self.splitter_2.addWidget(self.groupBox)
        self.layoutWidget = QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_3 = QGroupBox(self.layoutWidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.applyButton = DragButton(self.groupBox_3)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setMinimumSize(QSize(100, 100))

        self.verticalLayout_2.addWidget(self.applyButton)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.groupBox_3)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.trackIndexSpinBox = QSpinBox(self.groupBox_3)
        self.trackIndexSpinBox.setObjectName(u"trackIndexSpinBox")
        self.trackIndexSpinBox.setMinimum(1)
        self.trackIndexSpinBox.setValue(1)

        self.horizontalLayout_2.addWidget(self.trackIndexSpinBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.closeButton = QPushButton(self.layoutWidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(100, 40))

        self.verticalLayout_3.addWidget(self.closeButton)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.groupBox_2 = QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.filterListView = QListView(self.groupBox_2)
        self.filterListView.setObjectName(u"filterListView")
        self.filterListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.filterListView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.filterNameLineEdit = QLineEdit(self.groupBox_2)
        self.filterNameLineEdit.setObjectName(u"filterNameLineEdit")

        self.horizontalLayout.addWidget(self.filterNameLineEdit)

        self.addFilterButton = QPushButton(self.groupBox_2)
        self.addFilterButton.setObjectName(u"addFilterButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.addFilterButton.sizePolicy().hasHeightForWidth())
        self.addFilterButton.setSizePolicy(sizePolicy2)
        self.addFilterButton.setMinimumSize(QSize(0, 0))
        self.addFilterButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.addFilterButton)

        self.renameButton = QPushButton(self.groupBox_2)
        self.renameButton.setObjectName(u"renameButton")
        sizePolicy2.setHeightForWidth(self.renameButton.sizePolicy().hasHeightForWidth())
        self.renameButton.setSizePolicy(sizePolicy2)
        self.renameButton.setMinimumSize(QSize(40, 0))
        self.renameButton.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout.addWidget(self.renameButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.editFilterButton = QPushButton(self.groupBox_2)
        self.editFilterButton.setObjectName(u"editFilterButton")

        self.verticalLayout.addWidget(self.editFilterButton)


        self.horizontalLayout_3.addWidget(self.groupBox_2)

        self.splitter_2.addWidget(self.layoutWidget)

        self.verticalLayout_5.addWidget(self.splitter_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Setting File", None))
        self.groupBox_3.setTitle("")
        self.applyButton.setText(QCoreApplication.translate("Form", u" Apply", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u30c8\u30e9\u30c3\u30af\u756a\u53f7", None))
        self.closeButton.setText(QCoreApplication.translate("Form", u"close", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Filter", None))
        self.addFilterButton.setText(QCoreApplication.translate("Form", u"add", None))
        self.renameButton.setText(QCoreApplication.translate("Form", u"rename", None))
        self.editFilterButton.setText(QCoreApplication.translate("Form", u"edit", None))
    # retranslateUi


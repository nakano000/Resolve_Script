# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'path_mapper.ui'
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(98, 120)
        self.actionauto = QAction(MainWindow)
        self.actionauto.setObjectName(u"actionauto")
        self.actionauto.setCheckable(True)
        self.actionja = QAction(MainWindow)
        self.actionja.setObjectName(u"actionja")
        self.actionja.setCheckable(True)
        self.actionen = QAction(MainWindow)
        self.actionen.setObjectName(u"actionen")
        self.actionen.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.applyButton = QPushButton(self.centralwidget)
        self.applyButton.setObjectName(u"applyButton")
        self.applyButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout.addWidget(self.applyButton)

        self.removeButton = QPushButton(self.centralwidget)
        self.removeButton.setObjectName(u"removeButton")
        self.removeButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout.addWidget(self.removeButton)

        self.closeButton = QPushButton(self.centralwidget)
        self.closeButton.setObjectName(u"closeButton")
        self.closeButton.setMinimumSize(QSize(80, 30))

        self.verticalLayout.addWidget(self.closeButton)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionauto.setText(QCoreApplication.translate("MainWindow", u"auto", None))
        self.actionja.setText(QCoreApplication.translate("MainWindow", u"ja", None))
        self.actionen.setText(QCoreApplication.translate("MainWindow", u"en", None))
        self.applyButton.setText(QCoreApplication.translate("MainWindow", u"\u9069\u7528", None))
        self.removeButton.setText(QCoreApplication.translate("MainWindow", u"\u53d6\u308a\u9664\u304f", None))
        self.closeButton.setText(QCoreApplication.translate("MainWindow", u"close", None))
    # retranslateUi


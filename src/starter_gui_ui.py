# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'starter_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(463, 170)
        self.gridLayoutWidget = QWidget(Dialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 30, 361, 100))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.gridLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.filename_label = QLabel(self.gridLayoutWidget)
        self.filename_label.setObjectName(u"filename_label")

        self.verticalLayout_2.addWidget(self.filename_label)


        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.select_button = QPushButton(self.gridLayoutWidget)
        self.select_button.setObjectName(u"select_button")

        self.gridLayout.addWidget(self.select_button, 0, 1, 1, 1)

        self.warnings = QLabel(self.gridLayoutWidget)
        self.warnings.setObjectName(u"warnings")

        self.gridLayout.addWidget(self.warnings, 1, 0, 1, 1)

        self.apply_button = QPushButton(Dialog)
        self.apply_button.setObjectName(u"apply_button")
        self.apply_button.setGeometry(QRect(20, 130, 100, 32))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Select Texture Folder:", None))
        self.filename_label.setText("")
        self.select_button.setText(QCoreApplication.translate("Dialog", u"Select Folder", None))
        self.warnings.setText("")
        self.apply_button.setText(QCoreApplication.translate("Dialog", u"Apply", None))
    # retranslateUi


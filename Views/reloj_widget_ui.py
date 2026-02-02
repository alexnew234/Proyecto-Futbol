# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reloj_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(415, 408)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_horas = QLabel(Form)
        self.label_horas.setObjectName(u"label_horas")
        self.label_horas.setStyleSheet(u"QLabel {\n"
"    color: #E0190B;             /* Verde Ne\u00f3n tipo LCD */\n"
"    background-color: transparent; /* Fondo transparente para ver el negro de atr\u00e1s */\n"
"    font-family: \"Courier New\"; /* Fuente monoespaciada (ancho fijo) */\n"
"    font-weight: bold;\n"
"    font-size:  30px;            /* Tama\u00f1o grande */\n"
"    border: none;               /* Sin bordes individuales */\n"
"}")

        self.horizontalLayout.addWidget(self.label_horas)

        self.label_dos_puntos = QLabel(Form)
        self.label_dos_puntos.setObjectName(u"label_dos_puntos")
        self.label_dos_puntos.setStyleSheet(u"QLabel {\n"
"    color: #E0190B;             /* Verde Ne\u00f3n tipo LCD */\n"
"    background-color: transparent; /* Fondo transparente para ver el negro de atr\u00e1s */\n"
"    font-family: \"Courier New\"; /* Fuente monoespaciada (ancho fijo) */\n"
"    font-weight: bold;\n"
"    font-size: 30px;            /* Tama\u00f1o grande */\n"
"    border: none;               /* Sin bordes individuales */\n"
"}")

        self.horizontalLayout.addWidget(self.label_dos_puntos)

        self.label_minutos = QLabel(Form)
        self.label_minutos.setObjectName(u"label_minutos")
        self.label_minutos.setStyleSheet(u"QLabel {\n"
"    color: #E0190B;             /* Verde Ne\u00f3n tipo LCD */\n"
"    background-color: transparent; /* Fondo transparente para ver el negro de atr\u00e1s */\n"
"    font-family: \"Courier New\"; /* Fuente monoespaciada (ancho fijo) */\n"
"    font-weight: bold;\n"
"    font-size: 30px;            /* Tama\u00f1o grande */\n"
"    border: none;               /* Sin bordes individuales */\n"
"}")

        self.horizontalLayout.addWidget(self.label_minutos)

        self.label_dos_puntos_2 = QLabel(Form)
        self.label_dos_puntos_2.setObjectName(u"label_dos_puntos_2")
        self.label_dos_puntos_2.setStyleSheet(u"QLabel {\n"
"    color: #E0190B;             /* Verde Ne\u00f3n tipo LCD */\n"
"    background-color: transparent; /* Fondo transparente para ver el negro de atr\u00e1s */\n"
"    font-family: \"Courier New\"; /* Fuente monoespaciada (ancho fijo) */\n"
"    font-weight: bold;\n"
"    font-size: 30px;            /* Tama\u00f1o grande */\n"
"    border: none;               /* Sin bordes individuales */\n"
"}")

        self.horizontalLayout.addWidget(self.label_dos_puntos_2)

        self.label_segundos = QLabel(Form)
        self.label_segundos.setObjectName(u"label_segundos")
        self.label_segundos.setStyleSheet(u"QLabel {\n"
"    color: #E0190B;             /* Verde Ne\u00f3n tipo LCD */\n"
"    background-color: transparent; /* Fondo transparente para ver el negro de atr\u00e1s */\n"
"    font-family: \"Courier New\"; /* Fuente monoespaciada (ancho fijo) */\n"
"    font-weight: bold;\n"
"    font-size: 30px;            /* Tama\u00f1o grande */\n"
"    border: none;               /* Sin bordes individuales */\n"
"}")

        self.horizontalLayout.addWidget(self.label_segundos)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_horas.setText(QCoreApplication.translate("Form", u"10", None))
        self.label_dos_puntos.setText(QCoreApplication.translate("Form", u":", None))
        self.label_minutos.setText(QCoreApplication.translate("Form", u"23", None))
        self.label_dos_puntos_2.setText(QCoreApplication.translate("Form", u":", None))
        self.label_segundos.setText(QCoreApplication.translate("Form", u"56", None))
    # retranslateUi


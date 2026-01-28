# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(490, 537)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_nombre_equipo = QLabel(Form)
        self.label_nombre_equipo.setObjectName(u"label_nombre_equipo")

        self.verticalLayout.addWidget(self.label_nombre_equipo, 0, Qt.AlignmentFlag.AlignBottom)

        self.lineEdit_equipo_nombre = QLineEdit(Form)
        self.lineEdit_equipo_nombre.setObjectName(u"lineEdit_equipo_nombre")

        self.verticalLayout.addWidget(self.lineEdit_equipo_nombre, 0, Qt.AlignmentFlag.AlignTop)

        self.label_curso = QLabel(Form)
        self.label_curso.setObjectName(u"label_curso")

        self.verticalLayout.addWidget(self.label_curso, 0, Qt.AlignmentFlag.AlignBottom)

        self.lineEdit_curso = QLineEdit(Form)
        self.lineEdit_curso.setObjectName(u"lineEdit_curso")

        self.verticalLayout.addWidget(self.lineEdit_curso, 0, Qt.AlignmentFlag.AlignTop)

        self.label_camiseta = QLabel(Form)
        self.label_camiseta.setObjectName(u"label_camiseta")

        self.verticalLayout.addWidget(self.label_camiseta, 0, Qt.AlignmentFlag.AlignBottom)

        self.lineEdit_camiseta = QLineEdit(Form)
        self.lineEdit_camiseta.setObjectName(u"lineEdit_camiseta")

        self.verticalLayout.addWidget(self.lineEdit_camiseta)

        self.label_logo = QLabel(Form)
        self.label_logo.setObjectName(u"label_logo")

        self.verticalLayout.addWidget(self.label_logo, 0, Qt.AlignmentFlag.AlignBottom)

        self.label_imagen_vacia = QLabel(Form)
        self.label_imagen_vacia.setObjectName(u"label_imagen_vacia")
        self.label_imagen_vacia.setFrameShape(QFrame.Shape.Box)
        self.label_imagen_vacia.setScaledContents(True)

        self.verticalLayout.addWidget(self.label_imagen_vacia)

        self.pushButton_enviar = QPushButton(Form)
        self.pushButton_enviar.setObjectName(u"pushButton_enviar")

        self.verticalLayout.addWidget(self.pushButton_enviar)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_nombre_equipo.setText(QCoreApplication.translate("Form", u"Nombre del equipo", None))
        self.label_curso.setText(QCoreApplication.translate("Form", u"Curso", None))
        self.label_camiseta.setText(QCoreApplication.translate("Form", u"Color de camiseta", None))
        self.label_logo.setText(QCoreApplication.translate("Form", u"Logo", None))
        self.label_imagen_vacia.setText("")
        self.pushButton_enviar.setText(QCoreApplication.translate("Form", u"Enviar", None))
    # retranslateUi


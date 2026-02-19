# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reports_window.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QDialog, QFormLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_ReportsWindow(object):
    def setupUi(self, ReportsWindow):
        if not ReportsWindow.objectName():
            ReportsWindow.setObjectName(u"ReportsWindow")
        ReportsWindow.resize(860, 600)
        self.verticalLayout = QVBoxLayout(ReportsWindow)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(14, 14, 14, 14)
        self.label_title = QLabel(ReportsWindow)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setStyleSheet(u"font-size: 22px; font-weight: bold; color: #b71c1c;")

        self.verticalLayout.addWidget(self.label_title)

        self.label_desc = QLabel(ReportsWindow)
        self.label_desc.setObjectName(u"label_desc")
        self.label_desc.setStyleSheet(u"color: #b71c1c; font-weight: 600;")
        self.label_desc.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_desc)

        self.groupBox = QGroupBox(ReportsWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_tipo = QLabel(self.groupBox)
        self.label_tipo.setObjectName(u"label_tipo")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_tipo)

        self.combo_report = QComboBox(self.groupBox)
        self.combo_report.addItem("")
        self.combo_report.addItem("")
        self.combo_report.addItem("")
        self.combo_report.setObjectName(u"combo_report")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.combo_report)

        self.label_equipo = QLabel(self.groupBox)
        self.label_equipo.setObjectName(u"label_equipo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_equipo)

        self.combo_equipo = QComboBox(self.groupBox)
        self.combo_equipo.setObjectName(u"combo_equipo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.combo_equipo)

        self.label_jugador = QLabel(self.groupBox)
        self.label_jugador.setObjectName(u"label_jugador")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_jugador)

        self.input_jugador_destacado = QLineEdit(self.groupBox)
        self.input_jugador_destacado.setObjectName(u"input_jugador_destacado")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.input_jugador_destacado)

        self.label_eliminatoria = QLabel(self.groupBox)
        self.label_eliminatoria.setObjectName(u"label_eliminatoria")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_eliminatoria)

        self.combo_eliminatoria = QComboBox(self.groupBox)
        self.combo_eliminatoria.addItem("")
        self.combo_eliminatoria.addItem("")
        self.combo_eliminatoria.addItem("")
        self.combo_eliminatoria.addItem("")
        self.combo_eliminatoria.addItem("")
        self.combo_eliminatoria.setObjectName(u"combo_eliminatoria")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.combo_eliminatoria)

        self.label_fechas = QLabel(self.groupBox)
        self.label_fechas.setObjectName(u"label_fechas")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_fechas)

        self.widget_fechas = QWidget(self.groupBox)
        self.widget_fechas.setObjectName(u"widget_fechas")
        self.horizontalLayout_fechas = QHBoxLayout(self.widget_fechas)
        self.horizontalLayout_fechas.setObjectName(u"horizontalLayout_fechas")
        self.horizontalLayout_fechas.setContentsMargins(0, 0, 0, 0)
        self.chk_fecha_desde = QCheckBox(self.widget_fechas)
        self.chk_fecha_desde.setObjectName(u"chk_fecha_desde")

        self.horizontalLayout_fechas.addWidget(self.chk_fecha_desde)

        self.date_desde = QDateEdit(self.widget_fechas)
        self.date_desde.setObjectName(u"date_desde")
        self.date_desde.setCalendarPopup(True)

        self.horizontalLayout_fechas.addWidget(self.date_desde)

        self.horizontalSpacer = QSpacerItem(12, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_fechas.addItem(self.horizontalSpacer)

        self.chk_fecha_hasta = QCheckBox(self.widget_fechas)
        self.chk_fecha_hasta.setObjectName(u"chk_fecha_hasta")

        self.horizontalLayout_fechas.addWidget(self.chk_fecha_hasta)

        self.date_hasta = QDateEdit(self.widget_fechas)
        self.date_hasta.setObjectName(u"date_hasta")
        self.date_hasta.setCalendarPopup(True)

        self.horizontalLayout_fechas.addWidget(self.date_hasta)


        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.widget_fechas)

        self.label_destino = QLabel(self.groupBox)
        self.label_destino.setObjectName(u"label_destino")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_destino)

        self.widget_destino = QWidget(self.groupBox)
        self.widget_destino.setObjectName(u"widget_destino")
        self.horizontalLayout_destino = QHBoxLayout(self.widget_destino)
        self.horizontalLayout_destino.setObjectName(u"horizontalLayout_destino")
        self.horizontalLayout_destino.setContentsMargins(0, 0, 0, 0)
        self.input_output_dir = QLineEdit(self.widget_destino)
        self.input_output_dir.setObjectName(u"input_output_dir")

        self.horizontalLayout_destino.addWidget(self.input_output_dir)

        self.btn_browse = QPushButton(self.widget_destino)
        self.btn_browse.setObjectName(u"btn_browse")

        self.horizontalLayout_destino.addWidget(self.btn_browse)

        self.btn_open_folder = QPushButton(self.widget_destino)
        self.btn_open_folder.setObjectName(u"btn_open_folder")

        self.horizontalLayout_destino.addWidget(self.btn_open_folder)


        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.widget_destino)

        self.label_opciones = QLabel(self.groupBox)
        self.label_opciones.setObjectName(u"label_opciones")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_opciones)

        self.widget_opciones = QWidget(self.groupBox)
        self.widget_opciones.setObjectName(u"widget_opciones")
        self.horizontalLayout_opciones = QHBoxLayout(self.widget_opciones)
        self.horizontalLayout_opciones.setObjectName(u"horizontalLayout_opciones")
        self.horizontalLayout_opciones.setContentsMargins(0, 0, 0, 0)
        self.chk_export_csv = QCheckBox(self.widget_opciones)
        self.chk_export_csv.setObjectName(u"chk_export_csv")
        self.chk_export_csv.setChecked(True)

        self.horizontalLayout_opciones.addWidget(self.chk_export_csv)

        self.chk_force_native = QCheckBox(self.widget_opciones)
        self.chk_force_native.setObjectName(u"chk_force_native")

        self.horizontalLayout_opciones.addWidget(self.chk_force_native)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_opciones.addItem(self.horizontalSpacer_2)


        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.widget_opciones)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.btn_generar = QPushButton(ReportsWindow)
        self.btn_generar.setObjectName(u"btn_generar")
        self.btn_generar.setStyleSheet(u"QPushButton { background: #b71c1c; color: white; font-weight: bold; padding: 8px 14px; border-radius: 4px; }\n"
"QPushButton:hover { background: #d62828; }")

        self.horizontalLayout_bottom.addWidget(self.btn_generar)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer_3)

        self.lbl_engine = QLabel(ReportsWindow)
        self.lbl_engine.setObjectName(u"lbl_engine")
        self.lbl_engine.setStyleSheet(u"font-weight: bold; color: #b71c1c;")

        self.horizontalLayout_bottom.addWidget(self.lbl_engine)


        self.verticalLayout.addLayout(self.horizontalLayout_bottom)

        self.output_log = QPlainTextEdit(ReportsWindow)
        self.output_log.setObjectName(u"output_log")
        self.output_log.setReadOnly(True)

        self.verticalLayout.addWidget(self.output_log)


        self.retranslateUi(ReportsWindow)

        QMetaObject.connectSlotsByName(ReportsWindow)
    # setupUi

    def retranslateUi(self, ReportsWindow):
        ReportsWindow.setWindowTitle(QCoreApplication.translate("ReportsWindow", u"Centro de Informes", None))
        self.label_title.setText(QCoreApplication.translate("ReportsWindow", u"Informes del Torneo", None))
        self.label_desc.setText(QCoreApplication.translate("ReportsWindow", u"Genera PDF y CSV para Equipos/Jugadores, Partidos/Resultados y Clasificacion/Eliminatorias.", None))
        self.groupBox.setTitle(QCoreApplication.translate("ReportsWindow", u"Configuracion del informe", None))
        self.label_tipo.setText(QCoreApplication.translate("ReportsWindow", u"Tipo de informe:", None))
        self.combo_report.setItemText(0, QCoreApplication.translate("ReportsWindow", u"Informe Equipos y Jugadores", None))
        self.combo_report.setItemText(1, QCoreApplication.translate("ReportsWindow", u"Informe Partidos y Resultados", None))
        self.combo_report.setItemText(2, QCoreApplication.translate("ReportsWindow", u"Informe Clasificacion y Eliminatorias", None))

        self.label_equipo.setText(QCoreApplication.translate("ReportsWindow", u"Equipo (opcional):", None))
        self.label_jugador.setText(QCoreApplication.translate("ReportsWindow", u"Jugador destacado (opcional):", None))
        self.input_jugador_destacado.setPlaceholderText(QCoreApplication.translate("ReportsWindow", u"Nombre o parte del nombre", None))
        self.label_eliminatoria.setText(QCoreApplication.translate("ReportsWindow", u"Eliminatoria (opcional):", None))
        self.combo_eliminatoria.setItemText(0, QCoreApplication.translate("ReportsWindow", u"Todas", None))
        self.combo_eliminatoria.setItemText(1, QCoreApplication.translate("ReportsWindow", u"Octavos", None))
        self.combo_eliminatoria.setItemText(2, QCoreApplication.translate("ReportsWindow", u"Cuartos", None))
        self.combo_eliminatoria.setItemText(3, QCoreApplication.translate("ReportsWindow", u"Semifinal", None))
        self.combo_eliminatoria.setItemText(4, QCoreApplication.translate("ReportsWindow", u"Final", None))

        self.label_fechas.setText(QCoreApplication.translate("ReportsWindow", u"Rango de fechas:", None))
        self.chk_fecha_desde.setText(QCoreApplication.translate("ReportsWindow", u"Desde", None))
        self.chk_fecha_hasta.setText(QCoreApplication.translate("ReportsWindow", u"Hasta", None))
        self.label_destino.setText(QCoreApplication.translate("ReportsWindow", u"Destino PDF/CSV:", None))
        self.btn_browse.setText(QCoreApplication.translate("ReportsWindow", u"Examinar...", None))
        self.btn_open_folder.setText(QCoreApplication.translate("ReportsWindow", u"Abrir carpeta", None))
        self.label_opciones.setText(QCoreApplication.translate("ReportsWindow", u"Opciones:", None))
        self.chk_export_csv.setText(QCoreApplication.translate("ReportsWindow", u"Exportar CSV", None))
        self.chk_force_native.setText(QCoreApplication.translate("ReportsWindow", u"Forzar motor nativo (sin Jasper)", None))
        self.btn_generar.setText(QCoreApplication.translate("ReportsWindow", u"Generar y guardar", None))
        self.lbl_engine.setText(QCoreApplication.translate("ReportsWindow", u"Motor: -", None))
        self.output_log.setPlaceholderText(QCoreApplication.translate("ReportsWindow", u"Estado de la generacion...", None))
    # retranslateUi


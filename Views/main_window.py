from PySide6.QtCore import QCoreApplication, QEvent
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QPushButton

from Views.dashboard_view import DashboardView
from Views.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dashboard = DashboardView()
        self.ui.stackedWidget.insertWidget(0, self.dashboard)
        self.ui.stackedWidget.setCurrentIndex(0)

        if hasattr(self.ui, "toolBar"):
            self.ui.toolBar.setVisible(False)

        self.btn_exportar_csv = QPushButton("", self.ui.page_clasificacion)
        self.btn_exportar_csv.setGeometry(420, 30, 120, 30)
        self.btn_exportar_csv.setStyleSheet(
            """
            background-color: #1E6637;
            color: white;
            font-weight: bold;
            border-radius: 4px;
            """
        )
        self.btn_exportar_csv.setToolTip("")

        barra_menu = self.menuBar()
        barra_menu.clear()

        self.act_equipos_texto = QAction(self)
        barra_menu.addAction(self.act_equipos_texto)

        self.act_participantes_texto = QAction(self)
        barra_menu.addAction(self.act_participantes_texto)

        self.act_partidos_texto = QAction(self)
        barra_menu.addAction(self.act_partidos_texto)

        self.act_clasificacion_texto = QAction(self)
        barra_menu.addAction(self.act_clasificacion_texto)

        self.act_informes_texto = QAction(self)
        barra_menu.addAction(self.act_informes_texto)

        self.act_creditos = QAction(self)
        barra_menu.addAction(self.act_creditos)

        self.act_ayuda = QAction(self)
        barra_menu.addAction(self.act_ayuda)

        self.act_salir_texto = QAction(self)
        barra_menu.addAction(self.act_salir_texto)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.btn_exportar_csv.setText(QCoreApplication.translate("MainWindow", "Exportar CSV"))
        self.btn_exportar_csv.setToolTip(QCoreApplication.translate("MainWindow", "Guardar tabla en Excel/CSV"))
        self.act_equipos_texto.setText(QCoreApplication.translate("MainWindow", "Equipos"))
        self.act_participantes_texto.setText(QCoreApplication.translate("MainWindow", "Participantes"))
        self.act_partidos_texto.setText(QCoreApplication.translate("MainWindow", "Partidos"))
        self.act_clasificacion_texto.setText(QCoreApplication.translate("MainWindow", "Clasificación"))
        self.act_informes_texto.setText(QCoreApplication.translate("MainWindow", "Informes"))
        self.act_creditos.setText(QCoreApplication.translate("MainWindow", "Créditos"))
        self.act_ayuda.setText(QCoreApplication.translate("MainWindow", "Ayuda"))
        self.act_salir_texto.setText(QCoreApplication.translate("MainWindow", "Salir (Inicio)"))

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
            self.retranslate_ui()

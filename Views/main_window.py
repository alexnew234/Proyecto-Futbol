from PySide6.QtWidgets import QMainWindow, QPushButton, QWidget
from PySide6.QtGui import QAction 

# Importamos tu UI generada
from Views.main_window_ui import Ui_MainWindow 
# Importamos el Dashboard nuevo
from Views.dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ---------------------------------------------------------
        # 1. CONFIGURACIÓN DEL DASHBOARD
        # ---------------------------------------------------------
        self.dashboard = DashboardView()
        self.ui.stackedWidget.insertWidget(0, self.dashboard)
        self.ui.stackedWidget.setCurrentIndex(0)

        # ---------------------------------------------------------
        # 2. LIMPIEZAS
        # ---------------------------------------------------------
        if hasattr(self.ui, 'toolBar'):
            self.ui.toolBar.setVisible(False)
            
        if hasattr(self.ui, 'scrollArea_bracket'):
            pass

        # ---------------------------------------------------------
        # 3. BOTÓN EXPORTAR CSV (En la esquina superior derecha)
        # ---------------------------------------------------------
        self.btn_exportar_csv = QPushButton("Exportar CSV", self.ui.page_clasificacion)
        self.btn_exportar_csv.setGeometry(420, 30, 120, 30)
        self.btn_exportar_csv.setStyleSheet("""
            background-color: #1E6637; 
            color: white; 
            font-weight: bold; 
            border-radius: 4px;
        """)
        self.btn_exportar_csv.setToolTip("Guardar tabla en Excel/CSV")

        # ---------------------------------------------------------
        # 4. MENÚ SUPERIOR (Con botón 'Clasificación' añadido)
        # ---------------------------------------------------------
        barra_menu = self.menuBar()
        barra_menu.clear() 

        # -- Botones Principales --
        self.act_equipos_texto = QAction("Equipos", self)
        barra_menu.addAction(self.act_equipos_texto)

        self.act_participantes_texto = QAction("Participantes", self)
        barra_menu.addAction(self.act_participantes_texto)

        self.act_partidos_texto = QAction("Partidos", self)
        barra_menu.addAction(self.act_partidos_texto)

        # --- NUEVO BOTÓN: CLASIFICACIÓN ---
        self.act_clasificacion_texto = QAction("Clasificación", self)
        barra_menu.addAction(self.act_clasificacion_texto)

        # -- Extras --
        self.act_creditos = QAction("Créditos", self)
        barra_menu.addAction(self.act_creditos)

        self.act_ayuda = QAction("Ayuda", self)
        barra_menu.addAction(self.act_ayuda)

        self.act_salir_texto = QAction("Salir (Inicio)", self)
        barra_menu.addAction(self.act_salir_texto)
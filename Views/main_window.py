from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QAction 

# Importamos tu UI generada (con el nombre correcto que vimos antes)
from Views.main_window_ui import Ui_MainWindow 
# Importamos el Dashboard nuevo
from Views.dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # ---------------------------------------------------------
        # 1. CONFIGURACIÓN DEL DASHBOARD (PORTADA)
        # ---------------------------------------------------------
        self.dashboard = DashboardView()
        
        # ¡TRUCO!: Insertamos el dashboard en la posición 0 del StackedWidget
        # Así empujamos las otras páginas y el Dashboard se convierte en la portada.
        self.ui.stackedWidget.insertWidget(0, self.dashboard)
        
        # Le decimos que muestre esa página (la 0) al arrancar
        self.ui.stackedWidget.setCurrentIndex(0)

        # ---------------------------------------------------------
        # 2. LIMPIAR PÁGINA CLASIFICACIÓN ANTIGUA
        # ---------------------------------------------------------
        # Eliminar widgets viejos del scrollArea_bracket
        if hasattr(self.ui, 'scrollArea_bracket'):
            layout = self.ui.page_clasificacion.layout()
            if layout:
                while layout.count():
                    layout.takeAt(0).widget().deleteLater()
            else:
                # Si no hay layout, limpiar todos los widgets
                for widget in self.ui.page_clasificacion.findChildren(type):
                    widget.deleteLater()

        # ---------------------------------------------------------
        # 3. OCULTAR BARRA ANTIGUA
        # ---------------------------------------------------------
        if hasattr(self.ui, 'toolBar'):
            self.ui.toolBar.setVisible(False)

        # ---------------------------------------------------------
        # 4. MENÚ SUPERIOR (TEXTO)
        # ---------------------------------------------------------
        self.act_equipos_texto = QAction("Equipos", self)
        self.act_participantes_texto = QAction("Participantes", self)
        self.act_partidos_texto = QAction("Partidos", self)
        self.act_salir_texto = QAction("Salir (Inicio)", self)

        barra_menu = self.menuBar()
        barra_menu.addAction(self.act_equipos_texto)
        barra_menu.addAction(self.act_participantes_texto)
        barra_menu.addAction(self.act_partidos_texto)
        barra_menu.addAction(self.act_salir_texto)
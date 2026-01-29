import sys
import os
from PySide6.QtWidgets import QApplication, QHeaderView

# --- REQUISITO OBLIGATORIO PDF: Usar la librería externa ---
try:
    from torneo_db.database import inicializar_db, get_db_path
except ImportError:
    print("[ERROR CRÍTICO] No se encuentra la librería 'torneo_db'.")
    print("Debes crear la carpeta 'torneofutbol_db' y ejecutar 'pip install -e .' dentro.")
    sys.exit(1)

from Views.main_window import MainWindow
from Controllers.main_controller import MainController

def obtener_ruta_recurso(ruta_relativa):
    """ Función auxiliar para rutas en .exe y desarrollo """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, ruta_relativa)

def cargar_estilos(app):
    """
    Carga el archivo QSS externo de forma compatible con .exe
    """
    # Usamos la función auxiliar para encontrar el archivo
    ruta_qss = obtener_ruta_recurso(os.path.join("Resources", "qss", "estilos.qss"))
    
    if os.path.exists(ruta_qss):
        try:
            with open(ruta_qss, "r") as f:
                estilo = f.read()
                app.setStyleSheet(estilo)
            print(f"[OK] Estilos cargados desde: {ruta_qss}")
        except Exception as e:
            print(f"[ERROR] Error al leer el archivo QSS: {e}")
    else:
        print(f"[AVISO] No se encontró 'estilos.qss' en: {ruta_qss}")

def ajustar_tablas_bonitas(ui):
    """ Estira las columnas y pone colores alternos """
    tablas = [
        ui.tableWidget, ui.tableWidget_2,
        getattr(ui, 'tableWidget_local', None),
        getattr(ui, 'tableWidget_visitante', None)
    ]
    
    for tabla in tablas:
        if tabla and hasattr(tabla, 'horizontalHeader'):
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.setAlternatingRowColors(True)
            if hasattr(tabla, 'verticalHeader'):
                tabla.verticalHeader().setVisible(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Cargar estilos
    cargar_estilos(app) 
    
    # 2. Inicializar DB
    print(f"Usando base de datos en: {get_db_path()}")
    
    if inicializar_db():
        window = MainWindow()
        controller = MainController(window) 
        ajustar_tablas_bonitas(window.ui)
        
        window.show()
        sys.exit(app.exec())
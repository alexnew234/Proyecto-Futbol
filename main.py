import sys
from PySide6.QtWidgets import QApplication, QHeaderView
from PySide6.QtSql import QSqlDatabase, QSqlQuery

# Importamos tus módulos (Asegúrate de que las carpetas Models, Views, Controllers existen)
from Views.main_window import MainWindow
from Controllers.main_controller import MainController

def cargar_estilos(app):
    """
    Estilo 'Dark Mode' con corrección definitiva para FLECHAS (evitar cuadrados blancos)
    """
    estilo = """
    /* --- FONDO GENERAL --- */
    QMainWindow, QWidget {
        background-color: #1e1e1e;
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
    }

    /* --- MENÚ SUPERIOR --- */
    QMenuBar {
        background-color: #2d2d2d;
        color: #ffffff;
        border-bottom: 1px solid #444;
    }
    QMenuBar::item:selected {
        background-color: #B71C1C;
    }
    QMenu {
        background-color: #2d2d2d;
        color: white;
        border: 1px solid #555;
    }

    /* --- TABLAS --- */
    QTableWidget, QTreeWidget, QListView {
        background-color: #252526;
        color: #ddd;
        border: 1px solid #3e3e42;
        gridline-color: #3e3e42;
        selection-background-color: #B71C1C;
        selection-color: white;
    }
    QHeaderView::section {
        background-color: #333333;
        color: white;
        padding: 5px;
        border: 1px solid #3e3e42;
        font-weight: bold;
    }

    /* --- BOTONES --- */
    QPushButton {
        background-color: #3c3c3c;
        border: 1px solid #555;
        color: white;
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #505050;
        border: 1px solid #B71C1C;
    }
    
    /* Botones Específicos - VERDE */
    QPushButton#pushButton_anadir_equipo, 
    QPushButton#pushButton_nuevo_participante,
    QPushButton#BtnGuardar {
        background-color: #1E6637;
        border: 1px solid #2ECC71;
    }
    QPushButton#pushButton_anadir_equipo:hover, 
    QPushButton#pushButton_nuevo_participante:hover,
    QPushButton#BtnGuardar:hover {
        background-color: #2ECC71;
        color: black;
    }

    /* Botón Eliminar - ROJO */
    QPushButton#pushButton_eliminar_equipo {
        background-color: #781818; 
        border: 1px solid #E74C3C;
    }
    QPushButton#pushButton_eliminar_equipo:hover {
        background-color: #E74C3C; 
        color: white;
    }

    /* --- INPUTS TEXTO Y COMBOS --- */
    QLineEdit, QComboBox, QDateEdit {
        background-color: #3c3c3c;
        color: white;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 6px;
        min-height: 25px; 
    }
    QLineEdit:focus, QComboBox:focus {
        border: 2px solid #B71C1C;
    }

    /* --- SPINBOX (Cajitas de números) --- */
    QSpinBox {
        background-color: #3c3c3c;
        color: white;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 5px 45px 5px 5px;
        font-size: 18px; 
        font-weight: bold;
        min-height: 40px; 
    }

    /* --- BOTONES DEL SPINBOX --- */
    QSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right;
        width: 25px;
        background-color: #444;
        border: 1px solid #666;
        border-right: none;
        border-top-right-radius: 3px;
        margin: 0px;
        padding: 0px;
    }
    
    QSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right;
        width: 25px;
        background-color: #444;
        border: 1px solid #666;
        border-right: none;
        border-bottom-right-radius: 3px;
        margin: 0px;
        padding: 0px;
    }

    QSpinBox::up-button:hover {
        background-color: #666;
    }
    
    QSpinBox::down-button:hover {
        background-color: #666;
    }
    
    QSpinBox::up-button:pressed {
        background-color: #888;
    }
    
    QSpinBox::down-button:pressed {
        background-color: #888;
    }
    
    QSpinBox::up-arrow {
        image: url(nolink);
        width: 8px;
        height: 8px;
    }
    
    QSpinBox::down-arrow {
        image: url(nolink);
        width: 8px;
        height: 8px;
    }
    
    /* --- GROUP BOX --- */
    QGroupBox {
        border: 1px solid #555;
        border-radius: 6px;
        margin-top: 22px;
        font-weight: bold;
        color: #ccc;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 5px;
        color: #B71C1C;
    }
    """
    app.setStyleSheet(estilo)

def ajustar_tablas_bonitas(ui):
    """ Estira las columnas y pone colores alternos """
    # Lista de tablas para estirar columnas
    tablas = [
        ui.tableWidget,           # Tabla detalles equipo
        ui.tableWidget_2,         # Tabla participantes
        getattr(ui, 'tableWidget_local', None),     # Resultados local (si existe)
        getattr(ui, 'tableWidget_visitante', None)  # Resultados visitante (si existe)
    ]
    
    for tabla in tablas:
        if tabla and hasattr(tabla, 'horizontalHeader'):
            tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tabla.setAlternatingRowColors(True)
            tabla.verticalHeader().setVisible(False)

def inicializar_db():
    """ Crea las tablas con los campos NUEVOS (Goles, Tarjetas, Curso) """
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("Models/torneoFutbol_sqlite.db")
    
    if not db.open():
        print("No se pudo conectar a la base de datos")
        return False

    query = QSqlQuery()
    
    # 1. Tabla EQUIPOS
    query.exec("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            curso TEXT,
            color_camiseta TEXT,
            ruta_escudo TEXT
        )
    """)

    # 2. Tabla PARTICIPANTES (Actualizada)
    query.exec("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha_nacimiento TEXT,
            curso TEXT,              -- Nuevo
            tipo_participante TEXT,
            posicion TEXT,
            tarjetas_amarillas INTEGER DEFAULT 0, -- Nuevo
            tarjetas_rojas INTEGER DEFAULT 0,     -- Nuevo
            goles INTEGER DEFAULT 0,              -- Nuevo
            id_equipo INTEGER,
            FOREIGN KEY(id_equipo) REFERENCES equipos(id)
        )
    """)
    return True

# --- BLOQUE PRINCIPAL ÚNICO ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 1. Aplicamos Estilos
    cargar_estilos(app) 
    
    # 2. Inicializamos BBDD (Crear tablas nuevas si no existen)
    if inicializar_db():
        window = MainWindow()
        
        # 3. Arrancamos el Controlador
        controller = MainController(window) 
        
        # 4. Ajustes visuales extra
        ajustar_tablas_bonitas(window.ui)
        
        window.show()
        sys.exit(app.exec())
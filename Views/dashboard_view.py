from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal vertical
        layout = QVBoxLayout()
        # AlignTop es clave para que empiece pegado arriba
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter) 
        layout.setSpacing(10) 
        
        # --- CAMBIO AQUÍ: Margen superior reducido a 10 (antes 40) ---
        # (Izquierda, Arriba, Derecha, Abajo)
        layout.setContentsMargins(0, 10, 0, 0) 
        self.setLayout(layout)

        # 1. TÍTULO
        lbl_titulo = QLabel("Panel de Control RFEF")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #B71C1C;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        
        # Mantenemos el fixedHeight pequeño para "comprimir" el espacio del título
        lbl_titulo.setFixedHeight(30) 
        
        layout.addWidget(lbl_titulo)

        # 2. ESPACIO RESERVADO (El controlador insertará el reloj aquí, debajo del título)

        # 3. REJILLA DE BOTONES
        grid = QGridLayout()
        grid.setSpacing(20)
        
        self.btn_partidos = QPushButton("Gestión de Partidos")
        self.btn_resultados = QPushButton("Resultados / Clasificación")
        self.btn_equipos = QPushButton("Equipos")
        self.btn_participantes = QPushButton("Participantes")

        estilo_boton = """
            QPushButton {
                font-size: 18px;
                padding: 20px;
                min-width: 200px;
                min-height: 100px;
                border-radius: 10px;
                background-color: #3c3c3c;
                border: 2px solid #555;
            }
            QPushButton:hover {
                background-color: #B71C1C;
                border: 2px solid #ff5555;
            }
        """
        
        for btn in [self.btn_partidos, self.btn_resultados, self.btn_equipos, self.btn_participantes]:
            btn.setStyleSheet(estilo_boton)
            btn.setCursor(Qt.PointingHandCursor)

        grid.addWidget(self.btn_partidos, 0, 0)
        grid.addWidget(self.btn_resultados, 0, 1)
        grid.addWidget(self.btn_equipos, 1, 0)
        grid.addWidget(self.btn_participantes, 1, 1)

        # Contenedor para el grid
        grid_container = QWidget()
        grid_container.setLayout(grid)
        
        # Le damos un margen superior extra al grid para separarlo un poco del reloj
        # Así el reloj queda pegado al título, pero los botones bajan un poco
        layout.addWidget(grid_container)
        
        # Espaciador final para empujar todo hacia arriba con fuerza
        layout.addStretch()
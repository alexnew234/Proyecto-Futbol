from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal vertical
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter) 
        layout.setSpacing(10) # Espaciado general reducido
        
        # Margen superior reducido
        layout.setContentsMargins(0, 10, 0, 0) 
        self.setLayout(layout)

        # 1. TÍTULO
        lbl_titulo = QLabel("Panel de Control RFEF")
        lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #B71C1C;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setFixedHeight(30) 
        layout.addWidget(lbl_titulo)

        # 2. ESPACIO PARA RELOJ (El controlador lo insertará aquí, en el índice 1)

        # --- NUEVO: BOTÓN DE CONFIGURACIÓN ARRIBA ---
        # Lo colocamos aquí para que esté en la parte superior.
        self.btn_config_reloj = QPushButton("⚙️ Configuración del Reloj")
        self.btn_config_reloj.setCursor(Qt.PointingHandCursor)
        # Estilo más pequeño y discreto para la parte superior
        self.btn_config_reloj.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                padding: 8px 15px;
                border-radius: 5px;
                background-color: #444;
                color: #ddd;
                border: 1px solid #555;
            }
            QPushButton:hover {
                background-color: #555;
                color: white;
                border-color: #777;
            }
        """)
        # Lo metemos en un layout horizontal para centrarlo sin que ocupe todo el ancho
        layout_btn_reloj = QHBoxLayout()
        layout_btn_reloj.addWidget(self.btn_config_reloj)
        layout_btn_reloj.setAlignment(Qt.AlignCenter)
        layout.addLayout(layout_btn_reloj)
        # -------------------------------------------

        # 3. ESPACIO PARA LA IMAGEN
        # Preparamos un label contenedor para que el controlador ponga ahí la imagen
        self.image_container = QLabel()
        self.image_container.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_container)

        # 4. REJILLA DE BOTONES PRINCIPALES
        grid = QGridLayout()
        grid.setSpacing(15) # Espaciado entre botones reducido (antes 20)
        
        self.btn_partidos = QPushButton("Gestión de Partidos")
        self.btn_resultados = QPushButton("Resultados / Clasificación")
        self.btn_equipos = QPushButton("Equipos")
        self.btn_participantes = QPushButton("Participantes")
        
        # Estilo actualizado: Botones más compactos
        estilo_boton = """
            QPushButton {
                font-size: 18px;
                padding: 15px;       /* Reducido de 20px */
                min-width: 200px;
                min-height: 80px;    /* Reducido de 100px */
                border-radius: 10px;
                background-color: #3c3c3c;
                border: 2px solid #555;
            }
            QPushButton:hover {
                background-color: #B71C1C;
                border: 2px solid #ff5555;
            }
        """
        
        botones = [
            self.btn_partidos, self.btn_resultados, 
            self.btn_equipos, self.btn_participantes
        ]
        
        for btn in botones:
            btn.setStyleSheet(estilo_boton)
            btn.setCursor(Qt.PointingHandCursor)

        # Distribución en Grid (2 columnas)
        grid.addWidget(self.btn_partidos, 0, 0)
        grid.addWidget(self.btn_resultados, 0, 1)
        grid.addWidget(self.btn_equipos, 1, 0)
        grid.addWidget(self.btn_participantes, 1, 1)
        
        # Contenedor para el grid
        grid_container = QWidget()
        grid_container.setLayout(grid)
        layout.addWidget(grid_container)
        
        # Espaciador final para empujar todo hacia arriba
        layout.addStretch()
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal vertical (Título + Rejilla de botones)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(40)
        self.setLayout(layout)

        # TÍTULO GRANDE
        lbl_titulo = QLabel("Panel de Control RFEF")
        lbl_titulo.setStyleSheet("font-size: 32px; font-weight: bold; color: #B71C1C; margin-bottom: 20px;")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_titulo)

        # REJILLA DE BOTONES (Grid)
        grid = QGridLayout()
        grid.setSpacing(20)
        
        # Definimos los botones
        self.btn_partidos = QPushButton("Gestión de Partidos")
        self.btn_resultados = QPushButton("Resultados / Clasificación")
        self.btn_equipos = QPushButton("Equipos")
        self.btn_participantes = QPushButton("Participantes")

        # Estilo específico para que sean BOTONES GIGANTES
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
                background-color: #B71C1C; /* Rojo al pasar el ratón */
                border: 2px solid #ff5555;
            }
        """
        
        for btn in [self.btn_partidos, self.btn_resultados, self.btn_equipos, self.btn_participantes]:
            btn.setStyleSheet(estilo_boton)
            btn.setCursor(Qt.PointingHandCursor)

        # Añadimos al Grid (Fila, Columna)
        grid.addWidget(self.btn_partidos, 0, 0)
        grid.addWidget(self.btn_resultados, 0, 1)
        grid.addWidget(self.btn_equipos, 1, 0)
        grid.addWidget(self.btn_participantes, 1, 1)

        layout.addLayout(grid)
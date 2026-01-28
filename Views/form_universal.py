from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QLabel, QComboBox, 
    QDateEdit, QSpinBox, QGroupBox
)
from PySide6.QtCore import Qt, QDate

class FormUniversalView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión RFEF")
        self.setMinimumSize(500, 650) # Un poco más alto para que quepa todo

        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout_principal)

        # TÍTULO
        self.lbl_titulo = QLabel("Registro")
        self.lbl_titulo.setObjectName("Titulo") # Para que el CSS oscuro lo pille si quieres
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet("font-size: 20px; font-weight: bold; color: #B71C1C; margin-bottom: 10px;")
        layout_principal.addWidget(self.lbl_titulo)

        # ---------------------------------------------------------
        # ZONA EQUIPO
        # ---------------------------------------------------------
        self.container_equipo = QWidget()
        form_equipo = QFormLayout(self.container_equipo)
        
        self.txt_eq_nombre = QLineEdit()
        self.txt_eq_curso = QLineEdit()
        self.txt_eq_camiseta = QLineEdit()
        self.btn_imagen = QPushButton("Seleccionar Escudo...")
        self.lbl_ruta_imagen = QLabel("")
        self.lbl_ruta_imagen.setVisible(False)

        form_equipo.addRow("Nombre Equipo:", self.txt_eq_nombre)
        form_equipo.addRow("Curso:", self.txt_eq_curso)
        form_equipo.addRow("Color:", self.txt_eq_camiseta)
        form_equipo.addRow("Escudo:", self.btn_imagen)

        layout_principal.addWidget(self.container_equipo)

        # ---------------------------------------------------------
        # ZONA PARTICIPANTE (ACTUALIZADA A LA PRÁCTICA)
        # ---------------------------------------------------------
        self.container_participante = QWidget()
        layout_part = QVBoxLayout(self.container_participante)
        
        # Datos Personales
        group_datos = QGroupBox("Datos Personales")
        form_datos = QFormLayout()
        
        self.txt_part_nombre = QLineEdit()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.date_nacimiento.setDate(QDate.currentDate().addYears(-16))
        self.date_nacimiento.setCalendarPopup(True)
        
        self.txt_part_curso = QLineEdit() # NUEVO: Curso del alumno
        self.txt_part_curso.setPlaceholderText("Ej: 1º DAW")

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Jugador", "Árbitro", "Ambos"])

        self.combo_posicion = QComboBox()
        self.combo_posicion.addItems(["Portero", "Defensa", "Centrocampista", "Delantero", "N/A"])
        
        self.combo_equipo_asignado = QComboBox()

        form_datos.addRow("Nombre:", self.txt_part_nombre)
        form_datos.addRow("Fecha Nacim.:", self.date_nacimiento)
        form_datos.addRow("Curso:", self.txt_part_curso)
        form_datos.addRow("Tipo:", self.combo_tipo)
        form_datos.addRow("Posición:", self.combo_posicion)
        form_datos.addRow("Equipo:", self.combo_equipo_asignado)
        
        group_datos.setLayout(form_datos)
        layout_part.addWidget(group_datos)

        # Estadísticas (NUEVO)
        group_stats = QGroupBox("Estadísticas Iniciales")
        layout_stats = QHBoxLayout()
        
        # Tarjetas Amarillas
        self.spin_amarillas = QSpinBox()
        self.spin_amarillas.setRange(0, 100)
        lbl_amarillas = QLabel("T. Amarillas:")
        
        # Tarjetas Rojas
        self.spin_rojas = QSpinBox()
        self.spin_rojas.setRange(0, 100)
        lbl_rojas = QLabel("T. Rojas:")
        
        # Goles
        self.spin_goles = QSpinBox()
        self.spin_goles.setRange(0, 1000)
        lbl_goles = QLabel("Goles:")

        layout_stats.addWidget(lbl_amarillas)
        layout_stats.addWidget(self.spin_amarillas)
        layout_stats.addWidget(lbl_rojas)
        layout_stats.addWidget(self.spin_rojas)
        layout_stats.addWidget(lbl_goles)
        layout_stats.addWidget(self.spin_goles)
        
        group_stats.setLayout(layout_stats)
        layout_part.addWidget(group_stats)

        layout_principal.addWidget(self.container_participante)
        layout_principal.addStretch()

        # BOTÓN GUARDAR
        self.btn_guardar = QPushButton("GUARDAR")
        self.btn_guardar.setObjectName("BtnGuardar")
        self.btn_guardar.setMinimumHeight(40)
        self.btn_guardar.setCursor(Qt.PointingHandCursor)
        layout_principal.addWidget(self.btn_guardar)

    def modo_equipo(self):
        self.lbl_titulo.setText("Alta de Equipo")
        self.container_equipo.setVisible(True)
        self.container_participante.setVisible(False)

    def modo_participante(self):
        self.lbl_titulo.setText("Ficha de Participante")
        self.container_equipo.setVisible(False)
        self.container_participante.setVisible(True)
from PySide6.QtCore import QDate, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class FormUniversalView(QWidget):
    def __init__(self):
        super().__init__()
        self._is_english = False
        self._mode_key = "equipo"

        self.setWindowTitle("Gestión RFEF")
        self.setMinimumSize(500, 650)

        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout_principal)

        self.lbl_titulo = QLabel("Registro")
        self.lbl_titulo.setObjectName("Titulo")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #B71C1C; margin-bottom: 10px;"
        )
        layout_principal.addWidget(self.lbl_titulo)

        # Zona equipo
        self.container_equipo = QWidget()
        self.form_equipo = QFormLayout(self.container_equipo)
        self.txt_eq_nombre = QLineEdit()
        self.txt_eq_curso = QLineEdit()
        self.txt_eq_camiseta = QLineEdit()
        self.btn_imagen = QPushButton("")
        self.lbl_ruta_imagen = QLabel("")
        self.lbl_ruta_imagen.setVisible(False)

        self.lbl_eq_nombre = QLabel("")
        self.lbl_eq_curso = QLabel("")
        self.lbl_eq_color = QLabel("")
        self.lbl_eq_escudo = QLabel("")
        self.form_equipo.addRow(self.lbl_eq_nombre, self.txt_eq_nombre)
        self.form_equipo.addRow(self.lbl_eq_curso, self.txt_eq_curso)
        self.form_equipo.addRow(self.lbl_eq_color, self.txt_eq_camiseta)
        self.form_equipo.addRow(self.lbl_eq_escudo, self.btn_imagen)
        layout_principal.addWidget(self.container_equipo)

        # Zona participante
        self.container_participante = QWidget()
        layout_part = QVBoxLayout(self.container_participante)

        self.group_datos = QGroupBox("")
        form_datos = QFormLayout()
        self.txt_part_nombre = QLineEdit()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.date_nacimiento.setDate(QDate.currentDate().addYears(-16))
        self.date_nacimiento.setCalendarPopup(True)
        self.txt_part_curso = QLineEdit()

        self.combo_tipo = QComboBox()
        self.combo_posicion = QComboBox()
        self.combo_equipo_asignado = QComboBox()

        self.lbl_part_nombre = QLabel("")
        self.lbl_part_fecha = QLabel("")
        self.lbl_part_curso = QLabel("")
        self.lbl_part_tipo = QLabel("")
        self.lbl_part_posicion = QLabel("")
        self.lbl_part_equipo = QLabel("")
        form_datos.addRow(self.lbl_part_nombre, self.txt_part_nombre)
        form_datos.addRow(self.lbl_part_fecha, self.date_nacimiento)
        form_datos.addRow(self.lbl_part_curso, self.txt_part_curso)
        form_datos.addRow(self.lbl_part_tipo, self.combo_tipo)
        form_datos.addRow(self.lbl_part_posicion, self.combo_posicion)
        form_datos.addRow(self.lbl_part_equipo, self.combo_equipo_asignado)
        self.group_datos.setLayout(form_datos)
        layout_part.addWidget(self.group_datos)

        self.group_stats = QGroupBox("")
        layout_stats = QHBoxLayout()
        self.spin_amarillas = QSpinBox()
        self.spin_amarillas.setRange(0, 100)
        self.spin_rojas = QSpinBox()
        self.spin_rojas.setRange(0, 100)
        self.spin_goles = QSpinBox()
        self.spin_goles.setRange(0, 1000)
        self.lbl_amarillas = QLabel("")
        self.lbl_rojas = QLabel("")
        self.lbl_goles = QLabel("")
        layout_stats.addWidget(self.lbl_amarillas)
        layout_stats.addWidget(self.spin_amarillas)
        layout_stats.addWidget(self.lbl_rojas)
        layout_stats.addWidget(self.spin_rojas)
        layout_stats.addWidget(self.lbl_goles)
        layout_stats.addWidget(self.spin_goles)
        self.group_stats.setLayout(layout_stats)
        layout_part.addWidget(self.group_stats)

        layout_principal.addWidget(self.container_participante)
        layout_principal.addStretch()

        self.btn_guardar = QPushButton("")
        self.btn_guardar.setObjectName("BtnGuardar")
        self.btn_guardar.setMinimumHeight(40)
        self.btn_guardar.setCursor(Qt.PointingHandCursor)
        layout_principal.addWidget(self.btn_guardar)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle("RFEF Manager" if self._is_english else "Gestión RFEF")
        self.lbl_titulo.setText("Registration" if self._is_english else "Registro")

        self.lbl_eq_nombre.setText("Team Name:" if self._is_english else "Nombre Equipo:")
        self.lbl_eq_curso.setText("Course:" if self._is_english else "Curso:")
        self.lbl_eq_color.setText("Color:" if self._is_english else "Color:")
        self.lbl_eq_escudo.setText("Crest:" if self._is_english else "Escudo:")
        self.btn_imagen.setText("Select Crest..." if self._is_english else "Seleccionar Escudo...")

        self.group_datos.setTitle("Personal Data" if self._is_english else "Datos Personales")
        self.group_stats.setTitle("Initial Stats" if self._is_english else "Estadísticas Iniciales")
        self.lbl_part_nombre.setText("Name:" if self._is_english else "Nombre:")
        self.lbl_part_fecha.setText("Birth Date:" if self._is_english else "Fecha Nacim.:")
        self.lbl_part_curso.setText("Course:" if self._is_english else "Curso:")
        self.lbl_part_tipo.setText("Type:" if self._is_english else "Tipo:")
        self.lbl_part_posicion.setText("Position:" if self._is_english else "Posición:")
        self.lbl_part_equipo.setText("Team:" if self._is_english else "Equipo:")
        self.lbl_amarillas.setText("Yellow:" if self._is_english else "T. Amarillas:")
        self.lbl_rojas.setText("Red:" if self._is_english else "T. Rojas:")
        self.lbl_goles.setText("Goals:" if self._is_english else "Goles:")
        self.txt_part_curso.setPlaceholderText("Eg: 1st DAW" if self._is_english else "Ej: 1º DAW")

        tipo_actual = self.combo_tipo.currentData() if self.combo_tipo.count() else "Jugador"
        self.combo_tipo.blockSignals(True)
        self.combo_tipo.clear()
        self.combo_tipo.addItem("Player" if self._is_english else "Jugador", "Jugador")
        self.combo_tipo.addItem("Referee" if self._is_english else "Árbitro", "Árbitro")
        self.combo_tipo.addItem("Both" if self._is_english else "Ambos", "Ambos")
        idx_tipo = self.combo_tipo.findData(tipo_actual)
        self.combo_tipo.setCurrentIndex(idx_tipo if idx_tipo >= 0 else 0)
        self.combo_tipo.blockSignals(False)

        pos_actual = self.combo_posicion.currentData() if self.combo_posicion.count() else "Portero"
        self.combo_posicion.blockSignals(True)
        self.combo_posicion.clear()
        self.combo_posicion.addItem("Goalkeeper" if self._is_english else "Portero", "Portero")
        self.combo_posicion.addItem("Defender" if self._is_english else "Defensa", "Defensa")
        self.combo_posicion.addItem("Midfielder" if self._is_english else "Centrocampista", "Centrocampista")
        self.combo_posicion.addItem("Forward" if self._is_english else "Delantero", "Delantero")
        self.combo_posicion.addItem("N/A", "N/A")
        idx_pos = self.combo_posicion.findData(pos_actual)
        self.combo_posicion.setCurrentIndex(idx_pos if idx_pos >= 0 else 0)
        self.combo_posicion.blockSignals(False)

        if self._mode_key == "equipo":
            self.modo_equipo()
        else:
            self.modo_participante()

    def set_language(self, language_code):
        self._is_english = language_code == "en"
        self.retranslate_ui()

    def modo_equipo(self):
        self._mode_key = "equipo"
        self.lbl_titulo.setText("Edit Team" if self._is_english else "Alta de Equipo")
        self.container_equipo.setVisible(True)
        self.container_participante.setVisible(False)
        self.btn_guardar.setText("SAVE" if self._is_english else "GUARDAR")

    def modo_participante(self):
        self._mode_key = "participante"
        self.lbl_titulo.setText("Player Profile" if self._is_english else "Ficha de Participante")
        self.container_equipo.setVisible(False)
        self.container_participante.setVisible(True)
        self.btn_guardar.setText("SAVE" if self._is_english else "GUARDAR")

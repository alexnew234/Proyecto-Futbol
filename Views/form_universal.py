from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLineEdit, QPushButton, QLabel, QComboBox, 
    QDateEdit, QSpinBox, QGroupBox
)
from PySide6.QtCore import Qt, QDate, QCoreApplication, QEvent

class FormUniversalView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        self.setMinimumSize(500, 650) # Un poco más alto para que quepa todo

        layout_principal = QVBoxLayout()
        layout_principal.setSpacing(15)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        self.setLayout(layout_principal)

        # TÍTULO
        self.lbl_titulo = QLabel("")
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
        self.btn_imagen = QPushButton("")
        self.lbl_ruta_imagen = QLabel("")
        self.lbl_ruta_imagen.setVisible(False)
        
        self.lbl_eq_nombre = QLabel("")
        self.lbl_eq_curso = QLabel("")
        self.lbl_eq_color = QLabel("")
        self.lbl_eq_escudo = QLabel("")

        form_equipo.addRow(self.lbl_eq_nombre, self.txt_eq_nombre)
        form_equipo.addRow(self.lbl_eq_curso, self.txt_eq_curso)
        form_equipo.addRow(self.lbl_eq_color, self.txt_eq_camiseta)
        form_equipo.addRow(self.lbl_eq_escudo, self.btn_imagen)

        layout_principal.addWidget(self.container_equipo)

        # ---------------------------------------------------------
        # ZONA PARTICIPANTE (ACTUALIZADA A LA PRÁCTICA)
        # ---------------------------------------------------------
        self.container_participante = QWidget()
        layout_part = QVBoxLayout(self.container_participante)
        
        # Datos Personales
        self.group_datos = QGroupBox("")
        form_datos = QFormLayout()
        
        self.txt_part_nombre = QLineEdit()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        self.date_nacimiento.setDate(QDate.currentDate().addYears(-16))
        self.date_nacimiento.setCalendarPopup(True)
        
        self.txt_part_curso = QLineEdit() # NUEVO: Curso del alumno
        self.txt_part_curso.setPlaceholderText("")

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

        # Estadísticas (NUEVO)
        self.group_stats = QGroupBox("")
        layout_stats = QHBoxLayout()
        
        # Tarjetas Amarillas
        self.spin_amarillas = QSpinBox()
        self.spin_amarillas.setRange(0, 100)
        self.lbl_amarillas = QLabel("")
        
        # Tarjetas Rojas
        self.spin_rojas = QSpinBox()
        self.spin_rojas.setRange(0, 100)
        self.lbl_rojas = QLabel("")
        
        # Goles
        self.spin_goles = QSpinBox()
        self.spin_goles.setRange(0, 1000)
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

        # BOTÓN GUARDAR
        self.btn_guardar = QPushButton("")
        self.btn_guardar.setObjectName("BtnGuardar")
        self.btn_guardar.setMinimumHeight(40)
        self.btn_guardar.setCursor(Qt.PointingHandCursor)
        layout_principal.addWidget(self.btn_guardar)

        self._modo_actual = None
        self._title_key = "Registro"
        self._save_key = "GUARDAR"
        self.retranslate_ui()

    def modo_equipo(self):
        self._modo_actual = "EQUIPO"
        self._title_key = "Alta de Equipo"
        self.container_equipo.setVisible(True)
        self.container_participante.setVisible(False)
        self.retranslate_ui()

    def modo_participante(self):
        self._modo_actual = "PARTICIPANTE"
        self._title_key = "Ficha de Participante"
        self.container_equipo.setVisible(False)
        self.container_participante.setVisible(True)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(QCoreApplication.translate("FormUniversalView", "Gestión RFEF"))
        self.lbl_titulo.setText(QCoreApplication.translate("FormUniversalView", self._title_key))

        # Equipo
        self.lbl_eq_nombre.setText(QCoreApplication.translate("FormUniversalView", "Nombre Equipo:"))
        self.lbl_eq_curso.setText(QCoreApplication.translate("FormUniversalView", "Curso:"))
        self.lbl_eq_color.setText(QCoreApplication.translate("FormUniversalView", "Color:"))
        self.lbl_eq_escudo.setText(QCoreApplication.translate("FormUniversalView", "Escudo:"))
        if not self.lbl_ruta_imagen.text():
            self.btn_imagen.setText(QCoreApplication.translate("FormUniversalView", "Seleccionar Escudo..."))

        # Participante
        self.group_datos.setTitle(QCoreApplication.translate("FormUniversalView", "Datos Personales"))
        self.lbl_part_nombre.setText(QCoreApplication.translate("FormUniversalView", "Nombre:"))
        self.lbl_part_fecha.setText(QCoreApplication.translate("FormUniversalView", "Fecha Nacim.:"))
        self.lbl_part_curso.setText(QCoreApplication.translate("FormUniversalView", "Curso:"))
        self.lbl_part_tipo.setText(QCoreApplication.translate("FormUniversalView", "Tipo:"))
        self.lbl_part_posicion.setText(QCoreApplication.translate("FormUniversalView", "Posición:"))
        self.lbl_part_equipo.setText(QCoreApplication.translate("FormUniversalView", "Equipo:"))
        self.txt_part_curso.setPlaceholderText(QCoreApplication.translate("FormUniversalView", "Ej: 1º DAW"))

        # Combo tipo (mantener selección)
        tipo_actual = self.combo_tipo.currentData()
        self.combo_tipo.blockSignals(True)
        self.combo_tipo.clear()
        self.combo_tipo.addItem(QCoreApplication.translate("FormUniversalView", "Jugador"), "Jugador")
        self.combo_tipo.addItem(QCoreApplication.translate("FormUniversalView", "Árbitro"), "Árbitro")
        self.combo_tipo.addItem(QCoreApplication.translate("FormUniversalView", "Ambos"), "Ambos")
        idx = self.combo_tipo.findData(tipo_actual)
        self.combo_tipo.setCurrentIndex(idx if idx >= 0 else 0)
        self.combo_tipo.blockSignals(False)

        # Combo posición (mantener selección)
        pos_actual = self.combo_posicion.currentData()
        self.combo_posicion.blockSignals(True)
        self.combo_posicion.clear()
        self.combo_posicion.addItem(QCoreApplication.translate("FormUniversalView", "Portero"), "Portero")
        self.combo_posicion.addItem(QCoreApplication.translate("FormUniversalView", "Defensa"), "Defensa")
        self.combo_posicion.addItem(QCoreApplication.translate("FormUniversalView", "Centrocampista"), "Centrocampista")
        self.combo_posicion.addItem(QCoreApplication.translate("FormUniversalView", "Delantero"), "Delantero")
        self.combo_posicion.addItem(QCoreApplication.translate("FormUniversalView", "N/A"), "N/A")
        idx = self.combo_posicion.findData(pos_actual)
        self.combo_posicion.setCurrentIndex(idx if idx >= 0 else 0)
        self.combo_posicion.blockSignals(False)

        # Estadísticas
        self.group_stats.setTitle(QCoreApplication.translate("FormUniversalView", "Estadísticas Iniciales"))
        self.lbl_amarillas.setText(QCoreApplication.translate("FormUniversalView", "T. Amarillas:"))
        self.lbl_rojas.setText(QCoreApplication.translate("FormUniversalView", "T. Rojas:"))
        self.lbl_goles.setText(QCoreApplication.translate("FormUniversalView", "Goles:"))

        # Botón guardar
        self.btn_guardar.setText(QCoreApplication.translate("FormUniversalView", self._save_key))

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()

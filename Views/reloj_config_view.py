from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QCheckBox, QComboBox, QSpinBox, QLineEdit, 
    QPushButton, QLabel, QTimeEdit, QMessageBox
)
from PySide6.QtCore import QTime, Qt
from Views.reloj_widget import RelojDigital, ModoReloj

class RelojConfigView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout Principal
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        # --- COLUMNA IZQUIERDA: CONTROLES ---
        panel_izq = QWidget()
        layout_izq = QVBoxLayout(panel_izq)
        
        # 1. Grupo de Propiedades Generales
        grupo_props = QGroupBox("Propiedades del Componente")
        layout_props = QVBoxLayout()
        
        # Modo (Clock / Timer)
        layout_props.addWidget(QLabel("Modo de Funcionamiento:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Reloj Digital (Hora)", "Cronómetro / Temporizador"])
        layout_props.addWidget(self.combo_mode)
        
        # Formato 24h
        self.chk_24h = QCheckBox("Formato 24 Horas")
        self.chk_24h.setChecked(True)
        layout_props.addWidget(self.chk_24h)
        
        # Cuenta Atrás (Nueva funcionalidad)
        self.chk_countdown = QCheckBox("Modo Cuenta Regresiva (Solo Timer)")
        layout_props.addWidget(self.chk_countdown)
        
        grupo_props.setLayout(layout_props)
        layout_izq.addWidget(grupo_props)
        
        # 2. Grupo de Alarma y Tiempos
        grupo_alarma = QGroupBox("Configuración de Alarma y Tiempos")
        layout_alarma = QVBoxLayout()
        
        # Activar Alarma
        self.chk_alarm = QCheckBox("Alarma Activada")
        layout_alarma.addWidget(self.chk_alarm)
        
        # Mensaje
        layout_alarma.addWidget(QLabel("Mensaje de Alarma:"))
        self.txt_mensaje = QLineEdit("¡Tiempo completado!")
        layout_alarma.addWidget(self.txt_mensaje)
        
        # Hora Alarma (Para modo Reloj)
        layout_alarma.addWidget(QLabel("Hora de Alarma (Modo Reloj):"))
        self.time_alarm = QTimeEdit()
        self.time_alarm.setTime(QTime.currentTime().addSecs(60)) # Por defecto 1 min más
        layout_alarma.addWidget(self.time_alarm)
        
        # Duración (Para modo Timer)
        layout_alarma.addWidget(QLabel("Duración / Límite (Segundos):"))
        self.spin_duracion = QSpinBox()
        self.spin_duracion.setRange(0, 99999)
        self.spin_duracion.setValue(10) # 10 segundos para probar rápido
        layout_alarma.addWidget(self.spin_duracion)
        
        grupo_alarma.setLayout(layout_alarma)
        layout_izq.addWidget(grupo_alarma)
        
        # 3. Botones de Control
        grupo_ctrl = QGroupBox("Control Manual")
        layout_ctrl = QHBoxLayout()
        
        self.btn_start = QPushButton("Start")
        self.btn_pause = QPushButton("Pause")
        self.btn_reset = QPushButton("Reset")
        
        # Estilos botones
        self.btn_start.setStyleSheet("background-color: #2d7d2d; color: white; font-weight: bold;")
        self.btn_pause.setStyleSheet("background-color: #d8a600; color: black; font-weight: bold;")
        self.btn_reset.setStyleSheet("background-color: #7d2d2d; color: white; font-weight: bold;")
        
        layout_ctrl.addWidget(self.btn_start)
        layout_ctrl.addWidget(self.btn_pause)
        layout_ctrl.addWidget(self.btn_reset)
        
        grupo_ctrl.setLayout(layout_ctrl)
        layout_izq.addWidget(grupo_ctrl)
        
        layout_izq.addStretch() # Empujar todo arriba
        
        # --- COLUMNA DERECHA: VISUALIZACIÓN ---
        panel_der = QWidget()
        panel_der.setStyleSheet("background-color: #222; border-radius: 15px;")
        layout_der = QVBoxLayout(panel_der)
        layout_der.setAlignment(Qt.AlignCenter)
        
        # Título
        lbl_demo = QLabel("VISTA PREVIA DEL COMPONENTE")
        lbl_demo.setStyleSheet("color: #aaa; font-size: 14px; font-weight: bold; margin-bottom: 20px;")
        lbl_demo.setAlignment(Qt.AlignCenter)
        layout_der.addWidget(lbl_demo)
        
        # INSTANCIA DEL RELOJ
        self.reloj_demo = RelojDigital()
        self.reloj_demo.setFixedSize(400, 150) # Grande para verlo bien
        # Estilo "Digital" verde
        self.reloj_demo.setStyleSheet("""
            QLabel { 
                color: #00ff00; 
                font-size: 60px; 
                font-family: 'Courier New'; 
                font-weight: bold;
            }
        """)
        layout_der.addWidget(self.reloj_demo)
        
        # Label para mostrar señales recibidas
        self.lbl_signal = QLabel("Esperando señal...")
        self.lbl_signal.setStyleSheet("color: white; font-size: 16px; margin-top: 20px; padding: 10px; background-color: #444; border-radius: 5px;")
        self.lbl_signal.setAlignment(Qt.AlignCenter)
        layout_der.addWidget(self.lbl_signal)
        
        # Añadir paneles al layout principal
        main_layout.addWidget(panel_izq, 40) # 40% ancho
        main_layout.addWidget(panel_der, 60) # 60% ancho
        
        # CONEXIONES INTERNAS (Lógica de la vista)
        self.conectar_controles()

    def conectar_controles(self):
        # 1. Cambios de Propiedades -> Reloj
        self.combo_mode.currentIndexChanged.connect(self.actualizar_reloj)
        self.chk_24h.toggled.connect(lambda v: setattr(self.reloj_demo, 'is24Hour', v))
        self.chk_countdown.toggled.connect(lambda v: setattr(self.reloj_demo, 'isCountDown', v))
        self.chk_alarm.toggled.connect(lambda v: setattr(self.reloj_demo, 'alarmEnabled', v))
        self.txt_mensaje.textChanged.connect(lambda v: setattr(self.reloj_demo, 'alarmMessage', v))
        self.time_alarm.timeChanged.connect(lambda v: setattr(self.reloj_demo, 'alarmTime', v))
        self.spin_duracion.valueChanged.connect(lambda v: setattr(self.reloj_demo, 'duracionPartido', v))
        
        # 2. Botones -> Reloj
        self.btn_start.clicked.connect(self.reloj_demo.start)
        self.btn_pause.clicked.connect(self.reloj_demo.pause)
        self.btn_reset.clicked.connect(self.reloj_demo.reset)
        
        # 3. Señales del Reloj -> Interfaz (Requisito: "reflejarse en algún componente")
        self.reloj_demo.alarmTriggered.connect(self.mostrar_aviso)
        self.reloj_demo.timerFinished.connect(lambda: self.lbl_signal.setText("SEÑAL RECIBIDA: timerFinished()"))
        
        # Inicializar estado
        self.actualizar_reloj()

    def actualizar_reloj(self):
        idx = self.combo_mode.currentIndex()
        if idx == 0:
            self.reloj_demo.mode = ModoReloj.CLOCK
            self.spin_duracion.setEnabled(False)
            self.chk_countdown.setEnabled(False)
            self.time_alarm.setEnabled(True)
        else:
            self.reloj_demo.mode = ModoReloj.TIMER
            self.spin_duracion.setEnabled(True)
            self.chk_countdown.setEnabled(True)
            self.time_alarm.setEnabled(False)
            
            # Aplicar duración inicial
            self.reloj_demo.duracionPartido = self.spin_duracion.value()
            self.reloj_demo.reset()

    def mostrar_aviso(self, mensaje):
        self.lbl_signal.setText(f"ALARMA: {mensaje}")
        self.lbl_signal.setStyleSheet("color: white; font-size: 16px; margin-top: 20px; padding: 10px; background-color: #B71C1C; border-radius: 5px; font-weight: bold;")
        QMessageBox.information(self, "Aviso del Reloj", mensaje)
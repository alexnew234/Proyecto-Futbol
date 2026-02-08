from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
    QCheckBox, QComboBox, QSpinBox, QLineEdit, 
    QPushButton, QLabel, QTimeEdit, QMessageBox
)
from PySide6.QtCore import QTime, Qt, QCoreApplication, QEvent
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
        self.grupo_props = QGroupBox("")
        layout_props = QVBoxLayout()
        
        # Modo (Clock / Timer)
        self.lbl_modo = QLabel("")
        layout_props.addWidget(self.lbl_modo)
        self.combo_mode = QComboBox()
        layout_props.addWidget(self.combo_mode)
        
        # Formato 24h
        self.chk_24h = QCheckBox("")
        self.chk_24h.setChecked(True)
        layout_props.addWidget(self.chk_24h)
        
        # Cuenta Atrás (Nueva funcionalidad)
        self.chk_countdown = QCheckBox("")
        layout_props.addWidget(self.chk_countdown)
        
        self.grupo_props.setLayout(layout_props)
        layout_izq.addWidget(self.grupo_props)
        
        # 2. Grupo de Alarma y Tiempos
        self.grupo_alarma = QGroupBox("")
        layout_alarma = QVBoxLayout()
        
        # Activar Alarma
        self.chk_alarm = QCheckBox("")
        layout_alarma.addWidget(self.chk_alarm)
        
        # Mensaje
        self.lbl_mensaje = QLabel("")
        layout_alarma.addWidget(self.lbl_mensaje)
        self.txt_mensaje = QLineEdit("")
        layout_alarma.addWidget(self.txt_mensaje)
        
        # Hora Alarma (Para modo Reloj)
        self.lbl_hora_alarma = QLabel("")
        layout_alarma.addWidget(self.lbl_hora_alarma)
        self.time_alarm = QTimeEdit()
        self.time_alarm.setTime(QTime.currentTime().addSecs(60)) # Por defecto 1 min más
        layout_alarma.addWidget(self.time_alarm)
        
        # Duración (Para modo Timer)
        self.lbl_duracion = QLabel("")
        layout_alarma.addWidget(self.lbl_duracion)
        self.spin_duracion = QSpinBox()
        self.spin_duracion.setRange(0, 99999)
        self.spin_duracion.setValue(10) # 10 segundos para probar rápido
        layout_alarma.addWidget(self.spin_duracion)
        
        self.grupo_alarma.setLayout(layout_alarma)
        layout_izq.addWidget(self.grupo_alarma)
        
        # 3. Botones de Control
        self.grupo_ctrl = QGroupBox("")
        layout_ctrl = QHBoxLayout()
        
        self.btn_start = QPushButton("")
        self.btn_pause = QPushButton("")
        self.btn_reset = QPushButton("")
        
        # Estilos botones
        self.btn_start.setStyleSheet("background-color: #2d7d2d; color: white; font-weight: bold;")
        self.btn_pause.setStyleSheet("background-color: #d8a600; color: black; font-weight: bold;")
        self.btn_reset.setStyleSheet("background-color: #7d2d2d; color: white; font-weight: bold;")
        
        layout_ctrl.addWidget(self.btn_start)
        layout_ctrl.addWidget(self.btn_pause)
        layout_ctrl.addWidget(self.btn_reset)
        
        self.grupo_ctrl.setLayout(layout_ctrl)
        layout_izq.addWidget(self.grupo_ctrl)
        
        layout_izq.addStretch() # Empujar todo arriba
        
        # --- COLUMNA DERECHA: VISUALIZACIÓN ---
        panel_der = QWidget()
        panel_der.setStyleSheet("background-color: #222; border-radius: 15px;")
        layout_der = QVBoxLayout(panel_der)
        layout_der.setAlignment(Qt.AlignCenter)
        
        # Título
        self.lbl_demo = QLabel("")
        self.lbl_demo.setStyleSheet("color: #aaa; font-size: 14px; font-weight: bold; margin-bottom: 20px;")
        self.lbl_demo.setAlignment(Qt.AlignCenter)
        layout_der.addWidget(self.lbl_demo)
        
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
        self.lbl_signal = QLabel("")
        self.lbl_signal.setStyleSheet("color: white; font-size: 16px; margin-top: 20px; padding: 10px; background-color: #444; border-radius: 5px;")
        self.lbl_signal.setAlignment(Qt.AlignCenter)
        layout_der.addWidget(self.lbl_signal)
        
        # Añadir paneles al layout principal
        main_layout.addWidget(panel_izq, 40) # 40% ancho
        main_layout.addWidget(panel_der, 60) # 60% ancho
        
        # Valores por defecto traducibles
        self._alarm_default_messages = {
            "es": "¡Tiempo completado!",
            "en": "Time completed!"
        }
        self._signal_waiting_messages = {
            "es": "Esperando señal...",
            "en": "Waiting for signal..."
        }

        # CONEXIONES INTERNAS (Lógica de la vista)
        self.conectar_controles()
        self.retranslate_ui()
        # Asegurar que el modo inicial (reloj) muestre la hora actual
        self.actualizar_reloj()

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
        self.reloj_demo.timerFinished.connect(self.mostrar_timer_finished)
        
        # Inicializar estado
        self.actualizar_reloj()

    def obtener_config(self):
        """Devuelve la configuracion actual del reloj."""
        return {
            "modo": self.combo_mode.currentData(),
            "is24h": self.chk_24h.isChecked(),
            "countdown": self.chk_countdown.isChecked(),
            "alarm_enabled": self.chk_alarm.isChecked(),
            "alarm_message": self.txt_mensaje.text().strip(),
            "alarm_time": self.time_alarm.time(),
            "duracion": self.spin_duracion.value(),
        }

    def actualizar_reloj(self):
        modo = self.combo_mode.currentData()
        if modo is None:
            modo = ModoReloj.CLOCK if self.combo_mode.currentIndex() == 0 else ModoReloj.TIMER

        if modo == ModoReloj.CLOCK:
            self.reloj_demo.mode = ModoReloj.CLOCK
            self.spin_duracion.setEnabled(False)
            self.chk_countdown.setEnabled(False)
            self.time_alarm.setEnabled(True)
            # Forzar refresco inmediato y mantener reloj en marcha
            self.reloj_demo.reset()
            self.reloj_demo.start()
        else:
            self.reloj_demo.mode = ModoReloj.TIMER
            self.spin_duracion.setEnabled(True)
            self.chk_countdown.setEnabled(True)
            self.time_alarm.setEnabled(False)
            
            # Aplicar duración inicial
            self.reloj_demo.duracionPartido = self.spin_duracion.value()
            self.reloj_demo.reset()

    def mostrar_aviso(self, mensaje):
        texto = QCoreApplication.translate("RelojConfigView", "ALARMA: {mensaje}").format(mensaje=mensaje)
        self.lbl_signal.setText(texto)
        self.lbl_signal.setStyleSheet("color: white; font-size: 16px; margin-top: 20px; padding: 10px; background-color: #B71C1C; border-radius: 5px; font-weight: bold;")
        QMessageBox.information(self, QCoreApplication.translate("RelojConfigView", "Aviso del Reloj"), mensaje)

    def mostrar_timer_finished(self):
        texto = QCoreApplication.translate("RelojConfigView", "SEÑAL RECIBIDA: timerFinished()")
        self.lbl_signal.setText(texto)

    def retranslate_ui(self):
        # Grupo propiedades
        self.grupo_props.setTitle(QCoreApplication.translate("RelojConfigView", "Propiedades del Componente"))
        self.lbl_modo.setText(QCoreApplication.translate("RelojConfigView", "Modo de Funcionamiento:"))

        # Combo modo (mantener selección)
        current_mode = self.combo_mode.currentData()
        self.combo_mode.blockSignals(True)
        self.combo_mode.clear()
        self.combo_mode.addItem(QCoreApplication.translate("RelojConfigView", "Reloj Digital (Hora)"), ModoReloj.CLOCK)
        self.combo_mode.addItem(QCoreApplication.translate("RelojConfigView", "Cronómetro / Temporizador"), ModoReloj.TIMER)
        idx = self.combo_mode.findData(current_mode)
        self.combo_mode.setCurrentIndex(idx if idx >= 0 else 0)
        self.combo_mode.blockSignals(False)

        self.chk_24h.setText(QCoreApplication.translate("RelojConfigView", "Formato 24 Horas"))
        self.chk_countdown.setText(QCoreApplication.translate("RelojConfigView", "Modo Cuenta Regresiva (Solo Timer)"))

        # Grupo alarma
        self.grupo_alarma.setTitle(QCoreApplication.translate("RelojConfigView", "Configuración de Alarma y Tiempos"))
        self.chk_alarm.setText(QCoreApplication.translate("RelojConfigView", "Alarma Activada"))
        self.lbl_mensaje.setText(QCoreApplication.translate("RelojConfigView", "Mensaje de Alarma:"))
        self.lbl_hora_alarma.setText(QCoreApplication.translate("RelojConfigView", "Hora de Alarma (Modo Reloj):"))
        self.lbl_duracion.setText(QCoreApplication.translate("RelojConfigView", "Duración / Límite (Segundos):"))

        # Grupo control
        self.grupo_ctrl.setTitle(QCoreApplication.translate("RelojConfigView", "Control Manual"))
        self.btn_start.setText(QCoreApplication.translate("RelojConfigView", "Iniciar"))
        self.btn_pause.setText(QCoreApplication.translate("RelojConfigView", "Pausar"))
        self.btn_reset.setText(QCoreApplication.translate("RelojConfigView", "Reiniciar"))

        # Panel derecha
        self.lbl_demo.setText(QCoreApplication.translate("RelojConfigView", "VISTA PREVIA DEL COMPONENTE"))

        # Mensaje por defecto (solo si no fue editado por el usuario)
        nuevo_default = QCoreApplication.translate("RelojConfigView", "¡Tiempo completado!")
        if (not self.txt_mensaje.text()) or (self.txt_mensaje.text() in self._alarm_default_messages.values()):
            self.txt_mensaje.setText(nuevo_default)
        self.reloj_demo.alarmMessage = self.txt_mensaje.text()
        
        # Señal esperando (solo si está en valores por defecto)
        nuevo_wait = QCoreApplication.translate("RelojConfigView", "Esperando señal...")
        texto_actual = self.lbl_signal.text()
        if (not texto_actual) or (texto_actual in self._signal_waiting_messages.values()):
            self.lbl_signal.setText(nuevo_wait)
        if texto_actual in (
            "SEÑAL RECIBIDA: timerFinished()",
            "SIGNAL RECEIVED: timerFinished()"
        ):
            self.lbl_signal.setText(QCoreApplication.translate("RelojConfigView", "SEÑAL RECIBIDA: timerFinished()"))

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()

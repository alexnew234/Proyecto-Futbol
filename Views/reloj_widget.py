from enum import Enum
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, QTime, Signal, Property, Slot, Qt
from Views.reloj_widget_ui import Ui_Form

class ModoReloj(Enum):
    CLOCK = "clock"       # Reloj de sistema
    TIMER = "timer"       # Cronómetro / Temporizador

class RelojDigital(QWidget):
    alarmTriggered = Signal(str)  # Mensaje de texto al saltar alarma
    timerFinished = Signal()      # Señal específica al finalizar el tiempo

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # =========================================================
        # 🟢 COMPRESOR DE LAYOUT (Estilo visual)
        # =========================================================
        layout = self.layout()
        if not layout:
             children = self.findChildren(QHBoxLayout)
             if children: layout = children[0]

        if layout:
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setAlignment(Qt.AlignCenter)
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item.spacerItem():
                    item.spacerItem().changeSize(0, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.invalidate()
            layout.activate()
        # =========================================================

        # --- Variables Internas ---
        self._mode = ModoReloj.CLOCK
        self._is24Hour = True
        
        # Alarma
        self._alarmEnabled = False
        self._alarmTime = QTime(0, 0)
        self._alarmMessage = "¡Aviso del Reloj!"
        
        # Variables Timer/Cronómetro
        self._segundos_transcurridos = 0
        self._limite_cronometro = 90 * 60  # Duración (ej. partido)
        self._isCountDown = False          

        # Timer interno (1 segundo)
        self.timer_interno = QTimer(self)
        self.timer_interno.timeout.connect(self._procesar_logica)
        self.timer_interno.setInterval(1000)

    # =========================================================
    #  PROPIEDADES PÚBLICAS
    # =========================================================

    @Property(ModoReloj)
    def mode(self): return self._mode
    @mode.setter
    def mode(self, value):
        if self._mode != value:
            self._mode = value
            self.reset()
            self._actualizar_pantalla_inmediata()

    @Property(bool)
    def is24Hour(self): return self._is24Hour
    @is24Hour.setter
    def is24Hour(self, value):
        self._is24Hour = value
        self._actualizar_pantalla_inmediata()

    @Property(bool)
    def isCountDown(self): return self._isCountDown
    @isCountDown.setter
    def isCountDown(self, value):
        self._isCountDown = value
        self.reset() 

    @Property(bool)
    def alarmEnabled(self): return self._alarmEnabled
    @alarmEnabled.setter
    def alarmEnabled(self, value): self._alarmEnabled = value

    @Property(str)
    def alarmMessage(self): return self._alarmMessage
    @alarmMessage.setter
    def alarmMessage(self, value): self._alarmMessage = value

    @Property(QTime)
    def alarmTime(self): return self._alarmTime
    @alarmTime.setter
    def alarmTime(self, value): self._alarmTime = value

    @Property(int)
    def duracionPartido(self): return self._limite_cronometro
    @duracionPartido.setter
    def duracionPartido(self, segundos): 
        self._limite_cronometro = segundos
        if self._mode == ModoReloj.TIMER and self._isCountDown and not self.timer_interno.isActive():
            self.reset()

    # =========================================================
    #  MÉTODOS PÚBLICOS (Slots)
    # =========================================================
    @Slot()
    def start(self):
        if not self.timer_interno.isActive():
            self.timer_interno.start()

    @Slot()
    def pause(self):
        self.timer_interno.stop()

    @Slot()
    def reset(self):
        self.timer_interno.stop()
        if self._mode == ModoReloj.TIMER and self._isCountDown:
            self._segundos_transcurridos = self._limite_cronometro
        else:
            self._segundos_transcurridos = 0
        self._actualizar_pantalla_inmediata()

    # =========================================================
    #  LÓGICA INTERNA
    # =========================================================
    def _procesar_logica(self):
        
        # --- MODO RELOJ ---
        if self._mode == ModoReloj.CLOCK:
            hora_actual = QTime.currentTime()
            self._pintar_tiempo(hora_actual)
            
            if (self._alarmEnabled and 
                hora_actual.hour() == self._alarmTime.hour() and 
                hora_actual.minute() == self._alarmTime.minute() and 
                hora_actual.second() == 0):
                self.alarmTriggered.emit(self._alarmMessage)

        # --- MODO TIMER ---
        elif self._mode == ModoReloj.TIMER:
            if self._isCountDown:
                self._segundos_transcurridos -= 1
                if self._segundos_transcurridos <= 0:
                    self._segundos_transcurridos = 0
                    self._pintar_tiempo_segundos(0) 
                    self.timerFinished.emit()               
                    if self._alarmEnabled:
                        self.alarmTriggered.emit(self._alarmMessage)
                    self.pause()
                    return 

            else:
                self._segundos_transcurridos += 1
                if self._alarmEnabled and self._segundos_transcurridos >= self._limite_cronometro:
                    self.timerFinished.emit()               
                    self.alarmTriggered.emit(self._alarmMessage)
                    self.pause()

            self._pintar_tiempo_segundos(self._segundos_transcurridos)

    def _pintar_tiempo_segundos(self, segundos_totales):
        segundos_totales = max(0, segundos_totales)
        t = QTime(0, 0).addSecs(segundos_totales)
        # En modo Timer/Cronómetro, siempre pintamos HH:mm:ss como duración (formato 24h visual)
        # para evitar confusiones de AM/PM en un contador.
        texto = t.toString("HH:mm:ss")
        self._actualizar_labels(texto)

    def _pintar_tiempo(self, tiempo: QTime):
        # --- CORRECCIÓN FORMATO 12/24 HORAS ---
        if self._is24Hour:
            # Formato 24h estándar (00-23)
            texto = tiempo.toString("HH:mm:ss")
        else:
            # Formato 12h MANUAL (01-12)
            # Calculamos la hora manualmente para evitar líos con el string de Qt
            h = tiempo.hour()
            h_12 = h % 12
            if h_12 == 0: h_12 = 12
            
            # Construimos el string a mano: "05:30:00"
            texto = f"{h_12:02d}:{tiempo.minute():02d}:{tiempo.second():02d}"
            
        self._actualizar_labels(texto)

    def _actualizar_labels(self, texto):
        """Reparte el string HH:mm:ss en los 3 labels"""
        partes = texto.split(":")
        if len(partes) == 3:
            self.ui.label_horas.setText(partes[0])
            self.ui.label_minutos.setText(partes[1])
            self.ui.label_segundos.setText(partes[2])

    def _actualizar_pantalla_inmediata(self):
        if self._mode == ModoReloj.CLOCK:
            self._pintar_tiempo(QTime.currentTime())
        else:
            self._pintar_tiempo_segundos(self._segundos_transcurridos)
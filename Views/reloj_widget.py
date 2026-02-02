from enum import Enum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QTime, Signal, Property, Qt
from Views.reloj_widget_ui import Ui_Form

class ModoReloj(Enum):
    CLOCK = "clock"
    TIMER = "timer"

class RelojDigital(QWidget):
    # Señales requeridas
    alarmTriggered = Signal(str)
    timerFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Variables internas
        self._mode = ModoReloj.CLOCK
        self._is24Hour = True
        self._alarmEnabled = False
        self._alarmHour = 0
        self._alarmMinute = 0
        self._alarmMessage = "¡Tiempo finalizado!"
        
        # Variables para el cronómetro/temporizador
        self._segundos_transcurridos = 0 
        self._tiempo_limite = 90 * 60 # 90 minutos por defecto (en segundos)

        # Timer interno (1 segundo)
        self.timer_actualizacion = QTimer(self)
        self.timer_actualizacion.timeout.connect(self._actualizar_logica)
        # No iniciamos automático para que el botón "Iniciar" tenga sentido
        # self.timer_actualizacion.start(1000) 

    # --- PROPIEDADES ---
    @Property(ModoReloj)
    def mode(self): return self._mode
    @mode.setter
    def mode(self, value): 
        self._mode = value
        self._actualizar_display_inicial()

    @Property(bool)
    def is24Hour(self): return self._is24Hour
    @is24Hour.setter
    def is24Hour(self, value): self._is24Hour = value

    @Property(str)
    def alarmMessage(self): return self._alarmMessage
    @alarmMessage.setter
    def alarmMessage(self, value): self._alarmMessage = value

    # --- LÓGICA DE TIEMPO ---
    def _actualizar_logica(self):
        # MODO RELOJ (Hora del sistema)
        if self._mode == ModoReloj.CLOCK:
            tiempo_actual = QTime.currentTime()
            formato = "HH:mm:ss" if self._is24Hour else "hh:mm:ss"
            self._pintar_texto(tiempo_actual.toString(formato))
            
            # Comprobar alarma horaria
            if (self._alarmEnabled and 
                tiempo_actual.hour() == self._alarmHour and 
                tiempo_actual.minute() == self._alarmMinute and 
                tiempo_actual.second() == 0):
                self.alarmTriggered.emit(self._alarmMessage)

        # MODO TIMER (Cronómetro que cuenta hacia arriba)
        elif self._mode == ModoReloj.TIMER:
            self._segundos_transcurridos += 1
            
            # Convertir segundos totales a HH:MM:SS
            horas = self._segundos_transcurridos // 3600
            minutos = (self._segundos_transcurridos % 3600) // 60
            segundos = self._segundos_transcurridos % 60
            
            texto = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
            self._pintar_texto(texto)
            
            # Comprobar si llega al límite (ej. 90 min) para lanzar alarma
            if self._alarmEnabled and self._segundos_transcurridos >= self._tiempo_limite:
                 self.alarmTriggered.emit(self._alarmMessage)
                 self.timerFinished.emit()
                 self.pause() # Detener al terminar

    def _pintar_texto(self, texto_tiempo):
        partes = texto_tiempo.split(":")
        # Aseguramos que hay 3 partes, si no, rellenamos
        if len(partes) == 3:
            self.ui.label_horas.setText(partes[0])
            self.ui.label_minutos.setText(partes[1])
            self.ui.label_segundos.setText(partes[2])

    def _actualizar_display_inicial(self):
        # Pone el marcador a 00:00:00 si cambiamos a Timer
        if self._mode == ModoReloj.TIMER:
            self._pintar_texto("00:00:00")

    # --- MÉTODOS PÚBLICOS (Controles) ---
    def start(self): 
        if not self.timer_actualizacion.isActive():
            self.timer_actualizacion.start(1000) # 1000 ms = 1 segundo
            
    def pause(self): 
        self.timer_actualizacion.stop()
        
    def reset(self):
        self.timer_actualizacion.stop()
        self._segundos_transcurridos = 0
        self._actualizar_display_inicial()
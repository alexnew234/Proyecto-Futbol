from enum import Enum
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer, QTime, Signal, Property, Slot
from Views.reloj_widget_ui import Ui_Form

# [Requisito: Propiedad mode de tipo enumerado]
class ModoReloj(Enum):
    CLOCK = "clock"       # Muestra la hora actual del sistema
    TIMER = "timer"       # Funciona como cronómetro de partido

class RelojDigital(QWidget):
    # [Requisito: Eventos propios expuestos]
    alarmTriggered = Signal(str)  # Se emite cuando salta la alarma
    timerFinished = Signal()      # Se emite cuando el tiempo acaba

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Variables internas (Gestión interna, sin acceso externo directo)
        self._mode = ModoReloj.CLOCK
        self._is24Hour = True
        
        # Variables de Alarma y Tiempo
        self._alarmEnabled = False
        self._alarmTime = QTime(0, 0)      # Hora para alarma en modo Reloj
        self._alarmMessage = "¡Aviso del Reloj!"
        
        # Variables exclusivas del modo Temporizador/Cronómetro
        self._segundos_transcurridos = 0
        self._limite_cronometro = 90 * 60  # Duración por defecto (90 min)

        # [Requisito: Gestión interna del paso del tiempo]
        self.timer_interno = QTimer(self)
        self.timer_interno.timeout.connect(self._procesar_logica)
        self.timer_interno.setInterval(1000) # 1 segundo exacto

    # =========================================================
    #  PROPIEDADES PÚBLICAS (Configuración desde la App)
    # =========================================================

    @Property(ModoReloj)
    def mode(self): return self._mode
    @mode.setter
    def mode(self, value):
        if self._mode != value:
            self._mode = value
            self.reset() # Reiniciar contadores al cambiar de contexto
            self._actualizar_pantalla_inmediata()

    @Property(bool)
    def is24Hour(self): return self._is24Hour
    @is24Hour.setter
    def is24Hour(self, value):
        self._is24Hour = value
        self._actualizar_pantalla_inmediata()

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

    # Propiedad extra para configurar la duración del partido desde fuera
    @Property(int)
    def duracionPartido(self): return self._limite_cronometro
    @duracionPartido.setter
    def duracionPartido(self, segundos): self._limite_cronometro = segundos

    # =========================================================
    #  MÉTODOS PÚBLICOS (Control externo)
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
        self._segundos_transcurridos = 0
        self._actualizar_pantalla_inmediata()

    # =========================================================
    #  LÓGICA INTERNA (El "cerebro" del componente)
    # =========================================================
    def _procesar_logica(self):
        """Se ejecuta cada segundo y decide qué hacer según el modo"""
        
        # --- CASO 1: MODO RELOJ DIGITAL (Hora del sistema) ---
        if self._mode == ModoReloj.CLOCK:
            hora_actual = QTime.currentTime()
            self._pintar_tiempo(hora_actual)
            
            # Lógica de Alarma de Reloj (ej. "Avisar a las 14:00")
            if (self._alarmEnabled and 
                hora_actual.hour() == self._alarmTime.hour() and 
                hora_actual.minute() == self._alarmTime.minute() and 
                hora_actual.second() == 0):
                self.alarmTriggered.emit(self._alarmMessage)

        # --- CASO 2: MODO CRONÓMETRO (Partido de Fútbol) ---
        elif self._mode == ModoReloj.TIMER:
            self._segundos_transcurridos += 1
            
            # Convertir segundos a QTime para pintar
            t = QTime(0, 0).addSecs(self._segundos_transcurridos)
            self._pintar_tiempo(t)

            # Lógica de Alarma de Partido (ej. "Avisar al minuto 90")
            if self._alarmEnabled and self._segundos_transcurridos >= self._limite_cronometro:
                self.alarmTriggered.emit(self._alarmMessage) # Reflejo en interfaz
                self.timerFinished.emit()
                self.pause() # Parar automáticamente

    def _pintar_tiempo(self, tiempo: QTime):
        """Actualiza la UI visualmente"""
        formato = "HH:mm:ss" if self._is24Hour else "hh:mm:ss"
        texto = tiempo.toString(formato)
        partes = texto.split(":")
        if len(partes) == 3:
            self.ui.label_horas.setText(partes[0])
            self.ui.label_minutos.setText(partes[1])
            self.ui.label_segundos.setText(partes[2])

    def _actualizar_pantalla_inmediata(self):
        """Refresca la pantalla sin esperar 1 segundo"""
        if self._mode == ModoReloj.CLOCK:
            self._pintar_tiempo(QTime.currentTime())
        else:
            self._pintar_tiempo(QTime(0,0).addSecs(self._segundos_transcurridos))
from enum import Enum
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, QTime, Signal, Property, Slot, Qt
from Views.reloj_widget_ui import Ui_Form

class ModoReloj(Enum):
    CLOCK = "clock"
    TIMER = "timer"

class RelojDigital(QWidget):
    alarmTriggered = Signal(str)
    timerFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # =========================================================
        # 🟢 COMPRESOR DE LAYOUT (Versión Definitiva)
        # =========================================================
        # 1. Intentamos obtener el layout principal del propio widget
        layout = self.layout()
        
        # 2. Si no tiene layout directo, buscamos si hay uno horizontal dentro
        if not layout:
             children = self.findChildren(QHBoxLayout)
             if children:
                 layout = children[0]

        if layout:
            # 3. Eliminar el espaciado entre elementos y los márgenes
            layout.setSpacing(0)
            layout.setContentsMargins(0, 0, 0, 0)
            # Alineamos al centro para que el bloque quede centrado
            layout.setAlignment(Qt.AlignCenter)
            
            # 4. BUSCAR Y APLASTAR LOS SEPARADORES (Spacers)
            # Iteramos por todos los elementos del layout
            for i in range(layout.count()):
                item = layout.itemAt(i)
                # Si el elemento es un "muelle" (spacer)
                if item.spacerItem():
                    # Lo forzamos a tener tamaño 0 píxeles
                    item.spacerItem().changeSize(0, 0, QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            # 5. Forzar la actualización inmediata del layout
            layout.invalidate()
            layout.activate()
        # =========================================================

        # Variables internas
        self._mode = ModoReloj.CLOCK
        self._is24Hour = True
        
        self._alarmEnabled = False
        self._alarmTime = QTime(0, 0)
        self._alarmMessage = "¡Aviso del Reloj!"
        
        self._segundos_transcurridos = 0
        self._limite_cronometro = 90 * 60

        self.timer_interno = QTimer(self)
        self.timer_interno.timeout.connect(self._procesar_logica)
        self.timer_interno.setInterval(1000)

    # --- PROPIEDADES ---
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
    def duracionPartido(self, segundos): self._limite_cronometro = segundos

    # --- MÉTODOS PÚBLICOS ---
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

    # --- LÓGICA INTERNA ---
    def _procesar_logica(self):
        if self._mode == ModoReloj.CLOCK:
            hora_actual = QTime.currentTime()
            self._pintar_tiempo(hora_actual)
            
            if (self._alarmEnabled and 
                hora_actual.hour() == self._alarmTime.hour() and 
                hora_actual.minute() == self._alarmTime.minute() and 
                hora_actual.second() == 0):
                self.alarmTriggered.emit(self._alarmMessage)

        elif self._mode == ModoReloj.TIMER:
            self._segundos_transcurridos += 1
            t = QTime(0, 0).addSecs(self._segundos_transcurridos)
            self._pintar_tiempo(t)

            if self._alarmEnabled and self._segundos_transcurridos >= self._limite_cronometro:
                self.alarmTriggered.emit(self._alarmMessage)
                self.timerFinished.emit()
                self.pause()

    def _pintar_tiempo(self, tiempo: QTime):
        formato = "HH:mm:ss" if self._is24Hour else "hh:mm:ss"
        texto = tiempo.toString(formato)
        partes = texto.split(":")
        if len(partes) == 3:
            self.ui.label_horas.setText(partes[0])
            self.ui.label_minutos.setText(partes[1])
            self.ui.label_segundos.setText(partes[2])

    def _actualizar_pantalla_inmediata(self):
        if self._mode == ModoReloj.CLOCK:
            self._pintar_tiempo(QTime.currentTime())
        else:
            self._pintar_tiempo(QTime(0,0).addSecs(self._segundos_transcurridos))
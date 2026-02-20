from PySide6.QtCore import QDate, QEvent
from PySide6.QtWidgets import QDialog, QFileDialog

from Views.reports_window_ui import Ui_ReportsWindow


class ReportsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ReportsWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(860, 600)

        self._bind_compat_attrs()
        self._setup_defaults()

    def retranslate_ui(self):
        self.ui.retranslateUi(self)

    def _bind_compat_attrs(self):
        # Compatibilidad con el controlador actual (acceso directo a widgets).
        self.combo_report = self.ui.combo_report
        self.combo_equipo = self.ui.combo_equipo
        self.input_jugador_destacado = self.ui.input_jugador_destacado
        self.combo_eliminatoria = self.ui.combo_eliminatoria
        self.chk_fecha_desde = self.ui.chk_fecha_desde
        self.date_desde = self.ui.date_desde
        self.chk_fecha_hasta = self.ui.chk_fecha_hasta
        self.date_hasta = self.ui.date_hasta
        self.input_output_dir = self.ui.input_output_dir
        self.btn_browse = self.ui.btn_browse
        self.btn_open_folder = self.ui.btn_open_folder
        self.chk_export_csv = self.ui.chk_export_csv
        self.chk_force_native = self.ui.chk_force_native
        self.btn_generar = self.ui.btn_generar
        self.lbl_engine = self.ui.lbl_engine
        self.output_log = self.ui.output_log

    def _setup_defaults(self):
        self.combo_report.setItemData(0, "equipos_jugadores")
        self.combo_report.setItemData(1, "partidos_resultados")
        self.combo_report.setItemData(2, "clasificacion_eliminatorias")

        self.combo_equipo.clear()
        self.combo_equipo.addItem("Todos", "")

        self.date_desde.setDate(QDate.currentDate().addMonths(-1))
        self.date_hasta.setDate(QDate.currentDate())
        self.date_desde.setEnabled(False)
        self.date_hasta.setEnabled(False)
        self.chk_fecha_desde.toggled.connect(self.date_desde.setEnabled)
        self.chk_fecha_hasta.toggled.connect(self.date_hasta.setEnabled)

    def browse_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de salida")
        if folder:
            self.input_output_dir.setText(folder)

    def append_log(self, text):
        self.output_log.appendPlainText(text)

    def clear_log(self):
        self.output_log.clear()

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == QEvent.LanguageChange:
            self.retranslate_ui()

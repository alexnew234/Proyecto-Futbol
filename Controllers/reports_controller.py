import os
import traceback

from PySide6.QtWidgets import QFileDialog, QMessageBox

from Models.reports_service import ReportsService
from Views.reports_window import ReportsWindow


class ReportsController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.service = ReportsService()
        self.view = ReportsWindow(main_window)

        self.view.input_output_dir.setText(self.service.get_default_output_dir())

        self._load_filter_values()
        self._connect_signals()
        self._update_filter_visibility()

    def _connect_signals(self):
        self.view.btn_browse.clicked.connect(self._browse_output_dir)
        self.view.btn_open_folder.clicked.connect(self._open_output_dir)
        self.view.btn_generar.clicked.connect(self.generate_report)
        self.view.combo_report.currentIndexChanged.connect(self._update_filter_visibility)

    def show(self):
        self._load_filter_values()
        self.view.show()
        self.view.raise_()
        self.view.activateWindow()

    def _load_filter_values(self):
        current_team = self.view.combo_equipo.currentData() if self.view.combo_equipo.count() else ""
        self.view.combo_equipo.blockSignals(True)
        self.view.combo_equipo.clear()
        self.view.combo_equipo.addItem("Todos", "")
        try:
            for team in self.service.list_equipos():
                self.view.combo_equipo.addItem(team, team)
        except Exception:
            pass

        if current_team:
            idx = self.view.combo_equipo.findData(current_team)
            if idx >= 0:
                self.view.combo_equipo.setCurrentIndex(idx)
        self.view.combo_equipo.blockSignals(False)

        current_fase = self.view.combo_eliminatoria.currentText() if self.view.combo_eliminatoria.count() else ""
        self.view.combo_eliminatoria.blockSignals(True)
        self.view.combo_eliminatoria.clear()
        self.view.combo_eliminatoria.addItem("Todas")
        fases = ["Octavos", "Cuartos", "Semifinal", "Final"]
        try:
            db_fases = self.service.list_fases()
            if db_fases:
                fases = db_fases
        except Exception:
            pass
        self.view.combo_eliminatoria.addItems(fases)

        if current_fase:
            idx = self.view.combo_eliminatoria.findText(current_fase)
            if idx >= 0:
                self.view.combo_eliminatoria.setCurrentIndex(idx)
        self.view.combo_eliminatoria.blockSignals(False)

    def _update_filter_visibility(self):
        report_key = self.view.combo_report.currentData()
        equipos_report = report_key == "equipos_jugadores"

        self.view.combo_equipo.setEnabled(equipos_report)
        self.view.input_jugador_destacado.setEnabled(equipos_report)

        self.view.combo_eliminatoria.setEnabled(not equipos_report)
        self.view.chk_fecha_desde.setEnabled(True)
        self.view.chk_fecha_hasta.setEnabled(True)

    def _browse_output_dir(self):
        folder = QFileDialog.getExistingDirectory(self.main_window, "Seleccionar carpeta de salida")
        if folder:
            self.view.input_output_dir.setText(folder)

    def _open_output_dir(self):
        folder = (self.view.input_output_dir.text() or "").strip()
        if not folder:
            folder = self.service.get_default_output_dir()
            self.view.input_output_dir.setText(folder)

        os.makedirs(folder, exist_ok=True)
        os.startfile(folder)

    def _collect_filters(self):
        fecha_desde = ""
        fecha_hasta = ""
        if self.view.chk_fecha_desde.isChecked():
            fecha_desde = self.view.date_desde.date().toString("yyyy-MM-dd")
        if self.view.chk_fecha_hasta.isChecked():
            fecha_hasta = self.view.date_hasta.date().toString("yyyy-MM-dd")

        fase = self.view.combo_eliminatoria.currentText().strip()
        if fase.lower() == "todas":
            fase = ""

        return {
            "equipo": self.view.combo_equipo.currentData() or "",
            "jugador_destacado": self.view.input_jugador_destacado.text().strip(),
            "eliminatoria": fase,
            "fecha_desde": fecha_desde,
            "fecha_hasta": fecha_hasta,
        }

    def generate_report(self):
        report_key = self.view.combo_report.currentData()
        output_dir = (self.view.input_output_dir.text() or "").strip()
        if not output_dir:
            output_dir = self.service.get_default_output_dir()
            self.view.input_output_dir.setText(output_dir)

        filters = self._collect_filters()
        export_csv = self.view.chk_export_csv.isChecked()
        force_native = self.view.chk_force_native.isChecked()

        self.view.clear_log()
        self.view.append_log("Iniciando generacion...")
        self.view.append_log(f"- Informe: {self.view.combo_report.currentText()}")
        self.view.append_log(f"- Destino PDF/CSV: {output_dir}")

        try:
            result = self.service.generate_report(
                report_key=report_key,
                filters=filters,
                output_dir=output_dir,
                export_csv=export_csv,
                force_native=force_native,
            )

            self.view.lbl_engine.setText(f"Motor: {result['engine']}")
            self.view.append_log(f"PDF generado: {result['pdf_path']}")
            if result.get("csv_path"):
                self.view.append_log(f"CSV generado: {result['csv_path']}")
            if result.get("jasper_path"):
                self.view.append_log(f"Jasper compilado: {result['jasper_path']}")
            self.view.append_log(f"Plantilla JRXML: {result['jrxml_path']}")

            for warning in result.get("warnings", []):
                self.view.append_log(f"[AVISO] {warning}")

            QMessageBox.information(
                self.main_window,
                "Informes",
                f"Informe generado correctamente con motor {result['engine']}.\n\nPDF:\n{result['pdf_path']}",
            )
        except Exception as exc:
            self.view.lbl_engine.setText("Motor: error")
            self.view.append_log("[ERROR] Fallo al generar el informe")
            self.view.append_log(str(exc))
            self.view.append_log(traceback.format_exc())
            QMessageBox.critical(
                self.main_window,
                "Error al generar informe",
                f"No se pudo generar el informe.\n\n{exc}",
            )

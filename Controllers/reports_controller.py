import os
import traceback

from PySide6.QtWidgets import QFileDialog, QMessageBox

from Models.reports_service import ReportsService
from Views.reports_window import ReportsWindow


class ReportsController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_controller = getattr(main_window, "main_controller", None)
        self.service = ReportsService()
        self.view = ReportsWindow(main_window)

        self.view.input_output_dir.setText(self.service.get_default_output_dir())

        self._load_filter_values()
        self._connect_signals()
        self._update_filter_visibility()

    def _is_english(self):
        ctrl = self.main_controller or getattr(self.main_window, "main_controller", None)
        return bool(ctrl and getattr(ctrl, "current_language", "es") == "en")

    def _tr(self, es, en):
        return en if self._is_english() else es

    def _connect_signals(self):
        self.view.btn_browse.clicked.connect(self._browse_output_dir)
        self.view.btn_open_folder.clicked.connect(self._open_output_dir)
        self.view.btn_generar.clicked.connect(self.generate_report)
        self.view.combo_report.currentIndexChanged.connect(self._update_filter_visibility)

    def show(self):
        self.retranslate_ui()
        self._load_filter_values()
        self.view.show()
        self.view.raise_()
        self.view.activateWindow()

    def retranslate_ui(self):
        self.view.retranslate_ui()
        self._apply_manual_texts()
        # Reponer claves internas tras retraducir la UI
        self.view.combo_report.setItemData(0, "equipos_jugadores")
        self.view.combo_report.setItemData(1, "partidos_resultados")
        self.view.combo_report.setItemData(2, "clasificacion_eliminatorias")
        self._load_filter_values()
        self._update_filter_visibility()

    def _apply_manual_texts(self):
        ui = self.view.ui

        self.view.setWindowTitle(self._tr("Centro de Informes", "Reports Center"))
        ui.label_title.setText(self._tr("Informes del Torneo", "Tournament Reports"))
        ui.label_desc.setText(
            self._tr(
                "Genera PDF y CSV para Equipos/Jugadores, Partidos/Resultados y Clasificacion/Eliminatorias.",
                "Generate PDF and CSV for Teams/Players, Matches/Results and Standings/Knockout Stage.",
            )
        )
        ui.groupBox.setTitle(self._tr("Configuracion del informe", "Report settings"))

        ui.label_tipo.setText(self._tr("Tipo de informe:", "Report type:"))
        ui.combo_report.setItemText(0, self._tr("Informe Equipos y Jugadores", "Teams and Players Report"))
        ui.combo_report.setItemText(1, self._tr("Informe Partidos y Resultados", "Matches and Results Report"))
        ui.combo_report.setItemText(
            2, self._tr("Informe Clasificacion y Eliminatorias", "Standings and Knockout Stage Report")
        )

        ui.label_equipo.setText(self._tr("Equipo (opcional):", "Team (optional):"))
        ui.label_jugador.setText(self._tr("Jugador destacado (opcional):", "Highlighted player (optional):"))
        ui.input_jugador_destacado.setPlaceholderText(self._tr("Nombre o parte del nombre", "Name or part of name"))

        ui.label_eliminatoria.setText(self._tr("Eliminatoria (opcional):", "Knockout stage (optional):"))
        ui.combo_eliminatoria.setItemText(0, self._tr("Todas", "All"))
        ui.combo_eliminatoria.setItemText(1, self._tr("Octavos", "Round of 16"))
        ui.combo_eliminatoria.setItemText(2, self._tr("Cuartos", "Quarterfinals"))
        ui.combo_eliminatoria.setItemText(3, self._tr("Semifinal", "Semifinal"))
        ui.combo_eliminatoria.setItemText(4, self._tr("Final", "Final"))

        ui.label_fechas.setText(self._tr("Rango de fechas:", "Date range:"))
        ui.chk_fecha_desde.setText(self._tr("Desde", "From"))
        ui.chk_fecha_hasta.setText(self._tr("Hasta", "To"))

        ui.label_destino.setText(self._tr("Destino PDF/CSV:", "PDF/CSV output:"))
        ui.btn_browse.setText(self._tr("Examinar...", "Browse..."))
        ui.btn_open_folder.setText(self._tr("Abrir carpeta", "Open folder"))

        ui.label_opciones.setText(self._tr("Opciones:", "Options:"))
        ui.chk_export_csv.setText(self._tr("Exportar CSV", "Export CSV"))
        ui.chk_force_native.setText(self._tr("Forzar motor nativo (sin Jasper)", "Force native engine (without Jasper)"))

        ui.btn_generar.setText(self._tr("Generar y guardar", "Generate and save"))
        ui.lbl_engine.setText(self._tr("Motor: -", "Engine: -"))
        ui.output_log.setPlaceholderText(self._tr("Estado de la generacion...", "Generation status..."))

    def _load_filter_values(self):
        current_team = self.view.combo_equipo.currentData() if self.view.combo_equipo.count() else ""
        self.view.combo_equipo.blockSignals(True)
        self.view.combo_equipo.clear()
        self.view.combo_equipo.addItem(self._tr("Todos", "All"), "")
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

        current_fase = self.view.combo_eliminatoria.currentData() if self.view.combo_eliminatoria.count() else ""
        self.view.combo_eliminatoria.blockSignals(True)
        self.view.combo_eliminatoria.clear()
        self.view.combo_eliminatoria.addItem(self._tr("Todas", "All"), "")
        fases = ["Octavos", "Cuartos", "Semifinal", "Final"]
        try:
            db_fases = self.service.list_fases()
            if db_fases:
                fases = db_fases
        except Exception:
            pass
        for fase in fases:
            fase_display = {
                "Octavos": self._tr("Octavos", "Round of 16"),
                "Cuartos": self._tr("Cuartos", "Quarterfinals"),
                "Semifinal": self._tr("Semifinal", "Semifinal"),
                "Final": self._tr("Final", "Final"),
            }.get(fase, fase)
            self.view.combo_eliminatoria.addItem(fase_display, fase)

        if current_fase is not None:
            idx = self.view.combo_eliminatoria.findData(current_fase)
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
        folder = QFileDialog.getExistingDirectory(
            self.main_window, self._tr("Seleccionar carpeta de salida", "Select output folder")
        )
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

        fase = (self.view.combo_eliminatoria.currentData() or "").strip()

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
        self.view.append_log(self._tr("Iniciando generacion...", "Starting generation..."))
        self.view.append_log(f"- {self._tr('Informe', 'Report')}: {self.view.combo_report.currentText()}")
        self.view.append_log(f"- {self._tr('Destino PDF/CSV', 'PDF/CSV output')}: {output_dir}")

        try:
            result = self.service.generate_report(
                report_key=report_key,
                filters=filters,
                output_dir=output_dir,
                export_csv=export_csv,
                force_native=force_native,
            )

            self.view.lbl_engine.setText(f"{self._tr('Motor', 'Engine')}: {result['engine']}")
            self.view.append_log(f"{self._tr('PDF generado', 'PDF generated')}: {result['pdf_path']}")
            if result.get("csv_path"):
                self.view.append_log(f"{self._tr('CSV generado', 'CSV generated')}: {result['csv_path']}")
            if result.get("jasper_path"):
                self.view.append_log(f"{self._tr('Jasper compilado', 'Compiled Jasper')}: {result['jasper_path']}")
            self.view.append_log(f"{self._tr('Plantilla JRXML', 'JRXML template')}: {result['jrxml_path']}")

            for warning in result.get("warnings", []):
                self.view.append_log(f"[{self._tr('AVISO', 'WARNING')}] {warning}")

            QMessageBox.information(
                self.main_window,
                self._tr("Informes", "Reports"),
                self._tr(
                    f"Informe generado correctamente con motor {result['engine']}.\n\nPDF:\n{result['pdf_path']}",
                    f"Report generated successfully with {result['engine']} engine.\n\nPDF:\n{result['pdf_path']}",
                ),
            )
        except Exception as exc:
            self.view.lbl_engine.setText(f"{self._tr('Motor', 'Engine')}: error")
            self.view.append_log(f"[ERROR] {self._tr('Fallo al generar el informe', 'Failed to generate report')}")
            self.view.append_log(str(exc))
            self.view.append_log(traceback.format_exc())
            QMessageBox.critical(
                self.main_window,
                self._tr("Error al generar informe", "Error generating report"),
                self._tr(f"No se pudo generar el informe.\n\n{exc}", f"Could not generate report.\n\n{exc}"),
            )

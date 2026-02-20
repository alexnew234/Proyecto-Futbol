from PySide6.QtWidgets import QAbstractItemView, QMenu, QMessageBox, QTableWidgetItem
from PySide6.QtSql import QSqlQuery
from Controllers.universal_controller import UniversalController


class ParticipantesController:
    def __init__(self, main_window):
        self.main_view = main_window
        self.main_controller = None
        self.ventana_nuevo = None

        # Ocultar boton legado "Generar rondas" en esta pagina
        if hasattr(self.main_view.ui, "btn_generar_rondas"):
            self.main_view.ui.btn_generar_rondas.hide()
        if hasattr(self.main_view.ui, "pushButton_generar_rondas"):
            self.main_view.ui.pushButton_generar_rondas.hide()
        if hasattr(self.main_view.ui, "btn_generar_ronda"):
            self.main_view.ui.btn_generar_ronda.hide()

        self.init_connections()
        self.init_filtro_combo()
        self.retranslate_ui()
        self.cargar_participantes()

    def _is_english(self):
        ctrl = self.main_controller or getattr(self.main_view, "main_controller", None)
        return bool(ctrl and getattr(ctrl, "current_language", "es") == "en")

    def _tr(self, es, en):
        return en if self._is_english() else es

    def _translate_position(self, position):
        pos = (position or "").strip()
        if not self._is_english():
            return pos
        mapping = {
            "Portero": "Goalkeeper",
            "Defensa": "Defender",
            "Centrocampista": "Midfielder",
            "Delantero": "Forward",
            "N/A": "N/A",
        }
        return mapping.get(pos, pos)

    def init_connections(self):
        if hasattr(self.main_view.ui, "pushButton_nuevo_participante"):
            self.main_view.ui.pushButton_nuevo_participante.clicked.connect(self.abrir_formulario_participante)

        if hasattr(self.main_view.ui, "comboBox"):
            self.main_view.ui.comboBox.currentIndexChanged.connect(self.cargar_participantes)

        if hasattr(self.main_view.ui, "tableWidget_2"):
            self.main_view.ui.tableWidget_2.doubleClicked.connect(self.editar_participante_desde_tabla)
            from PySide6.QtCore import Qt
            self.main_view.ui.tableWidget_2.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.main_view.ui.tableWidget_2.customContextMenuRequested.connect(self.mostrar_menu_participante)

    def init_filtro_combo(self):
        if not hasattr(self.main_view.ui, "comboBox"):
            return

        combo = self.main_view.ui.comboBox
        selected_key = combo.currentData() if combo.count() else "all"

        options = [
            ("all", "Todos", "All"),
            ("player", "Jugador", "Player"),
            ("referee", "Árbitro", "Referee"),
            ("separator", "--- Rankings ---", "--- Rankings ---"),
            ("top_scorers", "Máximos Goleadores", "Top Scorers"),
            ("most_cards", "Más Tarjetas", "Most Cards"),
        ]

        combo.blockSignals(True)
        combo.clear()
        for key, es_text, en_text in options:
            combo.addItem(self._tr(es_text, en_text), key)

        idx = combo.findData(selected_key)
        combo.setCurrentIndex(idx if idx >= 0 else 0)
        combo.blockSignals(False)

    def _set_headers(self):
        if not hasattr(self.main_view.ui, "tableWidget_2"):
            return

        tabla = self.main_view.ui.tableWidget_2
        headers = [
            self._tr("Nombre", "Name"),
            self._tr("Fecha Nacimiento", "Birth Date"),
            self._tr("Jugador", "Player"),
            self._tr("Curso", "Course"),
            self._tr("Árbitro", "Referee"),
            self._tr("Posición", "Position"),
            self._tr("Tarjetas Amarillas", "Yellow Cards"),
            self._tr("Tarjetas Rojas", "Red Cards"),
            self._tr("Goles", "Goals"),
        ]
        for col, text in enumerate(headers):
            item = tabla.horizontalHeaderItem(col)
            if item is None:
                item = QTableWidgetItem()
                tabla.setHorizontalHeaderItem(col, item)
            item.setText(text)

    def retranslate_ui(self):
        ui = self.main_view.ui
        if hasattr(ui, "label_2"):
            ui.label_2.setText(self._tr("(Todos/Jugador/Árbitro)", "(All/Player/Referee)"))
        if hasattr(ui, "label_filtrar"):
            ui.label_filtrar.setText(self._tr("Filtrar por:", "Filter by:"))
        if hasattr(ui, "label_buscar"):
            ui.label_buscar.setText(self._tr("Buscar:", "Search:"))
        if hasattr(ui, "pushButton_nuevo_participante"):
            ui.pushButton_nuevo_participante.setText(self._tr("Nuevo Participante", "New Participant"))
        self._set_headers()
        self.init_filtro_combo()
        self.cargar_participantes()

    def abrir_formulario_participante(self):
        self.ventana_nuevo = UniversalController(self.main_view, "PARTICIPANTE", self.cargar_participantes)

    def cargar_participantes(self):
        tabla = self.main_view.ui.tableWidget_2
        tabla.setRowCount(0)
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._set_headers()

        filtro_key = "all"
        if hasattr(self.main_view.ui, "comboBox") and self.main_view.ui.comboBox.count():
            filtro_key = self.main_view.ui.comboBox.currentData() or "all"

        if filtro_key == "separator":
            return

        sql = """
            SELECT p.id, p.nombre, p.fecha_nacimiento, p.tipo_participante,
                   p.curso, p.posicion,
                   p.tarjetas_amarillas, p.tarjetas_rojas, p.goles
            FROM participantes p
        """

        if filtro_key == "player":
            sql += " WHERE p.tipo_participante LIKE '%Jugador%' OR p.tipo_participante = 'Ambos'"
        elif filtro_key == "referee":
            sql += " WHERE p.tipo_participante LIKE '%Árbitro%' OR p.tipo_participante LIKE '%Arbitro%' OR p.tipo_participante = 'Ambos'"
        elif filtro_key == "top_scorers":
            sql += " ORDER BY p.goles DESC"
        elif filtro_key == "most_cards":
            sql += " ORDER BY (p.tarjetas_amarillas + p.tarjetas_rojas) DESC"

        query = QSqlQuery()
        if not query.exec(sql):
            print(f"Error en consulta de participantes: {query.lastError().text()}")
            return

        row = 0
        while query.next():
            tabla.insertRow(row)

            id_participante = query.value(0)
            nombre = query.value(1)
            fecha = query.value(2)
            tipo = str(query.value(3) or "")
            curso = query.value(4)
            posicion = self._translate_position(query.value(5) or "")
            amarillas = query.value(6)
            rojas = query.value(7)
            goles = query.value(8)

            es_jugador = "X" if ("Jugador" in tipo or "Ambos" in tipo) else ""
            es_arbitro = "X" if ("Árbitro" in tipo or "Arbitro" in tipo or "Ambos" in tipo) else ""

            tabla.setItem(row, 0, QTableWidgetItem(str(nombre)))
            tabla.setItem(row, 1, QTableWidgetItem(str(fecha)))
            tabla.setItem(row, 2, QTableWidgetItem(es_jugador))
            tabla.setItem(row, 3, QTableWidgetItem(str(curso)))
            tabla.setItem(row, 4, QTableWidgetItem(es_arbitro))
            tabla.setItem(row, 5, QTableWidgetItem(str(posicion)))
            tabla.setItem(row, 6, QTableWidgetItem(str(amarillas)))
            tabla.setItem(row, 7, QTableWidgetItem(str(rojas)))
            tabla.setItem(row, 8, QTableWidgetItem(str(goles)))

            tabla.item(row, 0).setData(1001, id_participante)
            row += 1

    def editar_participante_desde_tabla(self, index):
        tabla = self.main_view.ui.tableWidget_2
        fila = index.row()
        item = tabla.item(fila, 0)
        if not item:
            return
        id_participante = item.data(1001)
        if id_participante:
            self.editar_participante(id_participante)

    def editar_participante(self, id_participante):
        self.ventana_nuevo = UniversalController(
            self.main_view,
            "PARTICIPANTE",
            self.cargar_participantes,
            id_editar=id_participante,
        )

    def mostrar_menu_participante(self, position):
        tabla = self.main_view.ui.tableWidget_2
        item = tabla.itemAt(position)
        if not item:
            return

        fila = tabla.row(item)
        id_participante = tabla.item(fila, 0).data(1001)
        nombre_participante = tabla.item(fila, 0).text()

        menu = QMenu(self.main_view)
        action_editar = menu.addAction(self._tr("Editar", "Edit"))
        action_eliminar = menu.addAction(self._tr("Eliminar", "Delete"))

        action = menu.exec(tabla.mapToGlobal(position))
        if action == action_editar:
            self.editar_participante(id_participante)
        elif action == action_eliminar:
            self.eliminar_participante(id_participante, nombre_participante)

    def eliminar_participante(self, id_participante, nombre):
        respuesta = QMessageBox.question(
            self.main_view,
            self._tr("Confirmar eliminación", "Confirm deletion"),
            self._tr(
                f"¿Deseas eliminar al participante '{nombre}'?",
                f"Do you want to delete participant '{nombre}'?",
            ),
            QMessageBox.Yes | QMessageBox.No,
        )

        if respuesta != QMessageBox.Yes:
            return

        query = QSqlQuery()
        query.prepare("DELETE FROM participantes WHERE id = ?")
        query.addBindValue(id_participante)

        if query.exec():
            QMessageBox.information(
                self.main_view,
                self._tr("Éxito", "Success"),
                self._tr(
                    f"Participante '{nombre}' eliminado correctamente.",
                    f"Participant '{nombre}' deleted successfully.",
                ),
            )
            self.cargar_participantes()
        else:
            QMessageBox.critical(
                self.main_view,
                self._tr("Error", "Error"),
                self._tr(
                    f"No se pudo eliminar el participante: {query.lastError().text()}",
                    f"Could not delete participant: {query.lastError().text()}",
                ),
            )

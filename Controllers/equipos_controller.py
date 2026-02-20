from PySide6.QtSql import QSqlQuery, QSqlQueryModel
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView

from Controllers.universal_controller import UniversalController


class EquiposController:
    def __init__(self, main_window):
        self.main_view = main_window
        self.main_controller = None
        self.ventana_alta = None
        self.funcion_refresco_externa = None

        self.modelo_lista = QSqlQueryModel()
        self.main_view.ui.list_Teams.setModel(self.modelo_lista)

        self.init_connections()
        self.retranslate_ui()
        self.cargar_lista_equipos()

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

    def _set_headers(self):
        tabla = self.main_view.ui.tableWidget
        headers = [
            self._tr("Nombre", "Name"),
            self._tr("Posición", "Position"),
            self._tr("Curso", "Course"),
            self._tr("Color Camiseta", "Shirt Color"),
            self._tr("Escudo", "Crest"),
        ]
        for col, text in enumerate(headers):
            item = tabla.horizontalHeaderItem(col)
            if item is None:
                item = QTableWidgetItem()
                tabla.setHorizontalHeaderItem(col, item)
            item.setText(text)

    def retranslate_ui(self):
        ui = self.main_view.ui
        if hasattr(ui, "groupBox_detalles"):
            ui.groupBox_detalles.setTitle(self._tr("Detalles", "Details"))
        if hasattr(ui, "pushButton_anadir_equipo"):
            ui.pushButton_anadir_equipo.setText(self._tr("Añadir equipo", "Add Team"))
        if hasattr(ui, "pushButton_editar_equipo"):
            ui.pushButton_editar_equipo.setText(self._tr("Editar equipo", "Edit Team"))
        if hasattr(ui, "pushButton_eliminar_equipo"):
            ui.pushButton_eliminar_equipo.setText(self._tr("Eliminar equipo", "Delete Team"))
        self._set_headers()
        current = self.main_view.ui.list_Teams.currentIndex()
        if current.isValid():
            self.cargar_jugadores(current)

    def init_connections(self):
        if hasattr(self.main_view.ui, "pushButton_anadir_equipo"):
            self.main_view.ui.pushButton_anadir_equipo.clicked.connect(self.abrir_formulario_alta)

        if hasattr(self.main_view.ui, "pushButton_editar_equipo"):
            self.main_view.ui.pushButton_editar_equipo.clicked.connect(self.abrir_formulario_editar)

        if hasattr(self.main_view.ui, "pushButton_eliminar_equipo"):
            self.main_view.ui.pushButton_eliminar_equipo.clicked.connect(self.eliminar_equipo)

        self.main_view.ui.list_Teams.clicked.connect(self.cargar_jugadores)

    def abrir_formulario_alta(self):
        self.ventana_alta = UniversalController(self.main_view, "EQUIPO", self.cargar_lista_equipos)

    def abrir_formulario_editar(self):
        index = self.main_view.ui.list_Teams.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self.main_view,
                self._tr("Aviso", "Warning"),
                self._tr("Selecciona un equipo de la lista primero", "Select a team from the list first"),
            )
            return

        nombre_seleccionado = index.data()
        query = QSqlQuery()
        query.prepare("SELECT id, nombre, curso, color_camiseta, ruta_escudo FROM equipos WHERE nombre = ?")
        query.addBindValue(nombre_seleccionado)

        if query.exec() and query.next():
            datos = (query.value(0), query.value(1), query.value(2), query.value(3), query.value(4))
            self.ventana_alta = UniversalController(
                self.main_view, "EQUIPO", self.cargar_lista_equipos, datos_editar=datos
            )
        else:
            QMessageBox.critical(
                self.main_view,
                self._tr("Error", "Error"),
                self._tr("No se pudieron leer los datos", "Could not read team data"),
            )

    def eliminar_equipo(self):
        index = self.main_view.ui.list_Teams.currentIndex()
        if not index.isValid():
            QMessageBox.warning(
                self.main_view,
                self._tr("Aviso", "Warning"),
                self._tr("Por favor, selecciona un equipo para eliminar.", "Please select a team to delete."),
            )
            return

        nombre_equipo = index.data()
        confirmacion = QMessageBox.question(
            self.main_view,
            self._tr("Confirmar borrado", "Confirm deletion"),
            self._tr(
                f"¿Estás seguro de que quieres eliminar el equipo '{nombre_equipo}'?\nSe borrarán AUTOMÁTICAMENTE todos sus jugadores.",
                f"Are you sure you want to delete team '{nombre_equipo}'?\nAll its players will be deleted automatically.",
            ),
            QMessageBox.Yes | QMessageBox.No,
        )

        if confirmacion != QMessageBox.Yes:
            return

        query_id = QSqlQuery()
        query_id.prepare("SELECT id FROM equipos WHERE nombre = ?")
        query_id.addBindValue(nombre_equipo)
        if not (query_id.exec() and query_id.next()):
            QMessageBox.critical(
                self.main_view,
                self._tr("Error", "Error"),
                self._tr("No se encontró el ID del equipo.", "Team ID was not found."),
            )
            return

        id_equipo = query_id.value(0)

        query_borrar_jugadores = QSqlQuery()
        query_borrar_jugadores.prepare("DELETE FROM participantes WHERE id_equipo = ?")
        query_borrar_jugadores.addBindValue(id_equipo)
        query_borrar_jugadores.exec()

        query_borrar_equipo = QSqlQuery()
        query_borrar_equipo.prepare("DELETE FROM equipos WHERE id = ?")
        query_borrar_equipo.addBindValue(id_equipo)

        if query_borrar_equipo.exec():
            QMessageBox.information(
                self.main_view,
                self._tr("Éxito", "Success"),
                self._tr("Equipo eliminado.", "Team deleted."),
            )
            self.main_view.ui.tableWidget.setRowCount(0)
            self.cargar_lista_equipos()
            if self.funcion_refresco_externa:
                self.funcion_refresco_externa()
        else:
            QMessageBox.critical(
                self.main_view,
                self._tr("Error", "Error"),
                self._tr("Falló el borrado del equipo.", "Failed to delete the team."),
            )

    def cargar_lista_equipos(self):
        self._set_headers()
        self.modelo_lista.setQuery("SELECT nombre FROM equipos")
        if self.modelo_lista.rowCount() > 0:
            indice_primero = self.modelo_lista.index(0, 0)
            self.main_view.ui.list_Teams.setCurrentIndex(indice_primero)
            self.cargar_jugadores(indice_primero)
        else:
            self.main_view.ui.tableWidget.setRowCount(0)

    def cargar_jugadores(self, index):
        nombre_equipo = index.data()
        tabla = self.main_view.ui.tableWidget
        tabla.setRowCount(0)
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._set_headers()

        sql = """
            SELECT p.nombre, p.posicion, e.curso, e.color_camiseta, e.ruta_escudo
            FROM participantes p
            JOIN equipos e ON p.id_equipo = e.id
            WHERE e.nombre = ?
        """
        query = QSqlQuery()
        query.prepare(sql)
        query.addBindValue(nombre_equipo)

        if query.exec():
            fila = 0
            while query.next():
                tabla.insertRow(fila)
                tabla.setItem(fila, 0, QTableWidgetItem(str(query.value(0))))
                tabla.setItem(fila, 1, QTableWidgetItem(self._translate_position(str(query.value(1) or ""))))
                tabla.setItem(fila, 2, QTableWidgetItem(str(query.value(2))))
                tabla.setItem(fila, 3, QTableWidgetItem(str(query.value(3))))
                ruta_escudo = query.value(4)
                self.insertar_imagen_escudo(tabla, fila, 4, ruta_escudo)
                fila += 1
            if fila > 0:
                tabla.setRowHeight(0, 50)

        tabla.horizontalHeader().setStretchLastSection(False)
        tabla.resizeColumnsToContents()
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, header.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, header.ResizeMode.ResizeToContents)

    def insertar_imagen_escudo(self, tabla, fila, columna, ruta_imagen):
        from PySide6.QtCore import Qt
        from PySide6.QtGui import QPixmap
        from PySide6.QtWidgets import QLabel

        if not ruta_imagen:
            tabla.setItem(fila, columna, QTableWidgetItem(""))
            return

        try:
            pixmap = QPixmap(ruta_imagen)
            if pixmap.isNull():
                tabla.setItem(fila, columna, QTableWidgetItem(self._tr("Sin imagen", "No image")))
                return

            pixmap = pixmap.scaledToHeight(40, Qt.SmoothTransformation)
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            tabla.setCellWidget(fila, columna, label)
        except Exception as e:
            tabla.setItem(fila, columna, QTableWidgetItem(f"Error: {e}"))

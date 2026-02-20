from PySide6.QtSql import QSqlQuery
from PySide6.QtWidgets import QFileDialog, QMessageBox

from Views.form_universal import FormUniversalView


class UniversalController:
    def __init__(self, main_window, modo, callback_refresh=None, datos_editar=None, id_editar=None):
        self.main_window = main_window
        self.view = FormUniversalView()
        self.modo_actual = modo
        self.refrescar_lista = callback_refresh
        self.datos_editar = datos_editar
        self.id_editar = id_editar

        self.main_controller = getattr(main_window, "main_controller", None)
        self.current_language = getattr(self.main_controller, "current_language", "es")
        self.view.set_language(self.current_language)

        if self.modo_actual == "EQUIPO":
            self.view.modo_equipo()
            self.view.btn_imagen.clicked.connect(self.seleccionar_imagen)
            if self.datos_editar:
                self.rellenar_datos_equipo()
        else:
            self.view.modo_participante()
            self.cargar_equipos_en_combo()
            if self.id_editar:
                self.rellenar_datos_participante()

        self.view.btn_guardar.clicked.connect(self.gestionar_guardado)
        self.view.show()

    def _tr(self, es, en):
        return en if self.current_language == "en" else es

    def rellenar_datos_equipo(self):
        _, nombre, curso, color, ruta = self.datos_editar
        self.view.lbl_titulo.setText(self._tr("Editar Equipo", "Edit Team"))
        self.view.btn_guardar.setText(self._tr("Actualizar Datos", "Update Data"))

        self.view.txt_eq_nombre.setText(nombre)
        self.view.txt_eq_curso.setText(curso)
        self.view.txt_eq_camiseta.setText(color)
        self.view.lbl_ruta_imagen.setText(ruta)

        if ruta:
            self.view.btn_imagen.setText(f"{self._tr('Imagen actual', 'Current image')}: ...{ruta[-15:]}")

    def rellenar_datos_participante(self):
        query = QSqlQuery()
        query.prepare(
            """
            SELECT nombre, fecha_nacimiento, curso, tipo_participante, posicion,
                   tarjetas_amarillas, tarjetas_rojas, goles, id_equipo
            FROM participantes WHERE id = ?
            """
        )
        query.addBindValue(self.id_editar)

        if not (query.exec() and query.next()):
            return

        self.view.lbl_titulo.setText(self._tr("Editar Participante", "Edit Participant"))
        self.view.btn_guardar.setText(self._tr("Actualizar Participante", "Update Participant"))

        self.view.txt_part_nombre.setText(query.value(0) or "")

        fecha_str = query.value(1) or ""
        if fecha_str:
            from PySide6.QtCore import QDate

            fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
            self.view.date_nacimiento.setDate(fecha)

        self.view.txt_part_curso.setText(query.value(2) or "")

        tipo = query.value(3) or ""
        idx_tipo = self.view.combo_tipo.findData(tipo)
        if idx_tipo >= 0:
            self.view.combo_tipo.setCurrentIndex(idx_tipo)

        posicion = query.value(4) or ""
        idx_pos = self.view.combo_posicion.findData(posicion)
        if idx_pos >= 0:
            self.view.combo_posicion.setCurrentIndex(idx_pos)

        self.view.spin_amarillas.setValue(query.value(5) or 0)
        self.view.spin_rojas.setValue(query.value(6) or 0)
        self.view.spin_goles.setValue(query.value(7) or 0)

        id_equipo = query.value(8)
        idx_equipo = self.view.combo_equipo_asignado.findData(id_equipo)
        if idx_equipo >= 0:
            self.view.combo_equipo_asignado.setCurrentIndex(idx_equipo)

    def seleccionar_imagen(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self.view,
            self._tr("Seleccionar Escudo", "Select Crest"),
            "",
            self._tr("Imagenes (*.png *.jpg)", "Images (*.png *.jpg)"),
        )
        if not archivo:
            return
        self.view.lbl_ruta_imagen.setText(archivo)
        self.view.btn_imagen.setText(f"{self._tr('Imagen', 'Image')}: ...{archivo[-15:]}")
        self.view.btn_imagen.setStyleSheet("border: 2px solid green; color: green;")

    def cargar_equipos_en_combo(self):
        combo = self.view.combo_equipo_asignado
        combo.clear()
        query = QSqlQuery("SELECT id, nombre FROM equipos")
        while query.next():
            combo.addItem(query.value(1), query.value(0))

    def gestionar_guardado(self):
        if self.modo_actual == "EQUIPO":
            self.guardar_equipo()
        else:
            self.guardar_participante()

    def guardar_equipo(self):
        nombre = self.view.txt_eq_nombre.text()
        curso = self.view.txt_eq_curso.text()
        color = self.view.txt_eq_camiseta.text()
        ruta = self.view.lbl_ruta_imagen.text()

        if not nombre:
            QMessageBox.warning(self.view, "Error", self._tr("El nombre no puede estar vacío.", "Name cannot be empty."))
            return
        if any(char.isdigit() for char in nombre):
            QMessageBox.warning(
                self.view,
                "Error",
                self._tr("El nombre del equipo no puede contener números.", "Team name cannot contain numbers."),
            )
            return

        query = QSqlQuery()
        if self.datos_editar:
            id_equipo = self.datos_editar[0]
            query.prepare("UPDATE equipos SET nombre=?, curso=?, color_camiseta=?, ruta_escudo=? WHERE id=?")
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(ruta)
            query.addBindValue(id_equipo)
            mensaje = self._tr("Equipo actualizado correctamente", "Team updated successfully")
        else:
            query.prepare("INSERT INTO equipos (nombre, curso, color_camiseta, ruta_escudo) VALUES (?, ?, ?, ?)")
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(ruta)
            mensaje = self._tr("Equipo creado correctamente", "Team created successfully")

        if query.exec():
            QMessageBox.information(self.view, self._tr("Éxito", "Success"), mensaje)
            self.view.close()
            if self.refrescar_lista:
                self.refrescar_lista()
        else:
            QMessageBox.critical(self.view, "Error SQL", query.lastError().text())

    def guardar_participante(self):
        nombre = self.view.txt_part_nombre.text()
        fecha = self.view.date_nacimiento.date().toString("yyyy-MM-dd")
        curso = self.view.txt_part_curso.text()
        tipo = self.view.combo_tipo.currentData() or self.view.combo_tipo.currentText()
        posicion = self.view.combo_posicion.currentData() or self.view.combo_posicion.currentText()
        id_equipo = self.view.combo_equipo_asignado.currentData()
        amarillas = self.view.spin_amarillas.value()
        rojas = self.view.spin_rojas.value()
        goles = self.view.spin_goles.value()

        if not nombre:
            QMessageBox.warning(self.view, "Error", self._tr("El nombre no puede estar vacío.", "Name cannot be empty."))
            return
        if any(char.isdigit() for char in nombre):
            QMessageBox.warning(
                self.view,
                "Error",
                self._tr(
                    "El nombre del participante no puede contener números.",
                    "Participant name cannot contain numbers.",
                ),
            )
            return

        query = QSqlQuery()
        if self.id_editar:
            query.prepare(
                """
                UPDATE participantes
                SET nombre=?, fecha_nacimiento=?, curso=?, tipo_participante=?, posicion=?,
                    tarjetas_amarillas=?, tarjetas_rojas=?, goles=?, id_equipo=?
                WHERE id = ?
                """
            )
            query.addBindValue(nombre)
            query.addBindValue(fecha)
            query.addBindValue(curso)
            query.addBindValue(tipo)
            query.addBindValue(posicion)
            query.addBindValue(amarillas)
            query.addBindValue(rojas)
            query.addBindValue(goles)
            query.addBindValue(id_equipo)
            query.addBindValue(self.id_editar)
            mensaje = self._tr("Participante actualizado correctamente", "Participant updated successfully")
        else:
            query.prepare(
                """
                INSERT INTO participantes
                (nombre, fecha_nacimiento, curso, tipo_participante, posicion,
                 tarjetas_amarillas, tarjetas_rojas, goles, id_equipo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            )
            query.addBindValue(nombre)
            query.addBindValue(fecha)
            query.addBindValue(curso)
            query.addBindValue(tipo)
            query.addBindValue(posicion)
            query.addBindValue(amarillas)
            query.addBindValue(rojas)
            query.addBindValue(goles)
            query.addBindValue(id_equipo)
            mensaje = self._tr("Participante registrado correctamente", "Participant created successfully")

        if query.exec():
            QMessageBox.information(self.view, self._tr("Éxito", "Success"), mensaje)
            self.view.close()
            if self.refrescar_lista:
                self.refrescar_lista()
        else:
            QMessageBox.critical(self.view, "Error SQL", query.lastError().text())

from PySide6.QtWidgets import QMessageBox, QFileDialog
from PySide6.QtCore import QCoreApplication
from PySide6.QtSql import QSqlQuery
from Views.form_universal import FormUniversalView

class UniversalController:
    def __init__(self, main_window, modo, callback_refresh=None, datos_editar=None, id_editar=None):
        """
        datos_editar: Tupla con (ID, Nombre, Curso, Color, Ruta) si vamos a editar equipo.
        id_editar: ID del participante si vamos a editar participante.
        """
        self.view = FormUniversalView()
        self.modo_actual = modo
        self.refrescar_lista = callback_refresh
        self.datos_editar = datos_editar 
        self.id_editar = id_editar 
        
        # Configuración según modo
        if self.modo_actual == "EQUIPO":
            self.view.modo_equipo()
            self.view.btn_imagen.clicked.connect(self.seleccionar_imagen)
            
            if self.datos_editar:
                self.rellenar_datos_equipo()
        else:
            self.view.modo_participante()
            self.cargar_equipos_en_combo()
            
            # Editar participante
            if self.id_editar:
                self.rellenar_datos_participante()

        self.view.btn_guardar.clicked.connect(self.gestionar_guardado)
        self.view.show()

    def rellenar_datos_equipo(self):
        """ Rellena los campos con la info que le pasamos """
        _, nombre, curso, color, ruta = self.datos_editar
        
        self.view._title_key = "Editar Equipo"
        self.view._save_key = "Actualizar Datos"
        self.view.retranslate_ui()
        
        self.view.txt_eq_nombre.setText(nombre)
        self.view.txt_eq_curso.setText(curso)
        self.view.txt_eq_camiseta.setText(color)
        self.view.lbl_ruta_imagen.setText(ruta)
        
        if ruta:
             pref = QCoreApplication.translate("UniversalController", "Imagen actual")
             self.view.btn_imagen.setText(f"{pref}: ...{ruta[-15:]}")
    
    def rellenar_datos_participante(self):
        """Rellena los campos del formulario con los datos del participante a editar"""
        query = QSqlQuery()
        query.prepare("""
            SELECT nombre, fecha_nacimiento, curso, tipo_participante, posicion, 
                   tarjetas_amarillas, tarjetas_rojas, goles, id_equipo
            FROM participantes WHERE id = ?
        """)
        query.addBindValue(self.id_editar)
        
        if query.exec() and query.next():
            self.view._title_key = "Editar Participante"
            self.view._save_key = "Actualizar Participante"
            self.view.retranslate_ui()
            
            self.view.txt_part_nombre.setText(query.value(0) or "")
            
            # Fecha
            fecha_str = query.value(1) or ""
            if fecha_str:
                from PySide6.QtCore import QDate
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                self.view.date_nacimiento.setDate(fecha)
            
            self.view.txt_part_curso.setText(query.value(2) or "")
            
            # Combobox tipo
            tipo = query.value(3) or ""
            idx = self.view.combo_tipo.findData(tipo)
            if idx >= 0:
                self.view.combo_tipo.setCurrentIndex(idx)
            
            # Combobox posición
            posicion = query.value(4) or ""
            idx = self.view.combo_posicion.findData(posicion)
            if idx >= 0:
                self.view.combo_posicion.setCurrentIndex(idx)
            
            # Spins
            self.view.spin_amarillas.setValue(query.value(5) or 0)
            self.view.spin_rojas.setValue(query.value(6) or 0)
            self.view.spin_goles.setValue(query.value(7) or 0)
            
            # Equipo asignado
            id_equipo = query.value(8)
            idx = self.view.combo_equipo_asignado.findData(id_equipo)
            if idx >= 0:
                self.view.combo_equipo_asignado.setCurrentIndex(idx)

    def seleccionar_imagen(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self.view,
            QCoreApplication.translate("UniversalController", "Seleccionar Escudo"),
            "",
            QCoreApplication.translate("UniversalController", "Imágenes (*.png *.jpg)")
        )
        if archivo:
            self.view.lbl_ruta_imagen.setText(archivo)
            pref = QCoreApplication.translate("UniversalController", "Imagen")
            self.view.btn_imagen.setText(f"{pref}: ...{archivo[-15:]}")
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

        # --- VALIDACIONES ---
        if not nombre:
            QMessageBox.warning(
                self.view,
                QCoreApplication.translate("UniversalController", "Error"),
                QCoreApplication.translate("UniversalController", "El nombre no puede estar vacío.")
            )
            return

        # VALIDACIÓN NUEVA: NO NÚMEROS
        if any(char.isdigit() for char in nombre):
            QMessageBox.warning(
                self.view,
                QCoreApplication.translate("UniversalController", "Error"),
                QCoreApplication.translate("UniversalController", "El nombre del equipo no puede contener números.")
            )
            return

        query = QSqlQuery()
        
        if self.datos_editar:
            # UPDATE
            id_equipo = self.datos_editar[0]
            query.prepare("UPDATE equipos SET nombre=?, curso=?, color_camiseta=?, ruta_escudo=? WHERE id=?")
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(ruta)
            query.addBindValue(id_equipo)
            mensaje = QCoreApplication.translate("UniversalController", "Equipo actualizado correctamente")
        else:
            # INSERT
            query.prepare("INSERT INTO equipos (nombre, curso, color_camiseta, ruta_escudo) VALUES (?, ?, ?, ?)")
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(ruta)
            mensaje = QCoreApplication.translate("UniversalController", "Equipo creado correctamente")

        if query.exec():
            QMessageBox.information(
                self.view,
                QCoreApplication.translate("UniversalController", "Éxito"),
                mensaje
            )
            self.view.close()
            if self.refrescar_lista:
                self.refrescar_lista()
        else:
            QMessageBox.critical(
                self.view,
                QCoreApplication.translate("UniversalController", "Error SQL"),
                query.lastError().text()
            )

    def guardar_participante(self):
        # 1. Recogemos datos
        nombre = self.view.txt_part_nombre.text()
        fecha = self.view.date_nacimiento.date().toString("yyyy-MM-dd")
        curso = self.view.txt_part_curso.text()
        tipo = self.view.combo_tipo.currentData()
        posicion = self.view.combo_posicion.currentData()
        id_equipo = self.view.combo_equipo_asignado.currentData()
        
        amarillas = self.view.spin_amarillas.value()
        rojas = self.view.spin_rojas.value()
        goles = self.view.spin_goles.value()

        # --- VALIDACIONES ---
        if not nombre:
            QMessageBox.warning(
                self.view,
                QCoreApplication.translate("UniversalController", "Error"),
                QCoreApplication.translate("UniversalController", "El nombre no puede estar vacío.")
            )
            return

        # VALIDACIÓN NUEVA: NO NÚMEROS
        if any(char.isdigit() for char in nombre):
            QMessageBox.warning(
                self.view,
                QCoreApplication.translate("UniversalController", "Error"),
                QCoreApplication.translate("UniversalController", "El nombre del participante no puede contener números.")
            )
            return

        query = QSqlQuery()
        
        # 2. INSERT O UPDATE
        if self.id_editar:
            # UPDATE
            query.prepare("""
                UPDATE participantes 
                SET nombre=?, fecha_nacimiento=?, curso=?, tipo_participante=?, posicion=?, 
                    tarjetas_amarillas=?, tarjetas_rojas=?, goles=?, id_equipo=?
                WHERE id = ?
            """)
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
            mensaje = QCoreApplication.translate("UniversalController", "Participante actualizado correctamente")
        else:
            # INSERT
            query.prepare("""
                INSERT INTO participantes 
                (nombre, fecha_nacimiento, curso, tipo_participante, posicion, 
                 tarjetas_amarillas, tarjetas_rojas, goles, id_equipo) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """)
            query.addBindValue(nombre)
            query.addBindValue(fecha)
            query.addBindValue(curso)
            query.addBindValue(tipo)
            query.addBindValue(posicion)
            query.addBindValue(amarillas)
            query.addBindValue(rojas)
            query.addBindValue(goles)
            query.addBindValue(id_equipo)
            mensaje = QCoreApplication.translate("UniversalController", "Participante registrado correctamente")

        if query.exec():
            QMessageBox.information(
                self.view,
                QCoreApplication.translate("UniversalController", "Éxito"),
                mensaje
            )
            self.view.close()
            if self.refrescar_lista:
                self.refrescar_lista()
        else:
            QMessageBox.critical(
                self.view,
                QCoreApplication.translate("UniversalController", "Error SQL"),
                query.lastError().text()
            )

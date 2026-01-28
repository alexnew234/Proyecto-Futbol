from PySide6.QtWidgets import QMessageBox, QFileDialog
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
        self.datos_editar = datos_editar # Guardamos los datos si existen
        self.id_editar = id_editar # ID para editar participante
        
        # Configuración según modo
        if self.modo_actual == "EQUIPO":
            self.view.modo_equipo()
            self.view.btn_imagen.clicked.connect(self.seleccionar_imagen)
            
            # --- DETECCIÓN DE MODO EDICIÓN ---
            if self.datos_editar:
                self.rellenar_datos_equipo() # Función nueva para rellenar
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
        # Desempaquetamos los datos: (id, nombre, curso, color, ruta)
        _, nombre, curso, color, ruta = self.datos_editar
        
        self.view.lbl_titulo.setText("Editar Equipo")
        self.view.btn_guardar.setText("Actualizar Datos")
        
        self.view.txt_eq_nombre.setText(nombre)
        self.view.txt_eq_curso.setText(curso)
        self.view.txt_eq_camiseta.setText(color)
        self.view.lbl_ruta_imagen.setText(ruta)
        
        if ruta:
             self.view.btn_imagen.setText(f"Imagen actual: ...{ruta[-15:]}")
    
    def rellenar_datos_participante(self):
        """Rellena los campos del formulario con los datos del participante a editar"""
        query = QSqlQuery()
        query.prepare("""
            SELECT nombre, fecha_nacimiento, curso, tipo_participante, posicion, 
                   t_amarillas, t_rojas, goles, id_equipo
            FROM participantes WHERE id = ?
        """)
        query.addBindValue(self.id_editar)
        
        if query.exec() and query.next():
            self.view.lbl_titulo.setText("Editar Participante")
            self.view.btn_guardar.setText("Actualizar Participante")
            
            self.view.txt_part_nombre.setText(query.value(0) or "")
            # Convertir fecha de texto a QDate
            fecha_str = query.value(1) or ""
            if fecha_str:
                from PySide6.QtCore import QDate
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                self.view.date_nacimiento.setDate(fecha)
            self.view.txt_part_curso.setText(query.value(2) or "")
            
            # Combobox tipo
            tipo = query.value(3) or ""
            idx = self.view.combo_tipo.findText(tipo)
            if idx >= 0:
                self.view.combo_tipo.setCurrentIndex(idx)
            
            # Combobox posición
            posicion = query.value(4) or ""
            idx = self.view.combo_posicion.findText(posicion)
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
        archivo, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar Escudo", "", "Imagenes (*.png *.jpg)")
        if archivo:
            self.view.lbl_ruta_imagen.setText(archivo)
            self.view.btn_imagen.setText(f"Imagen: ...{archivo[-15:]}")
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
            QMessageBox.warning(self.view, "Error", "Falta el nombre")
            return

        query = QSqlQuery()
        
        # --- DECISIÓN: ¿INSERTAR O ACTUALIZAR? ---
        if self.datos_editar:
            # MODO EDICIÓN (UPDATE)
            id_equipo = self.datos_editar[0] # El ID es el primer dato
            query.prepare("UPDATE equipos SET nombre=?, curso=?, color_camiseta=?, ruta_escudo=? WHERE id=?")
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(ruta)
            query.addBindValue(id_equipo)
            mensaje = "Equipo actualizado correctamente"
        else:
            # MODO NUEVO (INSERT)
            query.prepare("INSERT INTO equipos (nombre, curso, color_camiseta, ruta_escudo) VALUES (?, ?, ?, ?)")
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(ruta)
            mensaje = "Equipo creado correctamente"

        if query.exec():
            QMessageBox.information(self.view, "Éxito", mensaje)
            self.view.close()
            if self.refrescar_lista:
                self.refrescar_lista()
        else:
            QMessageBox.critical(self.view, "Error SQL", query.lastError().text())

    def guardar_participante(self):
        # 1. Recogemos TODOS los datos del formulario
        nombre = self.view.txt_part_nombre.text()
        fecha = self.view.date_nacimiento.text()
        curso = self.view.txt_part_curso.text()
        tipo = self.view.combo_tipo.currentText()
        posicion = self.view.combo_posicion.currentText()
        id_equipo = self.view.combo_equipo_asignado.currentData()
        
        # Estadísticas
        amarillas = self.view.spin_amarillas.value()
        rojas = self.view.spin_rojas.value()
        goles = self.view.spin_goles.value()

        if not nombre:
            QMessageBox.warning(self.view, "Error", "Falta el nombre")
            return

        query = QSqlQuery()
        
        # 2. INSERT O UPDATE
        if self.id_editar:
            # MODO EDICIÓN (UPDATE)
            query.prepare("""
                UPDATE participantes 
                SET nombre=?, fecha_nacimiento=?, curso=?, tipo_participante=?, posicion=?, 
                    t_amarillas=?, t_rojas=?, goles=?, id_equipo=?
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
            mensaje = "Participante actualizado correctamente"
        else:
            # MODO NUEVO (INSERT)
            query.prepare("""
                INSERT INTO participantes 
                (nombre, fecha_nacimiento, curso, tipo_participante, posicion, 
                 t_amarillas, t_rojas, goles, id_equipo) 
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
            mensaje = "Participante registrado correctamente"

        if query.exec():
            QMessageBox.information(self.view, "Éxito", mensaje)
            self.view.close()
            if self.refrescar_lista:
                self.refrescar_lista()
        else:
            QMessageBox.critical(self.view, "Error SQL", query.lastError().text())
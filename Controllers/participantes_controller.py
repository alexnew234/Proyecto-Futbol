from PySide6.QtWidgets import QTableWidgetItem, QMessageBox, QAbstractItemView
from PySide6.QtSql import QSqlQuery
from Controllers.universal_controller import UniversalController

class ParticipantesController:
    def __init__(self, main_window):
        self.main_view = main_window
        self.ventana_nuevo = None

        # --- MODIFICACIÓN: OCULTAR EL BOTÓN "GENERAR RONDAS" ---
        # Probamos los nombres más probables para asegurar que se oculte
        if hasattr(self.main_view.ui, 'btn_generar_rondas'):
            self.main_view.ui.btn_generar_rondas.hide()
        
        if hasattr(self.main_view.ui, 'pushButton_generar_rondas'):
            self.main_view.ui.pushButton_generar_rondas.hide()
            
        if hasattr(self.main_view.ui, 'btn_generar_ronda'):
            self.main_view.ui.btn_generar_ronda.hide()
        # -------------------------------------------------------

        # 1. Inicializamos conexiones de botones
        self.init_connections()
        
        # 2. Rellenamos el desplegable
        self.init_filtro_combo()
        
        # 3. Cargamos la lista de gente
        self.cargar_participantes()

    def init_connections(self):
        # Botón Nuevo Participante
        if hasattr(self.main_view.ui, 'pushButton_nuevo_participante'):
            self.main_view.ui.pushButton_nuevo_participante.clicked.connect(self.abrir_formulario_participante)
            
        # Cambio en el combo
        if hasattr(self.main_view.ui, 'comboBox'):
            self.main_view.ui.comboBox.currentIndexChanged.connect(self.cargar_participantes)
        
        # Doble clic para editar
        if hasattr(self.main_view.ui, 'tableWidget_2'):
            self.main_view.ui.tableWidget_2.doubleClicked.connect(self.editar_participante_desde_tabla)
        
        # Click derecho para menú contextual
        if hasattr(self.main_view.ui, 'tableWidget_2'):
            from PySide6.QtCore import Qt
            self.main_view.ui.tableWidget_2.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            self.main_view.ui.tableWidget_2.customContextMenuRequested.connect(self.mostrar_menu_participante)

    def init_filtro_combo(self):
        """ Rellena el desplegable de arriba con las opciones """
        if hasattr(self.main_view.ui, 'comboBox'):
            combo = self.main_view.ui.comboBox
            combo.clear()
            # Añadimos opciones normales y DE RANKING
            combo.addItems([
                "Todos", 
                "Jugador", 
                "Árbitro", 
                "--- Rankings ---",
                "Máximos Goleadores", 
                "Más Tarjetas"
            ])

    def abrir_formulario_participante(self):
        self.ventana_nuevo = UniversalController(
            self.main_view, 
            "PARTICIPANTE", 
            self.cargar_participantes 
        )

    def cargar_participantes(self):
        tabla = self.main_view.ui.tableWidget_2
        tabla.setRowCount(0)
        
        # Desactivar edición de doble clic
        from PySide6.QtWidgets import QAbstractItemView
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        filtro_tipo = "Todos"
        if hasattr(self.main_view.ui, 'comboBox'):
            filtro_tipo = self.main_view.ui.comboBox.currentText()

        # SQL BASE
        sql = """
            SELECT p.id, p.nombre, p.fecha_nacimiento, p.tipo_participante, 
                   p.curso, p.posicion, 
                   p.tarjetas_amarillas, p.tarjetas_rojas, p.goles
            FROM participantes p
        """
        
        # Modificar SQL según el filtro seleccionado
        if filtro_tipo == "Jugador":
            sql += " WHERE p.tipo_participante LIKE '%Jugador%' OR p.tipo_participante = 'Ambos'"
        elif filtro_tipo == "Árbitro":
            sql += " WHERE p.tipo_participante LIKE '%Árbitro%' OR p.tipo_participante = 'Ambos'"
        elif filtro_tipo == "Máximos Goleadores":
            sql += " ORDER BY p.goles DESC"
        elif filtro_tipo == "Más Tarjetas":
            # Ordenar por suma de tarjetas (Amarillas + Rojas)
            sql += " ORDER BY (p.tarjetas_amarillas + p.tarjetas_rojas) DESC"
        elif filtro_tipo == "--- Rankings ---":
            return # No hacer nada si selecciona el separador
            
        query = QSqlQuery()
        if query.exec(sql):
            fila = 0
            while query.next():
                tabla.insertRow(fila)
                
                id_participante = query.value(0)
                nombre = query.value(1)
                fecha = query.value(2)
                tipo = str(query.value(3))
                curso = query.value(4)
                posicion = query.value(5)
                amarillas = query.value(6)
                rojas = query.value(7)
                goles = query.value(8)

                # Lógica X
                es_jugador = "X" if "Jugador" in tipo or "Ambos" in tipo else ""
                es_arbitro = "X" if "Árbitro" in tipo or "Ambos" in tipo else ""
                
                tabla.setItem(fila, 0, QTableWidgetItem(str(nombre)))
                tabla.setItem(fila, 1, QTableWidgetItem(str(fecha)))
                tabla.setItem(fila, 2, QTableWidgetItem(es_jugador))
                tabla.setItem(fila, 3, QTableWidgetItem(str(curso)))
                tabla.setItem(fila, 4, QTableWidgetItem(es_arbitro))
                tabla.setItem(fila, 5, QTableWidgetItem(str(posicion)))
                
                # Estadísticas REALES
                tabla.setItem(fila, 6, QTableWidgetItem(str(amarillas)))
                tabla.setItem(fila, 7, QTableWidgetItem(str(rojas)))
                tabla.setItem(fila, 8, QTableWidgetItem(str(goles)))
                
                # Almacenar el ID en el primer item para poder acceder después
                tabla.item(fila, 0).setData(1001, id_participante)
                
                fila += 1
        else:
            print(f"Error en consulta de participantes: {query.lastError().text()}")
    
    def editar_participante_desde_tabla(self, index):
        """Editar participante al hacer doble clic en la tabla"""
        tabla = self.main_view.ui.tableWidget_2
        fila = index.row()
        item = tabla.item(fila, 0)
        id_participante = item.data(1001)
        
        if id_participante:
            self.editar_participante(id_participante)
    
    def editar_participante(self, id_participante):
        """Abre el formulario para editar un participante"""
        self.ventana_nuevo = UniversalController(
            self.main_view, 
            "PARTICIPANTE", 
            self.cargar_participantes,
            id_editar=id_participante
        )
    
    def mostrar_menu_participante(self, position):
        """Muestra un menú contextual con opciones editar/eliminar"""
        from PySide6.QtWidgets import QMenu
        
        tabla = self.main_view.ui.tableWidget_2
        item = tabla.itemAt(position)
        
        if not item:
            return
        
        fila = tabla.row(item)
        id_participante = tabla.item(fila, 0).data(1001)
        nombre_participante = tabla.item(fila, 0).text()
        
        menu = QMenu(self.main_view)
        
        action_editar = menu.addAction("Editar")
        action_eliminar = menu.addAction("Eliminar")
        
        action = menu.exec(tabla.mapToGlobal(position))
        
        if action == action_editar:
            self.editar_participante(id_participante)
        elif action == action_eliminar:
            self.eliminar_participante(id_participante, nombre_participante)
    
    def eliminar_participante(self, id_participante, nombre):
        """Elimina un participante de la base de datos"""
        respuesta = QMessageBox.question(
            self.main_view,
            "Confirmar eliminación",
            f"¿Deseas eliminar al participante '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM participantes WHERE id = ?")
            query.addBindValue(id_participante)
            
            if query.exec():
                QMessageBox.information(
                    self.main_view,
                    "Éxito",
                    f"Participante '{nombre}' eliminado correctamente."
                )
                self.cargar_participantes()
            else:
                QMessageBox.critical(
                    self.main_view,
                    "Error",
                    f"No se pudo eliminar el participante: {query.lastError().text()}"
                )
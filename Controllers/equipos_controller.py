from PySide6.QtWidgets import QTableWidgetItem, QMessageBox
from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from Controllers.universal_controller import UniversalController 

class EquiposController:
    def __init__(self, main_window):
        self.main_view = main_window
        self.ventana_alta = None 
        
        # --- NUEVO: Una variable para guardar el número de teléfono del vecino ---
        self.funcion_refresco_externa = None 
        
        self.modelo_lista = QSqlQueryModel()
        self.main_view.ui.list_Teams.setModel(self.modelo_lista)

        self.init_connections()
        self.cargar_lista_equipos()

    def init_connections(self):
        # Botón AÑADIR
        if hasattr(self.main_view.ui, 'pushButton_anadir_equipo'):
            self.main_view.ui.pushButton_anadir_equipo.clicked.connect(self.abrir_formulario_alta)
            
        # Botón EDITAR
        if hasattr(self.main_view.ui, 'pushButton_editar_equipo'):
             self.main_view.ui.pushButton_editar_equipo.clicked.connect(self.abrir_formulario_editar)
             
        # Botón ELIMINAR
        if hasattr(self.main_view.ui, 'pushButton_eliminar_equipo'):
             self.main_view.ui.pushButton_eliminar_equipo.clicked.connect(self.eliminar_equipo)
            
        # Clic en la lista
        self.main_view.ui.list_Teams.clicked.connect(self.cargar_jugadores)
        
    def abrir_formulario_alta(self):
        self.ventana_alta = UniversalController(
            self.main_view, "EQUIPO", self.cargar_lista_equipos
        )

    def abrir_formulario_editar(self):
        index = self.main_view.ui.list_Teams.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.main_view, "Aviso", "Selecciona un equipo de la lista primero")
            return
            
        nombre_seleccionado = index.data()

        query = QSqlQuery()
        query.prepare("SELECT id, nombre, curso, color_camiseta, ruta_escudo FROM equipos WHERE nombre = ?")
        query.addBindValue(nombre_seleccionado)
        
        if query.exec() and query.next():
            datos = (
                query.value(0), query.value(1), query.value(2), query.value(3), query.value(4)
            )
            self.ventana_alta = UniversalController(
                self.main_view, "EQUIPO", self.cargar_lista_equipos, datos_editar=datos
            )
        else:
            QMessageBox.critical(self.main_view, "Error", "No se pudieron leer los datos")

    def eliminar_equipo(self):
        index = self.main_view.ui.list_Teams.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self.main_view, "Aviso", "Por favor, selecciona un equipo para eliminar.")
            return

        nombre_equipo = index.data()

        confirmacion = QMessageBox.question(
            self.main_view, 
            "Confirmar borrado", 
            f"¿Estás seguro de que quieres eliminar el equipo '{nombre_equipo}'?\nSe borrarán AUTOMÁTICAMENTE todos sus jugadores.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            # 1. Obtener ID
            query_id = QSqlQuery()
            query_id.prepare("SELECT id FROM equipos WHERE nombre = ?")
            query_id.addBindValue(nombre_equipo)
            
            if query_id.exec() and query_id.next():
                id_equipo = query_id.value(0) 

                # 2. Borrar Jugadores
                query_borrar_jugadores = QSqlQuery()
                query_borrar_jugadores.prepare("DELETE FROM participantes WHERE id_equipo = ?")
                query_borrar_jugadores.addBindValue(id_equipo)
                query_borrar_jugadores.exec()
                
                # 3. Borrar Equipo
                query_borrar_equipo = QSqlQuery()
                query_borrar_equipo.prepare("DELETE FROM equipos WHERE id = ?")
                query_borrar_equipo.addBindValue(id_equipo)
                
                if query_borrar_equipo.exec():
                    QMessageBox.information(self.main_view, "Éxito", "Equipo eliminado.")
                    self.main_view.ui.tableWidget.setRowCount(0)
                    self.cargar_lista_equipos()
                    
                    # --- AQUÍ ESTÁ LA MAGIA ---
                    # Si tenemos el teléfono del vecino, le llamamos para que actualice SU lista
                    if self.funcion_refresco_externa:
                        print("Avisando al controlador de participantes...")
                        self.funcion_refresco_externa() 
                        
                else:
                    QMessageBox.critical(self.main_view, "Error", "Falló el borrado del equipo.")
            else:
                 QMessageBox.critical(self.main_view, "Error", "No se encontró el ID del equipo.")

    def cargar_lista_equipos(self):
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
        
        # Desactivar edición de doble clic
        from PySide6.QtWidgets import QAbstractItemView
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Cargar jugadores con todos los detalles incluyendo color y escudo del equipo
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
                tabla.setItem(fila, 0, QTableWidgetItem(str(query.value(0))))  # Nombre
                tabla.setItem(fila, 1, QTableWidgetItem(str(query.value(1))))  # Posición
                tabla.setItem(fila, 2, QTableWidgetItem(str(query.value(2))))  # Curso
                tabla.setItem(fila, 3, QTableWidgetItem(str(query.value(3))))  # Color Camiseta
                
                # Para el escudo, mostrar imagen en lugar de ruta
                ruta_escudo = query.value(4)
                self.insertar_imagen_escudo(tabla, fila, 4, ruta_escudo)
                fila += 1
            
            # Ajustar altura de las filas para las imágenes
            tabla.setRowHeight(0, 50)
        
        # Ajuste responsivo de las columnas
        tabla.horizontalHeader().setStretchLastSection(False)
        tabla.resizeColumnsToContents()
        
        # Hacer que las columnas se expandan para llenar el espacio disponible
        header = tabla.horizontalHeader()
        header.setSectionResizeMode(0, header.ResizeMode.Stretch)  # Nombre - flexible
        header.setSectionResizeMode(1, header.ResizeMode.ResizeToContents)  # Posición
        header.setSectionResizeMode(2, header.ResizeMode.ResizeToContents)  # Curso
        header.setSectionResizeMode(3, header.ResizeMode.ResizeToContents)  # Color
        header.setSectionResizeMode(4, header.ResizeMode.ResizeToContents)  # Escudo
    
    def insertar_imagen_escudo(self, tabla, fila, columna, ruta_imagen):
        """Inserta una imagen en la celda especificada de la tabla"""
        from PySide6.QtWidgets import QLabel
        from PySide6.QtGui import QPixmap
        from PySide6.QtCore import Qt
        
        if not ruta_imagen:
            tabla.setItem(fila, columna, QTableWidgetItem(""))
            return
        
        try:
            # Crear pixmap desde la ruta
            pixmap = QPixmap(ruta_imagen)
            
            if pixmap.isNull():
                tabla.setItem(fila, columna, QTableWidgetItem("Sin imagen"))
                return
            
            # Escalar la imagen a un tamaño apropiado
            pixmap = pixmap.scaledToHeight(40, Qt.SmoothTransformation)
            
            # Crear label con la imagen
            label = QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)
            
            # Insertar el label en la celda
            tabla.setCellWidget(fila, columna, label)
        except Exception as e:
            tabla.setItem(fila, columna, QTableWidgetItem(f"Error: {str(e)}"))
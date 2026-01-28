from PySide6.QtWidgets import (
    QMessageBox, QTreeWidgetItem, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy,
    QSpinBox
)
from PySide6.QtSql import QSqlQuery
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from PySide6.QtWidgets import QHeaderView
from Controllers.tournaments_controller import TournamentsController


class CustomSpinBox(QSpinBox):
    """SpinBox personalizado con botones + y - claramente visibles"""
    def __init__(self):
        super().__init__()
        # Estilo base del spinbox
        self.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: white;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px 5px 5px 5px;
                font-size: 18px;
                font-weight: bold;
                min-height: 40px;
            }
        """)
        # Ocultar los botones por defecto
        self.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        
    def wheelEvent(self, event):
        """Permitir cambios con rueda del ratón"""
        if event.angleDelta().y() > 0:
            self.stepUp()
        else:
            self.stepDown()


def crear_spinbox_con_botones(label_text, valor_inicial=0):
    """Crea un spinbox con botones + y - visibles junto a él"""
    from PySide6.QtWidgets import QHBoxLayout, QWidget
    
    # Contenedor
    contenedor = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(5)
    
    # Spinbox sin botones
    spinbox = CustomSpinBox()
    spinbox.setValue(valor_inicial)
    spinbox.setMinimum(0)
    
    # Botón menos
    btn_menos = QPushButton("-")
    btn_menos.setFixedWidth(40)
    btn_menos.setFixedHeight(40)
    btn_menos.setStyleSheet("""
        QPushButton {
            background-color: #B71C1C;
            color: white;
            border: 1px solid #8B0000;
            border-radius: 3px;
            font-size: 24px;
            font-weight: bold;
            padding: 0px;
        }
        QPushButton:hover {
            background-color: #D32F2F;
        }
        QPushButton:pressed {
            background-color: #8B0000;
        }
    """)
    btn_menos.clicked.connect(spinbox.stepDown)
    
    # Botón más
    btn_mas = QPushButton("+")
    btn_mas.setFixedWidth(40)
    btn_mas.setFixedHeight(40)
    btn_mas.setStyleSheet("""
        QPushButton {
            background-color: #B71C1C;
            color: white;
            border: 1px solid #8B0000;
            border-radius: 3px;
            font-size: 24px;
            font-weight: bold;
            padding: 0px;
        }
        QPushButton:hover {
            background-color: #D32F2F;
        }
        QPushButton:pressed {
            background-color: #8B0000;
        }
    """)
    btn_mas.clicked.connect(spinbox.stepUp)
    
    # Armar el layout
    layout.addWidget(btn_menos)
    layout.addWidget(spinbox, 1)
    layout.addWidget(btn_mas)
    
    contenedor.setLayout(layout)
    contenedor.spinbox = spinbox  # Guardar referencia al spinbox
    
    return contenedor


class CalendarioController:
    """Controlador para la página de calendario y torneos"""
    
    def __init__(self, main_window, main_controller=None):
        self.main_view = main_window
        self.main_controller = main_controller
        self.tournaments_ctrl = TournamentsController(main_window)
        
        # Obtener la página de calendario
        self.page_calendario = self.main_view.ui.page_calendario
        self.tree_widget = self.main_view.ui.treeWidget_partidos
        
        # Configurar el árbol para mostrar texto completo y usar todo el espacio
        self.tree_widget.setColumnCount(1)
        self.tree_widget.header().setStretchLastSection(True)
        
        # Agregar botones a la página de calendario
        self.setup_ui()
        self.init_connections()
        self.cargar_calendario()
    
    def setup_ui(self):
        """Agrega los botones a la página de calendario"""
        # Obtener el layout principal
        layout_main = self.page_calendario.layout()
        
        # Crear layout horizontal para botones
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(10)
        
        # Botón Generar Siguiente Ronda
        self.btn_generar_ronda = QPushButton("Generar Siguiente Ronda")
        self.btn_generar_ronda.setStyleSheet("""
            QPushButton {
                background-color: #2d7d2d;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3da83d;
            }
        """)
        self.btn_generar_ronda.setCursor(Qt.PointingHandCursor)
        
        # Botón Ver Clasificación
        self.btn_clasificacion = QPushButton("Ver Clasificación")
        self.btn_clasificacion.setStyleSheet("""
            QPushButton {
                background-color: #1a5d7d;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a7d9d;
            }
        """)
        self.btn_clasificacion.setCursor(Qt.PointingHandCursor)
        
        # Botón Nueva Temporada
        self.btn_nueva_temporada = QPushButton("Nueva Temporada")
        self.btn_nueva_temporada.setStyleSheet("""
            QPushButton {
                background-color: #7d2d2d;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a83d3d;
            }
        """)
        self.btn_nueva_temporada.setCursor(Qt.PointingHandCursor)
        
        layout_botones.addWidget(self.btn_generar_ronda)
        layout_botones.addWidget(self.btn_clasificacion)
        layout_botones.addWidget(self.btn_nueva_temporada)
        layout_botones.addStretch()
        
        # Insertar botones después del label_titulo
        layout_main.insertLayout(1, layout_botones)
        
        # Label para ronda actual
        self.lbl_ronda_actual = QLabel("Ronda actual: Ninguna generada")
        self.lbl_ronda_actual.setStyleSheet("color: #888; font-style: italic;")
        layout_main.insertWidget(2, self.lbl_ronda_actual)
        
        # Configurar el árbol para que use el espacio disponible
        try:
            self.tree_widget.header().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        except:
            pass  # En caso de que la versión de PySide6 no soporte este método
        
        # Tabla de clasificación (inicialmente oculta)
        self.tabla_clasificacion = QTableWidget()
        self.tabla_clasificacion.setVisible(False)
        self.tabla_clasificacion.setStyleSheet("""
            QTableWidget {
                background-color: #252526;
                color: #ddd;
                border: 1px solid #3e3e42;
                gridline-color: #3e3e42;
            }
            QHeaderView::section {
                background-color: #333333;
                color: white;
                padding: 5px;
                border: 1px solid #3e3e42;
            }
        """)
        layout_main.addWidget(self.tabla_clasificacion)
        
        # Botón volver al calendario
        self.btn_volver = QPushButton("Volver al Calendario")
        self.btn_volver.setVisible(False)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #555;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        self.btn_volver.setCursor(Qt.PointingHandCursor)
        layout_main.addWidget(self.btn_volver)
    
    def init_connections(self):
        """Conectar botones y eventos"""
        self.btn_generar_ronda.clicked.connect(self.generar_siguiente_ronda)
        self.btn_clasificacion.clicked.connect(self.mostrar_clasificacion)
        self.btn_nueva_temporada.clicked.connect(self.nueva_temporada)
        self.btn_volver.clicked.connect(self.volver_calendario)
        
        # Permitir hacer clic en partidos para editar goles
        self.tree_widget.itemDoubleClicked.connect(self.editar_partido)
    
    def cargar_calendario(self):
        """Carga y muestra los partidos organizados por rondas"""
        self.tree_widget.clear()
        
        # Desactivar edición de doble clic en el árbol de partidos
        from PySide6.QtWidgets import QAbstractItemView
        self.tree_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Obtener rondas disponibles
        query = QSqlQuery()
        query.exec("""
            SELECT DISTINCT ronda FROM partidos WHERE ronda IS NOT NULL
            ORDER BY CASE ronda
                WHEN 'Octavos' THEN 1
                WHEN 'Cuartos' THEN 2
                WHEN 'Semifinal' THEN 3
                WHEN 'Final' THEN 4
                ELSE 5
            END
        """)
        
        rondas = []
        while query.next():
            rondas.append(query.value(0))
        
        # Actualizar label de ronda actual
        ronda_actual = self.tournaments_ctrl.obtener_ronda_actual()
        if ronda_actual:
            self.lbl_ronda_actual.setText(f"Ronda actual: {ronda_actual}")
        else:
            self.lbl_ronda_actual.setText("Ronda actual: Ninguna generada")
        
        # Si no hay rondas, mostrar mensaje
        if not rondas:
            tree_item = QTreeWidgetItem(["No hay partidos programados"])
            self.tree_widget.addTopLevelItem(tree_item)
            return
        
        # Agregar rondas al árbol
        for ronda in rondas:
            ronda_item = QTreeWidgetItem([ronda])
            ronda_item.setBackground(0, self.crear_color_ronda(ronda))
            
            # Obtener partidos de esta ronda
            partidos_query = QSqlQuery()
            partidos_query.prepare("""
                SELECT id, fecha, hora, id_equipo_local, id_equipo_visitante, 
                       goles_local, goles_visitante, jugado
                FROM partidos
                WHERE ronda = ?
                ORDER BY fecha, hora
            """)
            partidos_query.addBindValue(ronda)
            
            if partidos_query.exec():
                while partidos_query.next():
                    id_partido = partidos_query.value(0)
                    fecha = partidos_query.value(1)
                    hora = partidos_query.value(2)
                    id_local = partidos_query.value(3)
                    id_visitante = partidos_query.value(4)
                    goles_local = partidos_query.value(5)
                    goles_visitante = partidos_query.value(6)
                    jugado = partidos_query.value(7)
                    
                    # Obtener nombres de equipos
                    nombre_local = self.obtener_nombre_equipo(id_local)
                    nombre_visitante = self.obtener_nombre_equipo(id_visitante)
                    
                    # Crear texto del partido
                    if jugado:
                        partido_texto = f"{nombre_local} {goles_local} - {goles_visitante} {nombre_visitante} ({fecha} {hora}) ✓"
                    else:
                        partido_texto = f"{nombre_local} vs {nombre_visitante} ({fecha} {hora})"
                    
                    partido_item = QTreeWidgetItem([partido_texto])
                    ronda_item.addChild(partido_item)
            
            self.tree_widget.addTopLevelItem(ronda_item)
    
    def obtener_nombre_equipo(self, id_equipo):
        """Obtiene el nombre de un equipo por su ID"""
        query = QSqlQuery()
        query.prepare("SELECT nombre FROM equipos WHERE id = ?")
        query.addBindValue(id_equipo)
        
        if query.exec() and query.next():
            return query.value(0)
        return "Desconocido"
    
    def crear_color_ronda(self, ronda):
        """Crea un color diferente para cada ronda"""
        colores = {
            "Octavos": QColor(100, 120, 180),
            "Cuartos": QColor(100, 150, 200),
            "Semifinal": QColor(150, 180, 220),
            "Final": QColor(200, 50, 50)
        }
        return colores.get(ronda, QColor(80, 80, 80))
    
    def generar_siguiente_ronda(self):
        """Genera la siguiente ronda del torneo"""
        if self.tournaments_ctrl.generar_siguiente_ronda():
            self.cargar_calendario()
    
    def mostrar_clasificacion(self):
        """Navega a la página de clasificación"""
        # Cambiar a la página de clasificación (índice 2)
        self.main_view.ui.stackedWidget.setCurrentIndex(2)
    
    def volver_calendario(self):
        """Vuelve a la vista del calendario"""
        self.tree_widget.setVisible(True)
        self.tabla_clasificacion.setVisible(False)
        self.btn_volver.setVisible(False)
    
    def nueva_temporada(self):
        """Inicia una nueva temporada borrando todos los partidos"""
        from PySide6.QtWidgets import QMessageBox
        
        # Confirmar con el usuario
        respuesta = QMessageBox.question(
            self.main_view,
            "Nueva Temporada",
            "¿Estás seguro de que quieres iniciar una nueva temporada?\n\n"
            "Se borrarán TODOS los partidos y rondas.\n"
            "Los equipos y participantes se mantendrán.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta != QMessageBox.Yes:
            return
        
        # Borrar todos los partidos
        query = QSqlQuery()
        if query.exec("DELETE FROM partidos"):
            QMessageBox.information(
                self.main_view,
                "Éxito",
                "Nueva temporada iniciada.\nTodos los partidos han sido eliminados."
            )
            self.cargar_calendario()
        else:
            QMessageBox.critical(
                self.main_view,
                "Error",
                f"Error al borrar los partidos: {query.lastError().text()}"
            )
    
    def editar_partido(self, item, column):
        """Permite editar los goles de un partido haciendo doble clic"""
        # Solo editar si es un partido (no una ronda)
        if item.parent() is None:
            return
        
        # Obtener el texto del partido
        partido_texto = item.text(0)
        
        # Extraer información del partido
        ronda_item = item.parent()
        ronda = ronda_item.text(0)
        
        # Buscar el ID del partido por el texto
        query = QSqlQuery()
        query.prepare("""
            SELECT id, id_equipo_local, id_equipo_visitante, goles_local, goles_visitante
            FROM partidos
            WHERE ronda = ?
        """)
        query.addBindValue(ronda)
        
        id_partido = None
        if query.exec():
            while query.next():
                id_local = query.value(1)
                id_visitante = query.value(2)
                nombre_local = self.obtener_nombre_equipo(id_local)
                nombre_visitante = self.obtener_nombre_equipo(id_visitante)
                
                # Verificar si este es el partido
                if nombre_local in partido_texto and nombre_visitante in partido_texto:
                    id_partido = query.value(0)
                    goles_local_actual = query.value(3)
                    goles_visitante_actual = query.value(4)
                    break
        
        if id_partido is None:
            return
        
        # Crear diálogo para editar goles
        from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
        
        dialog = QDialog(self.main_view)
        dialog.setWindowTitle("Editar Resultado del Partido")
        dialog.setGeometry(100, 100, 380, 250)
        
        layout = QVBoxLayout()
        
        # Campo goles local
        layout.addWidget(QLabel(f"{nombre_local}:"))
        widget_local = crear_spinbox_con_botones("", goles_local_actual if goles_local_actual else 0)
        spin_local = widget_local.spinbox
        layout.addWidget(widget_local)
        
        # Campo goles visitante
        layout.addWidget(QLabel(f"{nombre_visitante}:"))
        widget_visitante = crear_spinbox_con_botones("", goles_visitante_actual if goles_visitante_actual else 0)
        spin_visitante = widget_visitante.spinbox
        layout.addWidget(widget_visitante)
        
        # Botones
        btn_guardar = QPushButton("Guardar")
        btn_cancelar = QPushButton("Cancelar")
        
        layout.addWidget(btn_guardar)
        layout.addWidget(btn_cancelar)
        
        def guardar_goles():
            # Actualizar goles en la base de datos
            update_query = QSqlQuery()
            update_query.prepare("""
                UPDATE partidos
                SET goles_local = ?, goles_visitante = ?, jugado = 1
                WHERE id = ?
            """)
            update_query.addBindValue(spin_local.value())
            update_query.addBindValue(spin_visitante.value())
            update_query.addBindValue(id_partido)
            
            if update_query.exec():
                QMessageBox.information(self.main_view, "Éxito", "Resultado actualizado")
                self.cargar_calendario()
                
                # También actualizar la clasificación si está visible
                if self.main_controller:
                    self.main_controller.actualizar_clasificacion()
                
                dialog.close()
            else:
                QMessageBox.critical(self.main_view, "Error", "No se pudo actualizar el resultado")
        
        btn_guardar.clicked.connect(guardar_goles)
        btn_cancelar.clicked.connect(dialog.close)
        
        dialog.setLayout(layout)
        dialog.exec()

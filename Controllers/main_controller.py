from PySide6.QtWidgets import QMessageBox
from Controllers.equipos_controller import EquiposController
from Controllers.participantes_controller import ParticipantesController
from Controllers.calendario_controller import CalendarioController

class MainController:
    def __init__(self, main_window):
        self.view = main_window
        
        # 1. Nacen los controladores
        self.equipos_ctrl = EquiposController(main_window)
        self.participantes_ctrl = ParticipantesController(main_window)
        
        # Crear controlador de calendario (pasando self para que tenga acceso a actualizar_clasificacion)
        self.calendario_ctrl = CalendarioController(main_window, self)
        
        # Conexión directa (teléfono) entre equipos y participantes
        self.equipos_ctrl.funcion_refresco_externa = self.participantes_ctrl.cargar_participantes

        # 2. Conexiones
        self.init_toolbar_connections()
        if hasattr(self.view, 'dashboard'):
            self.init_dashboard_connections()

    def init_dashboard_connections(self):
        """ Botones del Menú Principal (Dashboard) """
        self.view.dashboard.btn_equipos.clicked.connect(lambda: self.cambiar_pagina(3))
        self.view.dashboard.btn_participantes.clicked.connect(lambda: self.cambiar_pagina(4))
        self.view.dashboard.btn_partidos.clicked.connect(lambda: self.cambiar_pagina(1))
        self.view.dashboard.btn_resultados.clicked.connect(lambda: self.cambiar_pagina(2))

    def init_toolbar_connections(self):
        """ 
        Conectamos los NUEVOS botones de texto que pusimos arriba 
        """
        # Botón Equipos (Texto arriba)
        self.view.act_equipos_texto.triggered.connect(lambda: self.cambiar_pagina(3))
            
        # Botón Participantes (Texto arriba)
        self.view.act_participantes_texto.triggered.connect(lambda: self.cambiar_pagina(4))

        # Botón Partidos (Texto arriba)
        self.view.act_partidos_texto.triggered.connect(lambda: self.cambiar_pagina(1))

        # Botón Salir (Texto arriba)
        self.view.act_salir_texto.triggered.connect(lambda: self.cambiar_pagina(0))

        # (Opcional) Mantenemos los antiguos de 'Créditos' y 'Ayuda' si existen en el diseño original
        if hasattr(self.view.ui, 'actionSalir'):
             self.view.ui.actionSalir.triggered.connect(lambda: self.cambiar_pagina(0))

    def cambiar_pagina(self, indice):
        self.view.ui.stackedWidget.setCurrentIndex(indice)
        
        # Recarga automática al cambiar de pestaña
        if indice == 1:
            self.calendario_ctrl.cargar_calendario()
        if indice == 2:
            # Actualizar clasificación cuando se va a esa página
            self.actualizar_clasificacion()
        if indice == 3:
            self.equipos_ctrl.cargar_lista_equipos()
        if indice == 4:
            self.participantes_ctrl.cargar_participantes()
    
    def actualizar_clasificacion(self):
        """Actualiza la tabla de clasificación de la página"""
        from PySide6.QtWidgets import QTableWidget, QTableWidgetItem
        
        print("DEBUG: actualizar_clasificacion() LLAMADO")
        
        # Obtener la página de clasificación
        page_clasificacion = self.view.ui.page_clasificacion
        
        # Buscar el scrollArea existente
        scroll_area = self.view.ui.scrollArea_bracket
        print(f"DEBUG: scrollArea_bracket encontrado: {scroll_area is not None}")
        
        # Buscar tabla existente en el scroll area
        tabla = None
        if scroll_area:
            widget = scroll_area.widget()
            if isinstance(widget, QTableWidget):
                tabla = widget
                print(f"DEBUG: Tabla existente encontrada")
        
        # Si no existe tabla, crearla
        if tabla is None:
            print("DEBUG: Creando tabla nueva")
            tabla = QTableWidget()
            tabla.setStyleSheet("""
                QTableWidget {
                    background-color: #252526;
                    color: #ddd;
                    border: none;
                    gridline-color: #3e3e42;
                    font-size: 13px;
                }
                QTableWidget::item {
                    padding: 8px;
                    border: none;
                }
                QHeaderView::section {
                    background-color: #333333;
                    color: white;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                    border-bottom: 1px solid #B71C1C;
                }
            """)
            tabla.horizontalHeader().setStretchLastSection(True)
            
            # Desactivar edición en la tabla
            from PySide6.QtWidgets import QAbstractItemView
            tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
            # Agregar tabla al scroll area
            if scroll_area:
                scroll_area.setWidget(tabla)
        
        # Limpiar la tabla antes de llenarla
        tabla.setRowCount(0)
        tabla.setColumnCount(0)
        
        print("DEBUG: Llamando a mostrar_clasificacion()")
        # Actualizar la tabla con la clasificación actual
        self.calendario_ctrl.tournaments_ctrl.mostrar_clasificacion(tabla)
        print("DEBUG: mostrar_clasificacion() completado")
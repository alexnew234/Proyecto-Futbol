import csv
import sys
import os 
from PySide6.QtWidgets import (
    QMessageBox, QPushButton, QFileDialog, QTableWidget, 
    QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel
)
from PySide6.QtGui import QAction, QColor, QBrush, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery

from Controllers.equipos_controller import EquiposController
from Controllers.participantes_controller import ParticipantesController
from Controllers.calendario_controller import CalendarioController
<<<<<<< Updated upstream
=======
from Controllers.reports_controller import ReportsController
# IMPORTACIÃ“N DEL COMPONENTE RELOJ
from Views.reloj_widget import RelojDigital, ModoReloj
# IMPORTACIÃ“N DE LA NUEVA VISTA DE CONFIGURACIÃ“N
from Views.reloj_config_view import RelojConfigView

>>>>>>> Stashed changes

class MainController:
    def __init__(self, main_window):
        self.view = main_window
        
        # 1. Controladores
        self.equipos_ctrl = EquiposController(main_window)
        self.participantes_ctrl = ParticipantesController(main_window)
        # Pasamos self para que el calendario pueda llamar a actualizar_clasificacion
        self.calendario_ctrl = CalendarioController(main_window, self) 
        self.reports_ctrl = ReportsController(main_window)
        self.equipos_ctrl.funcion_refresco_externa = self.participantes_ctrl.cargar_participantes

<<<<<<< Updated upstream
=======
        # --- AÃ‘ADIR PESTAÃ‘A DE CONFIGURACIÃ“N RELOJ AL STACK ---
        self.reloj_config_view = RelojConfigView()
        self.ui.stackedWidget.addWidget(self.reloj_config_view)
        self.index_reloj_config = self.ui.stackedWidget.count() - 1
        
        # --- AÃ‘ADIR BOTONES DE IDIOMA EN LA PESTAÃ‘A DE CONFIGURACIÃ“N ---
        # Lo hacemos aquí por código para no tener que editar el archivo de la Vista
        try:
            layout_config = self.reloj_config_view.layout()
            if not layout_config:
                layout_config = QVBoxLayout(self.reloj_config_view)
                self.reloj_config_view.setLayout(layout_config)
            
            # Crear contenedor para los botones
            self.lbl_idioma = QLabel("")
            self.lbl_idioma.setStyleSheet("color: white; font-weight: bold; margin-top: 10px;")
            
            layout_idiomas = QHBoxLayout()
            self.btn_es = QPushButton("")
            self.btn_en = QPushButton("")
            
            estilo_btn = "padding: 8px; font-weight: bold; border-radius: 4px; background-color: #444; color: white;"
            self.btn_es.setStyleSheet(estilo_btn)
            self.btn_en.setStyleSheet(estilo_btn)
            
            layout_idiomas.addWidget(self.btn_es)
            layout_idiomas.addWidget(self.btn_en)
            
            layout_config.addWidget(self.lbl_idioma)
            layout_config.addLayout(layout_idiomas)
            
            # Conectar señales
            self.btn_es.clicked.connect(lambda: self.cambiar_idioma("es"))
            self.btn_en.clicked.connect(lambda: self.cambiar_idioma("en"))
            
        except Exception as e:
            print(f"Error al inyectar botones de idioma: {e}")
        # ----------------------------------------------------

>>>>>>> Stashed changes
        # 2. Conexiones
        self.init_toolbar_connections()
        if hasattr(self.view, 'dashboard'):
            self.init_dashboard_connections()

        # Conectar el botón de Exportar CSV
        if hasattr(self.view, 'btn_exportar_csv'):
            self.view.btn_exportar_csv.clicked.connect(self.exportar_csv)

        # 3. Configuración visual
        self.arreglar_botones_rebeldes()
        self.setup_dashboard_logo() 
<<<<<<< Updated upstream
=======
        
        # 4. CONFIGURACIÃ“N DEL RELOJ EN EL DASHBOARD
        self.setup_reloj_dashboard()
        
        # 5. AÃ‘ADIR BOTÃ“N A LA BARRA SUPERIOR (MÃ‰TODO CLÃSICO - SIN ROMPER NADA)
        self.setup_toolbar_extra_button()
        
        # 6. ASEGURAR RESPONSIVIDAD Y COLOR ROJO SÃ“LIDO
        self.ensure_toolbar_responsive()

        # 7. Asegurar textos traducibles iniciales
        self.retraducir_ui()

    # =========================================================================
    #  MÃ‰TODOS DE INTERNACIONALIZACIÃ“N (TRADUCCIÃ“N)
    # =========================================================================
    def cambiar_idioma(self, codigo_idioma):
        """Carga el archivo .qm y actualiza toda la interfaz"""
        if codigo_idioma == "es":
            self.app.removeTranslator(self.translator)
        else:
            archivo = f"app_{codigo_idioma}.qm"
            ruta = os.path.join(self.translation_path, archivo)
            if self.translator.load(ruta):
                self.app.installTranslator(self.translator)
                print(f"Idioma cambiado a: {codigo_idioma}")
            else:
                print(f"No se encontró traducción: {ruta}")
        
        self.retraducir_ui()

    def retraducir_ui(self):
        """Refresca los textos visibles"""
        # 1. Refrescar UI cargada de Designer
        self.ui.retranslateUi(self.view)

        # 1.1 Textos creados en MainWindow
        if hasattr(self.view, 'retranslate_ui'):
            self.view.retranslate_ui()
        if hasattr(self.view, 'dashboard') and hasattr(self.view.dashboard, 'retranslate_ui'):
            self.view.dashboard.retranslate_ui()
        if hasattr(self, 'reloj_config_view') and hasattr(self.reloj_config_view, 'retranslate_ui'):
            self.reloj_config_view.retranslate_ui()
        if hasattr(self, 'calendario_ctrl') and hasattr(self.calendario_ctrl, 'retranslate_ui'):
            self.calendario_ctrl.retranslate_ui()
        if hasattr(self, 'participantes_ctrl') and hasattr(self.participantes_ctrl, 'retranslate_ui'):
            self.participantes_ctrl.retranslate_ui()
        
        # 2. Refrescar textos creados por código
        if hasattr(self, 'act_config_reloj'):
            self.act_config_reloj.setText(QCoreApplication.translate("MainController", "Config. Reloj"))
        if hasattr(self, 'lbl_idioma'):
            self.lbl_idioma.setText(QCoreApplication.translate("MainController", "Idioma / Language:"))
        if hasattr(self, 'btn_es'):
            self.btn_es.setText(QCoreApplication.translate("MainController", "Espanol"))
        if hasattr(self, 'btn_en'):
            self.btn_en.setText(QCoreApplication.translate("MainController", "English"))
            
        # 3. Refrescar tabla de clasificación si está visible
        if self.ui.stackedWidget.currentIndex() == 2:
            self.actualizar_clasificacion()

    # =========================================================================

    def ensure_toolbar_responsive(self):
        """
        Configura las barras de herramientas para que se adapten al ancho de la ventana.
        Si no caben los botones, aparecerá un menú desplegable (>>).
        """
        # Buscar todas las toolbars de la ventana
        toolbars = self.view.findChildren(QToolBar)
        
        if not toolbars:
            return

        # Aplicar configuración a todas las barras encontradas
        for toolbar in toolbars:
            # Fijar la barra (evita que se pueda arrastrar fuera) ayuda al layout a calcular mejor el espacio
            toolbar.setMovable(False)
            toolbar.setFloatable(False)
            
            # Configurar la política de tamaño para que intente expandirse horizontalmente
            sizePolicy = toolbar.sizePolicy()
            sizePolicy.setHorizontalPolicy(QSizePolicy.Expanding)
            toolbar.setSizePolicy(sizePolicy)
            
            # --- MODIFICACIÃ“N VISUAL: FLECHA CON FONDO ROJO ---
            toolbar.setStyleSheet("""
                QToolBar {
                    border: none;
                    spacing: 5px;
                }
                /* Flecha de extensión (>>) cuando no caben los botones */
                QToolBar::extension {
                    background-color: #B71C1C; /* ROJO RFEF SÃ“LIDO */
                    color: white;              /* Icono Blanco */
                    border: 1px solid white;   /* Borde fino blanco */
                    border-radius: 4px;
                    padding: 5px;              /* Tamaño generoso */
                    margin: 2px;
                    width: 20px;               /* Ancho forzado */
                }
                QToolBar::extension:hover {
                    background-color: #ff3333; /* Rojo más claro al pasar ratón */
                }
            """)
            # -------------------------------------------------------
            
            # Forzar recalculo de geometría
            toolbar.updateGeometry()

    def setup_toolbar_extra_button(self):
        """ 
        Busca dónde están los botones 'Salir' o 'Ayuda' e inserta 
        el de Configuración en el mismo contenedor.
        """
        
        # 1. Crear la Acción (TRADUCIBLE)
        texto_boton = QCoreApplication.translate("MainController", "Config. Reloj")
        self.act_config_reloj = QAction(texto_boton, self.view)
        self.act_config_reloj.triggered.connect(lambda: self.cambiar_pagina(self.index_reloj_config))
        
        # 2. Identificar acciones que SABEMOS que están en esa barra
        known_actions = []
        if hasattr(self.view, 'act_salir_texto'): known_actions.append(self.view.act_salir_texto)
        if hasattr(self.view, 'act_ayuda'): known_actions.append(self.view.act_ayuda)
        if hasattr(self.view, 'act_creditos'): known_actions.append(self.view.act_creditos)
        
        target_container = None
        reference_action = None
        
        # 3. ESCANEAR TOOLBARS (Barras de Herramientas)
        all_toolbars = self.view.findChildren(QToolBar)
        for toolbar in all_toolbars:
            toolbar_actions = toolbar.actions()
            for ka in known_actions:
                if ka in toolbar_actions:
                    target_container = toolbar
                    reference_action = ka
                    break
            if target_container: break
            
        # 4. ESCANEAR MENUBAR (Barra de Menú)
        if not target_container:
            menubar = self.view.menuBar()
            if menubar:
                menubar_actions = menubar.actions()
                for ka in known_actions:
                    if ka in menubar_actions:
                        target_container = menubar
                        reference_action = ka
                        break
        
        # 5. INSERTAR EL BOTÃ“N
        if target_container:
            if reference_action:
                target_container.insertAction(reference_action, self.act_config_reloj)
            else:
                target_container.addAction(self.act_config_reloj)
        else:
            print("[AVISO] No se encontró la barra original. Creando barra auxiliar.")
            tb = QToolBar(QCoreApplication.translate("MainController", "Configuracion"))
            self.view.addToolBar(Qt.TopToolBarArea, tb)
            tb.addAction(self.act_config_reloj)
>>>>>>> Stashed changes

    def setup_dashboard_logo(self):
        """Inserta la imagen de la RFEF en el Dashboard (Compatible con .exe y normal)"""
        try:
            # Obtenemos la página del dashboard (índice 0 del StackedWidget)
            page_dashboard = self.view.ui.stackedWidget.widget(0)
            
            # Verificamos si tiene layout
            if not page_dashboard.layout():
                return

            # Creamos el Label para la imagen
            lbl_imagen = QLabel()
            lbl_imagen.setAlignment(Qt.AlignCenter)
            
            # --- MODIFICACIÓN NECESARIA PARA EL .EXE ---
            # Determinamos la ruta base dependiendo de si es .exe o script normal
            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.getcwd()
            
            # Construimos la ruta: Carpeta base + Resources + img + logo_rfef.jpg
            ruta_img = os.path.join(base_path, "Resources", "img", "logo_rfef.jpg")
            # -------------------------------------------
            
            if os.path.exists(ruta_img):
                pixmap = QPixmap(ruta_img)
                # Escalamos la imagen para que no sea gigante (ej: 250px de alto), manteniendo proporción
                pixmap = pixmap.scaledToHeight(250, Qt.SmoothTransformation)
                lbl_imagen.setPixmap(pixmap)
                
                # Insertamos en el layout (Posición 1: Debajo del Título, Encima de los botones)
                page_dashboard.layout().insertWidget(1, lbl_imagen)
            else:
                print(f"[AVISO] No se encontró la imagen en: {ruta_img}")
                
        except Exception as e:
            print(f"No se pudo cargar el logo del dashboard: {e}")

    def exportar_csv(self):
        """ Exportar datos a CSV """
        scroll_area = self.view.ui.scrollArea_bracket
        tabla = None
        if scroll_area:
            tabla = scroll_area.widget()
        
        if not isinstance(tabla, QTableWidget) or tabla.rowCount() == 0:
            QMessageBox.warning(self.view, "Error", "No hay datos para exportar.")
            return

<<<<<<< Updated upstream
        archivo, _ = QFileDialog.getSaveFileName(self.view, "Guardar Clasificación", "clasificacion.csv", "Archivos CSV (*.csv)")
=======
        archivo, _ = QFileDialog.getSaveFileName(
            self.view,
            QCoreApplication.translate("MainController", "Guardar Clasificacion"),
            "clasificacion.csv",
            QCoreApplication.translate("MainController", "Archivos CSV (*.csv)")
        )
>>>>>>> Stashed changes
        
        if not archivo:
            return 

        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                headers = []
                for col in range(tabla.columnCount()):
                    item = tabla.horizontalHeaderItem(col)
                    headers.append(item.text() if item else f"Col {col}")
                writer.writerow(headers)
                
                for row in range(tabla.rowCount()):
                    row_data = []
                    for col in range(tabla.columnCount()):
                        item = tabla.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
<<<<<<< Updated upstream
            QMessageBox.information(self.view, "Éxito", "Datos exportados correctamente.")
=======
            QMessageBox.information(
                self.view,
                QCoreApplication.translate("MainController", "Exito"),
                QCoreApplication.translate("MainController", "Datos exportados correctamente.")
            )
>>>>>>> Stashed changes
        except Exception as e:
            QMessageBox.critical(self.view, "Error", f"Error al guardar: {e}")

    def mostrar_creditos(self):
<<<<<<< Updated upstream
        """ Muestra la pantalla de créditos con Autor, Versión y Fecha """
        titulo = "Acerca de - Gestor de Torneos"
        texto = """
        <h3>⚽ Gestor de Torneos de Fútbol</h3>
        <p>Aplicación para la gestión integral de competiciones deportivas.</p>
=======
        titulo = QCoreApplication.translate("MainController", "Acerca de - Gestor de Torneos")
        texto = QCoreApplication.translate("MainController", """
        <h3>Gestor de Torneos de Futbol</h3>
        <p>Aplicacion para la gestion integral de competiciones deportivas.</p>
>>>>>>> Stashed changes
        <hr>
        <p><b>Autor:</b> Alex</p>
        <p><b>Fecha de Actualizacion:</b> 29 de Enero de 2026</p>
        <p><b>Version:</b> 1.0.0 (Release Final)</p>
        <hr>
        <p><i>Desarrollado con Python 3.13, PySide6 y SQLite.</i></p>
        """
        QMessageBox.about(self.view, titulo, texto)

    def mostrar_ayuda(self):
<<<<<<< Updated upstream
        """ Muestra una guía rápida de uso """
        titulo = "Ayuda - Guía Rápida"
        texto = """
        <h3>📖 Cómo utilizar el Gestor</h3>
=======
        titulo = QCoreApplication.translate("MainController", "Ayuda - Guia Rapida")
        texto = QCoreApplication.translate("MainController", """
        <h3>Como utilizar el Gestor</h3>
>>>>>>> Stashed changes
        <ol>
            <li><b>Crear Equipos:</b> Ve a la pestana 'Equipos' y registra los clubes participantes.</li>
            <li><b>Generar Torneo:</b> En la pestana 'Partidos', pulsa el boton verde <b>'Generar Siguiente Ronda'</b>.</li>
            <li><b>Registrar Resultados:</b> Haz <b>doble clic</b> sobre un partido del calendario para editar el marcador, la fecha y asignar goles a jugadores.</li>
            <li><b>Eliminar Errores:</b> Haz <b>clic derecho</b> sobre un partido si necesitas borrarlo.</li>
            <li><b>Ver Clasificacion:</b> Consulta la tabla actualizada automaticamente en la seccion 'Clasificacion'.</li>
        </ol>
        <p><i>Nota: Es necesario completar todos los partidos de una ronda para poder generar la siguiente.</i></p>
        """
        QMessageBox.about(self.view, titulo, texto)

    def arreglar_botones_rebeldes(self):
        page_cal = self.view.ui.page_calendario
        if page_cal:
            for btn in page_cal.findChildren(QPushButton):
                if "clasificaci" in btn.text().lower() or "tabla" in btn.text().lower():
                    try: btn.clicked.disconnect() 
                    except: pass
                    btn.clicked.connect(lambda: self.cambiar_pagina(2))

    def init_dashboard_connections(self):
        self.view.dashboard.btn_equipos.clicked.connect(lambda: self.cambiar_pagina(3))
        self.view.dashboard.btn_participantes.clicked.connect(lambda: self.cambiar_pagina(4))
        self.view.dashboard.btn_partidos.clicked.connect(lambda: self.cambiar_pagina(1))
        self.view.dashboard.btn_resultados.clicked.connect(lambda: self.cambiar_pagina(2))

    def init_toolbar_connections(self):
        # Botones existentes
        if hasattr(self.view, 'act_equipos_texto'):
            self.view.act_equipos_texto.triggered.connect(lambda: self.cambiar_pagina(3))
        if hasattr(self.view, 'act_participantes_texto'):
            self.view.act_participantes_texto.triggered.connect(lambda: self.cambiar_pagina(4))
        if hasattr(self.view, 'act_partidos_texto'):
            self.view.act_partidos_texto.triggered.connect(lambda: self.cambiar_pagina(1))
        if hasattr(self.view, 'act_salir_texto'):
            self.view.act_salir_texto.triggered.connect(lambda: self.cambiar_pagina(0))
            
        # Conexión Clasificación
        if hasattr(self.view, 'act_clasificacion_texto'):
            self.view.act_clasificacion_texto.triggered.connect(lambda: self.cambiar_pagina(2))
        if hasattr(self.view, 'act_informes_texto'):
            self.view.act_informes_texto.triggered.connect(self.reports_ctrl.show)

        # Ayuda y Créditos
        if hasattr(self.view, 'act_creditos'):
            self.view.act_creditos.triggered.connect(self.mostrar_creditos)
        if hasattr(self.view, 'act_ayuda'):
            self.view.act_ayuda.triggered.connect(self.mostrar_ayuda)

    def cambiar_pagina(self, indice):
        self.view.ui.stackedWidget.setCurrentIndex(indice)
        if indice == 1:
            self.calendario_ctrl.cargar_calendario()
            self.arreglar_botones_rebeldes()
        if indice == 2:
            self.actualizar_clasificacion()
        if indice == 3:
            self.equipos_ctrl.cargar_lista_equipos()
        if indice == 4:
            self.participantes_ctrl.cargar_participantes()
    
    def actualizar_clasificacion(self):
        """Calcula y muestra la clasificación REAL desde la BD"""
        # Buscar la tabla en el scroll area
        scroll_area = self.view.ui.scrollArea_bracket
        tabla = None
        if scroll_area:
            tabla = scroll_area.widget()
        
        # Si no existe o no es tabla, crear una nueva
        if not isinstance(tabla, QTableWidget):
            tabla = QTableWidget()
            tabla.setStyleSheet("background-color: #252526; color: #ddd; border: none;")
            tabla.horizontalHeader().setStretchLastSection(True)
            tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            tabla.verticalHeader().setVisible(False)
            if scroll_area:
                scroll_area.setWidget(tabla)
        
        # Configurar columnas
        columnas = ["Pos", "Equipo", "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts"]
        tabla.setColumnCount(len(columnas))
        tabla.setHorizontalHeaderLabels(columnas)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents) # Pos pequeña
        tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents) # Nombre ajuste
        
        # 1. Obtener Equipos
        equipos_stats = {} # {id: {'nombre': 'X', 'pj': 0, ...}}
        q_eq = QSqlQuery("SELECT id, nombre FROM equipos")
        while q_eq.next():
            eid = q_eq.value(0)
            equipos_stats[eid] = {
                'nombre': q_eq.value(1),
                'pj': 0, 'g': 0, 'e': 0, 'p': 0, 
                'gf': 0, 'gc': 0, 'dg': 0, 'pts': 0
            }
            
        # 2. Calcular Puntos de Partidos Jugados
        q_part = QSqlQuery("SELECT equipo_local_id, equipo_visitante_id, goles_local, goles_visitante FROM partidos WHERE jugado = 1")
        while q_part.next():
            l_id = q_part.value(0)
            v_id = q_part.value(1)
            gl = q_part.value(2)
            gv = q_part.value(3)
            
            if l_id in equipos_stats and v_id in equipos_stats:
                # Local
                equipos_stats[l_id]['pj'] += 1
                equipos_stats[l_id]['gf'] += gl
                equipos_stats[l_id]['gc'] += gv
                # Visitante
                equipos_stats[v_id]['pj'] += 1
                equipos_stats[v_id]['gf'] += gv
                equipos_stats[v_id]['gc'] += gl
                
                if gl > gv: # Gana Local
                    equipos_stats[l_id]['g'] += 1
                    equipos_stats[l_id]['pts'] += 3
                    equipos_stats[v_id]['p'] += 1
                elif gv > gl: # Gana Visitante
                    equipos_stats[v_id]['g'] += 1
                    equipos_stats[v_id]['pts'] += 3
                    equipos_stats[l_id]['p'] += 1
                else: # Empate
                    equipos_stats[l_id]['e'] += 1
                    equipos_stats[l_id]['pts'] += 1
                    equipos_stats[v_id]['e'] += 1
                    equipos_stats[v_id]['pts'] += 1

        # 3. Calcular DG y Ordenar
        lista_final = []
        for eid, s in equipos_stats.items():
            s['dg'] = s['gf'] - s['gc']
            lista_final.append(s)
            
        # Ordenar por Puntos (desc), luego DG (desc), luego GF (desc)
        lista_final.sort(key=lambda x: (x['pts'], x['dg'], x['gf']), reverse=True)
        
        # 4. Rellenar Tabla
        tabla.setRowCount(len(lista_final))
        for i, datos in enumerate(lista_final):
            # Posición
            tabla.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            # Equipo
            tabla.setItem(i, 1, QTableWidgetItem(datos['nombre']))
            # Stats
            tabla.setItem(i, 2, QTableWidgetItem(str(datos['pj'])))
            tabla.setItem(i, 3, QTableWidgetItem(str(datos['g'])))
            tabla.setItem(i, 4, QTableWidgetItem(str(datos['e'])))
            tabla.setItem(i, 5, QTableWidgetItem(str(datos['p'])))
            tabla.setItem(i, 6, QTableWidgetItem(str(datos['gf'])))
            tabla.setItem(i, 7, QTableWidgetItem(str(datos['gc'])))
            tabla.setItem(i, 8, QTableWidgetItem(str(datos['dg'])))
            tabla.setItem(i, 9, QTableWidgetItem(str(datos['pts'])))
            
            # Centrar celdas
            for j in range(10):
                if tabla.item(i, j):
<<<<<<< Updated upstream
                    tabla.item(i, j).setTextAlignment(Qt.AlignCenter)
=======
                    tabla.item(i, j).setTextAlignment(Qt.AlignCenter)


>>>>>>> Stashed changes

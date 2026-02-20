import csv
import sys
import os 
from PySide6.QtWidgets import (
    QMessageBox, QPushButton, QFileDialog, QTableWidget, 
    QTableWidgetItem, QHeaderView, QAbstractItemView, QLabel, QVBoxLayout,
    QToolBar, QMenuBar, QSizePolicy, QApplication, QHBoxLayout, QWidget
)
from PySide6.QtGui import QAction, QColor, QBrush, QPixmap
from PySide6.QtCore import Qt, QTranslator, QCoreApplication, QTimer
from PySide6.QtSql import QSqlQuery

from Controllers.equipos_controller import EquiposController
from Controllers.participantes_controller import ParticipantesController
from Controllers.calendario_controller import CalendarioController
from Controllers.reports_controller import ReportsController
# IMPORTACIÃ“N DEL COMPONENTE RELOJ
from Views.reloj_widget import RelojDigital, ModoReloj
# IMPORTACIÃ“N DE LA NUEVA VISTA DE CONFIGURACIÃ“N
from Views.reloj_config_view import RelojConfigView


class MainController:
    def __init__(self, main_window):
        self.view = main_window
        self.view.main_controller = self
        self.ui = main_window.ui # Acceso directo a la UI
        self.app = QApplication.instance() # Referencia a la app para traducciones
        
        # --- 1. SISTEMA DE TRADUCCIONES ---
        self.translator = QTranslator()
        self.translation_path = self._resolver_ruta_traducciones()
        self.current_language = "es"
        self.translation_loaded = False
        # ----------------------------------

        # --- ARREGLO VISUAL PARA LAS CASILLAS (CHECKBOX) ---
        # Añadimos la imagen del TIC (SVG) para que se vea blanco sobre fondo rojo
        self.view.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #999;
                background-color: transparent;
                border-radius: 3px;
            }
            /* ESTADO MARCADO (CHECKED): Fondo Rojo, Borde Blanco y TIC BLANCO */
            QCheckBox::indicator:checked {
                background-color: #B71C1C; 
                border: 2px solid white;
                image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="white" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>');
            }
            QCheckBox::indicator:unchecked:hover {
                border: 2px solid #B71C1C;
            }
        """)
        # ---------------------------------------------------

        # 1. Controladores
        self.equipos_ctrl = EquiposController(main_window)
        self.participantes_ctrl = ParticipantesController(main_window)
        self.calendario_ctrl = CalendarioController(main_window, self) 
        self.reports_ctrl = ReportsController(main_window)
        self.equipos_ctrl.main_controller = self
        self.participantes_ctrl.main_controller = self
        self.equipos_ctrl.funcion_refresco_externa = self.participantes_ctrl.cargar_participantes

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
            
            self._idioma_btn_base_style = (
                "padding: 8px; font-weight: bold; border-radius: 4px; "
                "background-color: #444; color: white;"
            )
            self._idioma_btn_active_style = (
                "padding: 8px; font-weight: bold; border-radius: 4px; "
                "background-color: #B71C1C; color: white; border: 1px solid white;"
            )
            self.btn_es.setStyleSheet(self._idioma_btn_base_style)
            self.btn_en.setStyleSheet(self._idioma_btn_base_style)
            
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
        
        # 4. CONFIGURACIÃ“N DEL RELOJ EN EL DASHBOARD
        self.setup_reloj_dashboard()
        
        # 5. AÃ‘ADIR BOTÃ“N A LA BARRA SUPERIOR (MÃ‰TODO CLÃSICO - SIN ROMPER NADA)
        self.setup_toolbar_extra_button()
        
        # 6. ASEGURAR RESPONSIVIDAD Y COLOR ROJO SÃ“LIDO
        self.ensure_toolbar_responsive()

        # 7. Asegurar textos traducibles iniciales
        self.cambiar_idioma(self.current_language)

    # =========================================================================
    #  MÃ‰TODOS DE INTERNACIONALIZACIÃ“N (TRADUCCIÃ“N)
    # =========================================================================
    def _resolver_ruta_traducciones(self):
        candidatos = []
        if hasattr(sys, "_MEIPASS"):
            candidatos.append(os.path.join(sys._MEIPASS, "translations"))

        raiz_proyecto = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        candidatos.append(os.path.join(raiz_proyecto, "translations"))
        candidatos.append(os.path.join(os.getcwd(), "translations"))

        for ruta in candidatos:
            if os.path.isdir(ruta):
                return ruta

        return candidatos[0]

    def cambiar_idioma(self, codigo_idioma):
        """Carga traduccion Qt (.qm). Si falla, aplica fallback manual."""
        self.current_language = codigo_idioma if codigo_idioma in ("es", "en") else "es"
        self.app.removeTranslator(self.translator)
        self.translation_loaded = False

        archivo = f"app_{self.current_language}.qm"
        ruta = os.path.join(self.translation_path, archivo)
        if self.translator.load(ruta):
            self.app.installTranslator(self.translator)
            self.translation_loaded = True
            print(f"[OK] Idioma cambiado a: {self.current_language} ({ruta})")
        else:
            print(f"[AVISO] No se encontro traduccion en: {ruta}. Se usa fallback manual.")
        
        self.retraducir_ui()
        # Algunos widgets reciben LanguageChange después de este método.
        # Reaplicamos overrides al final del ciclo para evitar textos mezclados.
        QTimer.singleShot(0, self._post_language_sync)

    def _post_language_sync(self):
        self._apply_manual_language_overrides()
        self._set_language_button_state()
        if hasattr(self, "equipos_ctrl") and hasattr(self.equipos_ctrl, "retranslate_ui"):
            self.equipos_ctrl.retranslate_ui()
        if hasattr(self, "participantes_ctrl") and hasattr(self.participantes_ctrl, "retranslate_ui"):
            self.participantes_ctrl.retranslate_ui()
        if hasattr(self, "reports_ctrl") and hasattr(self.reports_ctrl, "retranslate_ui"):
            self.reports_ctrl.retranslate_ui()

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
        if hasattr(self, 'equipos_ctrl') and hasattr(self.equipos_ctrl, 'retranslate_ui'):
            self.equipos_ctrl.retranslate_ui()
        if hasattr(self, 'reports_ctrl') and hasattr(self.reports_ctrl, 'retranslate_ui'):
            self.reports_ctrl.retranslate_ui()
        
        # 2. Refrescar textos creados por código
        if hasattr(self, 'act_config_reloj'):
            self.act_config_reloj.setText(QCoreApplication.translate("MainController", "\u2699 Config. Reloj"))
        if hasattr(self, 'lbl_idioma'):
            self.lbl_idioma.setText(QCoreApplication.translate("MainController", "Idioma / Language:"))
        if hasattr(self, 'btn_es'):
            self.btn_es.setText(QCoreApplication.translate("MainController", "Espa\u00f1ol"))
        if hasattr(self, 'btn_en'):
            self.btn_en.setText(QCoreApplication.translate("MainController", "English"))

        # 2.1 Complemento manual para textos dinamicos/no cubiertos en .qm
        self._apply_manual_language_overrides()
        self._set_language_button_state()
             
        # 3. Refrescar tabla de clasificación si está visible
        if self.ui.stackedWidget.currentIndex() == 2:
            self.actualizar_clasificacion()

    def _set_language_button_state(self):
        if not hasattr(self, "btn_es") or not hasattr(self, "btn_en"):
            return
        es_activo = self.current_language == "es"
        self.btn_es.setStyleSheet(self._idioma_btn_active_style if es_activo else self._idioma_btn_base_style)
        self.btn_en.setStyleSheet(self._idioma_btn_base_style if es_activo else self._idioma_btn_active_style)

    def _apply_manual_language_overrides(self):
        lang = self.current_language
        es = lang == "es"

        # Barra principal
        if hasattr(self.view, "act_equipos_texto"):
            self.view.act_equipos_texto.setText("Equipos" if es else "Teams")
        if hasattr(self.view, "act_participantes_texto"):
            self.view.act_participantes_texto.setText("Participantes" if es else "Players")
        if hasattr(self.view, "act_partidos_texto"):
            self.view.act_partidos_texto.setText("Partidos" if es else "Matches")
        if hasattr(self.view, "act_clasificacion_texto"):
            self.view.act_clasificacion_texto.setText("Clasificación" if es else "Standings")
        if hasattr(self.view, "act_informes_texto"):
            self.view.act_informes_texto.setText("Informes" if es else "Reports")
        if hasattr(self.view, "act_creditos"):
            self.view.act_creditos.setText("Créditos" if es else "Credits")
        if hasattr(self.view, "act_ayuda"):
            self.view.act_ayuda.setText("Ayuda" if es else "Help")
        if hasattr(self.ui, "menuCreditos"):
            self.ui.menuCreditos.setTitle("Créditos" if es else "Credits")
        if hasattr(self.ui, "menuAyuda"):
            self.ui.menuAyuda.setTitle("Ayuda" if es else "Help")
        if hasattr(self.view, "act_salir_texto"):
            self.view.act_salir_texto.setText("Salir (Inicio)" if es else "Exit (Home)")

        # Dashboard
        if hasattr(self.view, "dashboard"):
            dash = self.view.dashboard
            if hasattr(dash, "lbl_titulo"):
                dash.lbl_titulo.setText("Panel de Control RFEF" if es else "RFEF Control Panel")
            if hasattr(dash, "btn_config_reloj"):
                dash.btn_config_reloj.setText("\u2699 Configuración del Reloj" if es else "\u2699 Clock Settings")
            if hasattr(dash, "btn_partidos"):
                dash.btn_partidos.setText("Gestión de Partidos" if es else "Match Management")
            if hasattr(dash, "btn_resultados"):
                dash.btn_resultados.setText("Resultados / Clasificación" if es else "Results / Standings")
            if hasattr(dash, "btn_equipos"):
                dash.btn_equipos.setText("Equipos" if es else "Teams")
            if hasattr(dash, "btn_participantes"):
                dash.btn_participantes.setText("Participantes" if es else "Players")

        # Acción extra de reloj
        if hasattr(self, "act_config_reloj"):
            self.act_config_reloj.setText("\u2699 Config. Reloj" if es else "\u2699 Clock Config")

        # Texto de selector de idioma
        if hasattr(self, "lbl_idioma"):
            self.lbl_idioma.setText("Idioma / Language:")
        if hasattr(self, "btn_es"):
            self.btn_es.setText("ES Español" if es else "ES Spanish")
        if hasattr(self, "btn_en"):
            self.btn_en.setText("US English")

        # Panel de configuración del reloj
        if hasattr(self, "reloj_config_view"):
            rc = self.reloj_config_view
            if hasattr(rc, "grupo_props"):
                rc.grupo_props.setTitle("Propiedades del Componente" if es else "Component Properties")
            if hasattr(rc, "lbl_modo"):
                rc.lbl_modo.setText("Modo de Funcionamiento:" if es else "Operating Mode:")
            if hasattr(rc, "combo_mode"):
                current_mode = rc.combo_mode.currentData()
                rc.combo_mode.blockSignals(True)
                rc.combo_mode.clear()
                if es:
                    rc.combo_mode.addItem("Reloj Digital (Hora)", ModoReloj.CLOCK)
                    rc.combo_mode.addItem("Cronómetro / Temporizador", ModoReloj.TIMER)
                else:
                    rc.combo_mode.addItem("Digital Clock (Time)", ModoReloj.CLOCK)
                    rc.combo_mode.addItem("Chronometer / Timer", ModoReloj.TIMER)
                idx = rc.combo_mode.findData(current_mode)
                rc.combo_mode.setCurrentIndex(idx if idx >= 0 else 0)
                rc.combo_mode.blockSignals(False)
            if hasattr(rc, "chk_24h"):
                rc.chk_24h.setText("Formato 24 Horas" if es else "24-Hour Format")
            if hasattr(rc, "chk_countdown"):
                rc.chk_countdown.setText(
                    "Modo Cuenta Regresiva (Solo Timer)" if es else "Countdown Mode (Timer Only)"
                )
            if hasattr(rc, "grupo_alarma"):
                rc.grupo_alarma.setTitle(
                    "Configuración de Alarma y Tiempos" if es else "Alarm and Time Settings"
                )
            if hasattr(rc, "chk_alarm"):
                rc.chk_alarm.setText("Alarma Activada" if es else "Alarm Enabled")
            if hasattr(rc, "lbl_mensaje"):
                rc.lbl_mensaje.setText("Mensaje de Alarma:" if es else "Alarm Message:")
            if hasattr(rc, "lbl_hora_alarma"):
                rc.lbl_hora_alarma.setText(
                    "Hora de Alarma (Modo Reloj):" if es else "Alarm Time (Clock Mode):"
                )
            if hasattr(rc, "lbl_duracion"):
                rc.lbl_duracion.setText("Duración / Límite (Segundos):" if es else "Duration / Limit (Seconds):")
            if hasattr(rc, "grupo_ctrl"):
                rc.grupo_ctrl.setTitle("Control Manual" if es else "Manual Controls")
            if hasattr(rc, "btn_start"):
                rc.btn_start.setText("Iniciar" if es else "Start")
            if hasattr(rc, "btn_pause"):
                rc.btn_pause.setText("Pausar" if es else "Pause")
            if hasattr(rc, "btn_reset"):
                rc.btn_reset.setText("Reiniciar" if es else "Reset")
            if hasattr(rc, "lbl_demo"):
                rc.lbl_demo.setText(
                    "VISTA PREVIA DEL COMPONENTE" if es else "COMPONENT PREVIEW"
                )
            if hasattr(rc, "txt_mensaje"):
                default_es = "¡Tiempo completado!"
                default_en = "Time completed!"
                txt_actual = rc.txt_mensaje.text().strip()
                if not txt_actual or txt_actual in (default_es, default_en):
                    rc.txt_mensaje.setText(default_es if es else default_en)
            if hasattr(rc, "lbl_signal"):
                waiting_es = "Esperando señal..."
                waiting_en = "Waiting for signal..."
                txt_actual = rc.lbl_signal.text().strip()
                is_notice = txt_actual.startswith("ALARMA:") or txt_actual.startswith("ALARM:")
                is_finished = ("SEÑAL RECIBIDA" in txt_actual) or ("SIGNAL RECEIVED" in txt_actual)
                if (not txt_actual) or (txt_actual in (waiting_es, waiting_en)) or (not is_notice and not is_finished):
                    rc.lbl_signal.setText(waiting_es if es else waiting_en)

        # Botones principales de calendario
        if hasattr(self, "calendario_ctrl"):
            c = self.calendario_ctrl
            if hasattr(c, "btn_generar_ronda"):
                c.btn_generar_ronda.setText("Generar Siguiente Ronda" if es else "Generate Next Round")
            if hasattr(c, "btn_clasificacion"):
                c.btn_clasificacion.setText("Ver Clasificación" if es else "View Standings")
            if hasattr(c, "btn_nueva_temporada"):
                c.btn_nueva_temporada.setText("Nueva Temporada" if es else "New Season")
            if hasattr(c, "btn_volver"):
                c.btn_volver.setText("Volver al Calendario" if es else "Back to Calendar")

        # Labels estáticos de páginas principales
        if hasattr(self.ui, "label_titulo"):
            self.ui.label_titulo.setText(
                "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">"
                + ("Calendario del torneo" if es else "Tournament Calendar")
                + "</span></p></body></html>"
            )
        if hasattr(self.ui, "pushButton_anadir_equipo"):
            self.ui.pushButton_anadir_equipo.setText("Añadir equipo" if es else "Add Team")
        if hasattr(self.ui, "pushButton_editar_equipo"):
            self.ui.pushButton_editar_equipo.setText("Editar equipo" if es else "Edit Team")
        if hasattr(self.ui, "pushButton_eliminar_equipo"):
            self.ui.pushButton_eliminar_equipo.setText("Eliminar equipo" if es else "Delete Team")
        if hasattr(self.ui, "label_3"):
            self.ui.label_3.setText(
                "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">"
                + ("Fase Final" if es else "Final Stage")
                + "</span></p></body></html>"
            )

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
        texto_boton = QCoreApplication.translate("MainController", "\u2699 Config. Reloj")
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

    def setup_dashboard_logo(self):
        """Inserta la imagen de la RFEF en el Dashboard"""
        try:
            page_dashboard = self.view.ui.stackedWidget.widget(0)
            
            if hasattr(page_dashboard, 'image_container'):
                lbl_imagen = page_dashboard.image_container
            else:
                return

            if hasattr(sys, '_MEIPASS'):
                base_path = sys._MEIPASS
            else:
                base_path = os.getcwd()
            
            ruta_img = os.path.join(base_path, "Resources", "img", "logo_rfef.jpg")
            
            if os.path.exists(ruta_img):
                pixmap = QPixmap(ruta_img)
                pixmap = pixmap.scaledToHeight(160, Qt.SmoothTransformation)
                lbl_imagen.setPixmap(pixmap)
            else:
                print(f"[AVISO] No se encontró la imagen en: {ruta_img}")
                
        except Exception as e:
            print(f"No se pudo cargar el logo del dashboard: {e}")

    def setup_reloj_dashboard(self):
        """
        Crea e inserta el reloj digital en el panel principal
        """
        try:
            page_dashboard = self.ui.stackedWidget.widget(0)
            self.reloj_sistema = RelojDigital(page_dashboard)
            
            self.reloj_sistema.mode = ModoReloj.CLOCK
            self.reloj_sistema.is24Hour = True
            self.reloj_sistema.alarmEnabled = False
            
            # Tamaño compacto para no tapar el dashboard
            self.reloj_sistema.setFixedSize(300, 68)
            
            self.reloj_sistema.setStyleSheet("""
                QLabel { 
                    font-size: 44px;
                    font-family: 'Courier New';
                    font-weight: bold;
                    color: #E0190B;
                    background-color: transparent;
                }
            """)
            
            self.reloj_sistema.start()
            
            if page_dashboard.layout():
                # Index 1: Debajo del Título
                page_dashboard.layout().insertWidget(1, self.reloj_sistema, 0, Qt.AlignCenter)
            else:
                layout = QVBoxLayout(page_dashboard)
                page_dashboard.setLayout(layout)
                layout.insertWidget(1, self.reloj_sistema, 0, Qt.AlignCenter)
                
        except Exception as e:
            print(f"Error al cargar el reloj en dashboard: {e}")

    def exportar_csv(self):
        scroll_area = self.view.ui.scrollArea_bracket
        tabla = None
        if scroll_area:
            contenedor = scroll_area.widget()
            if isinstance(contenedor, QTableWidget):
                tabla = contenedor
            elif contenedor:
                tabla = contenedor.findChild(QTableWidget)
        
        if not isinstance(tabla, QTableWidget) or tabla.rowCount() == 0:
            QMessageBox.warning(
                self.view,
                QCoreApplication.translate("MainController", "Error"),
                QCoreApplication.translate("MainController", "No hay datos para exportar.")
            )
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self.view,
            QCoreApplication.translate("MainController", "Guardar Clasificacion"),
            "clasificacion.csv",
            QCoreApplication.translate("MainController", "Archivos CSV (*.csv)")
        )
        
        if not archivo:
            return 

        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                headers = []
                for col in range(tabla.columnCount()):
                    item = tabla.horizontalHeaderItem(col)
                    headers.append(
                        item.text() if item else
                        QCoreApplication.translate("MainController", "Col {col}").format(col=col)
                    )
                writer.writerow(headers)
                
                for row in range(tabla.rowCount()):
                    row_data = []
                    for col in range(tabla.columnCount()):
                        item = tabla.item(row, col)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
            QMessageBox.information(
                self.view,
                QCoreApplication.translate("MainController", "Exito"),
                QCoreApplication.translate("MainController", "Datos exportados correctamente.")
            )
        except Exception as e:
            QMessageBox.critical(
                self.view,
                QCoreApplication.translate("MainController", "Error"),
                QCoreApplication.translate("MainController", "Error al guardar: {error}").format(error=e)
            )

    def mostrar_creditos(self):
        es = self.current_language == "es"
        if es:
            titulo = "Acerca de - Gestor de Torneos"
            texto = """
            <h3>Gestor de Torneos de Futbol</h3>
            <p>Aplicacion para la gestion integral de competiciones deportivas.</p>
            <hr>
            <p><b>Autor:</b> Alex</p>
            <p><b>Fecha de Actualizacion:</b> 29 de Enero de 2026</p>
            <p><b>Version:</b> 1.0.0 (Release Final)</p>
            <hr>
            <p><i>Desarrollado con Python 3.13, PySide6 y SQLite.</i></p>
            """
        else:
            titulo = "About - Tournament Manager"
            texto = """
            <h3>Football Tournament Manager</h3>
            <p>Desktop application for complete sports competition management.</p>
            <hr>
            <p><b>Author:</b> Alex</p>
            <p><b>Last Update:</b> January 29, 2026</p>
            <p><b>Version:</b> 1.0.0 (Final Release)</p>
            <hr>
            <p><i>Built with Python 3.13, PySide6 and SQLite.</i></p>
            """
        QMessageBox.about(self.view, titulo, texto)

    def mostrar_ayuda(self):
        es = self.current_language == "es"
        if es:
            titulo = "Ayuda - Guia Rapida"
            texto = """
            <h3>Como utilizar el Gestor</h3>
            <ol>
                <li><b>Crear Equipos:</b> Ve a la pestana 'Equipos' y registra los clubes participantes.</li>
                <li><b>Generar Torneo:</b> En la pestana 'Partidos', pulsa el boton verde <b>'Generar Siguiente Ronda'</b>.</li>
                <li><b>Registrar Resultados:</b> Haz <b>doble clic</b> sobre un partido del calendario para editar el marcador, la fecha y asignar goles a jugadores.</li>
                <li><b>Eliminar Errores:</b> Haz <b>clic derecho</b> sobre un partido si necesitas borrarlo.</li>
                <li><b>Ver Clasificacion:</b> Consulta la tabla actualizada automaticamente en la seccion 'Clasificacion'.</li>
            </ol>
            <p><i>Nota: Es necesario completar todos los partidos de una ronda para poder generar la siguiente.</i></p>
            """
        else:
            titulo = "Help - Quick Guide"
            texto = """
            <h3>How to use the Manager</h3>
            <ol>
                <li><b>Create Teams:</b> Go to the 'Teams' section and register the participating clubs.</li>
                <li><b>Generate Tournament:</b> In the 'Matches' section, click the green <b>'Generate Next Round'</b> button.</li>
                <li><b>Record Results:</b> Double-click a match in the calendar to edit score, date and player stats.</li>
                <li><b>Delete Errors:</b> Right-click a match if you need to remove it.</li>
                <li><b>View Standings:</b> Check the automatically updated table in the 'Standings' section.</li>
            </ol>
            <p><i>Note: all matches in a round must be completed before generating the next one.</i></p>
            """
        QMessageBox.about(self.view, titulo, texto)

    def arreglar_botones_rebeldes(self):
        page_cal = self.view.ui.page_calendario
        if page_cal:
            for btn in page_cal.findChildren(QPushButton):
                texto = btn.text().lower()
                if "clasificaci" in texto or "tabla" in texto or "standings" in texto or "table" in texto:
                    try: btn.clicked.disconnect() 
                    except: pass
                    btn.clicked.connect(lambda: self.cambiar_pagina(2))

    def init_dashboard_connections(self):
        self.view.dashboard.btn_equipos.clicked.connect(lambda: self.cambiar_pagina(3))
        self.view.dashboard.btn_participantes.clicked.connect(lambda: self.cambiar_pagina(4))
        self.view.dashboard.btn_partidos.clicked.connect(lambda: self.cambiar_pagina(1))
        self.view.dashboard.btn_resultados.clicked.connect(lambda: self.cambiar_pagina(2))
        
        # Conexión del botón del dashboard (el que está en el centro de la pantalla)
        if hasattr(self.view.dashboard, 'btn_config_reloj'):
             self.view.dashboard.btn_config_reloj.clicked.connect(lambda: self.cambiar_pagina(self.index_reloj_config))

    def init_toolbar_connections(self):
        # Botones existentes del .ui
        if hasattr(self.view, 'act_equipos_texto'):
            self.view.act_equipos_texto.triggered.connect(lambda: self.cambiar_pagina(3))
        if hasattr(self.view, 'act_participantes_texto'):
            self.view.act_participantes_texto.triggered.connect(lambda: self.cambiar_pagina(4))
        if hasattr(self.view, 'act_partidos_texto'):
            self.view.act_partidos_texto.triggered.connect(lambda: self.cambiar_pagina(1))
        if hasattr(self.view, 'act_salir_texto'):
            self.view.act_salir_texto.triggered.connect(lambda: self.cambiar_pagina(0))
            
        if hasattr(self.view, 'act_clasificacion_texto'):
            self.view.act_clasificacion_texto.triggered.connect(lambda: self.cambiar_pagina(2))
        if hasattr(self.view, 'act_informes_texto'):
            self.view.act_informes_texto.triggered.connect(self.reports_ctrl.show)

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
        scroll_area = self.view.ui.scrollArea_bracket
        tabla = None
        contenedor = None
        if scroll_area:
            contenedor = scroll_area.widget()

        # Si antes se había reemplazado el widget por la tabla, la reutilizamos
        if isinstance(contenedor, QTableWidget):
            tabla = contenedor
        else:
            # Si el contenedor existe, buscamos una tabla ya creada
            if contenedor:
                tabla = contenedor.findChild(QTableWidget)
            if tabla is None:
                tabla = QTableWidget()
                tabla.setStyleSheet("background-color: #252526; color: #ddd; border: none;")
                tabla.horizontalHeader().setStretchLastSection(True)
                tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
                tabla.verticalHeader().setVisible(False)

                # Reutilizamos el widget existente del scroll para no destruirlo
                if contenedor is None and scroll_area:
                    contenedor = QWidget()
                    scroll_area.setWidget(contenedor)
                if contenedor is not None:
                    layout = contenedor.layout()
                    if layout is None:
                        layout = QVBoxLayout(contenedor)
                        layout.setContentsMargins(0, 0, 0, 0)
                        contenedor.setLayout(layout)
                    layout.addWidget(tabla)

                    # Ocultar etiquetas antiguas del bracket para evitar solapes
                    for nombre in ("label_4", "label_5", "label_6"):
                        lbl = getattr(self.view.ui, nombre, None)
                        if lbl:
                            lbl.hide()
        
        # --- CABECERAS TRADUCIBLES ---
        # Usamos QCoreApplication.translate para que se puedan traducir al cambiar idioma
        t_pos = QCoreApplication.translate("MainController", "Pos")
        t_equipo = QCoreApplication.translate("MainController", "Equipo")
        t_pj = QCoreApplication.translate("MainController", "PJ")
        t_g = QCoreApplication.translate("MainController", "G")
        t_e = QCoreApplication.translate("MainController", "E")
        t_p = QCoreApplication.translate("MainController", "P")
        t_gf = QCoreApplication.translate("MainController", "GF")
        t_gc = QCoreApplication.translate("MainController", "GC")
        t_dg = QCoreApplication.translate("MainController", "DG")
        t_pts = QCoreApplication.translate("MainController", "Pts")

        columnas = [t_pos, t_equipo, t_pj, t_g, t_e, t_p, t_gf, t_gc, t_dg, t_pts]
        # -----------------------------

        tabla.setColumnCount(len(columnas))
        tabla.setHorizontalHeaderLabels(columnas)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        tabla.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        
        equipos_stats = {}
        q_eq = QSqlQuery("SELECT id, nombre FROM equipos")
        while q_eq.next():
            eid = q_eq.value(0)
            equipos_stats[eid] = {
                'nombre': q_eq.value(1),
                'pj': 0, 'g': 0, 'e': 0, 'p': 0, 
                'gf': 0, 'gc': 0, 'dg': 0, 'pts': 0
            }
            
        q_part = QSqlQuery("SELECT equipo_local_id, equipo_visitante_id, goles_local, goles_visitante FROM partidos WHERE jugado = 1")
        while q_part.next():
            l_id = q_part.value(0)
            v_id = q_part.value(1)
            gl = q_part.value(2)
            gv = q_part.value(3)
            
            if l_id in equipos_stats and v_id in equipos_stats:
                equipos_stats[l_id]['pj'] += 1
                equipos_stats[l_id]['gf'] += gl
                equipos_stats[l_id]['gc'] += gv
                equipos_stats[v_id]['pj'] += 1
                equipos_stats[v_id]['gf'] += gv
                equipos_stats[v_id]['gc'] += gl
                
                if gl > gv:
                    equipos_stats[l_id]['g'] += 1
                    equipos_stats[l_id]['pts'] += 3
                    equipos_stats[v_id]['p'] += 1
                elif gv > gl:
                    equipos_stats[v_id]['g'] += 1
                    equipos_stats[v_id]['pts'] += 3
                    equipos_stats[l_id]['p'] += 1
                else:
                    equipos_stats[l_id]['e'] += 1
                    equipos_stats[l_id]['pts'] += 1
                    equipos_stats[v_id]['e'] += 1
                    equipos_stats[v_id]['pts'] += 1

        lista_final = []
        for eid, s in equipos_stats.items():
            s['dg'] = s['gf'] - s['gc']
            lista_final.append(s)
            
        lista_final.sort(key=lambda x: (x['pts'], x['dg'], x['gf']), reverse=True)
        
        tabla.setRowCount(len(lista_final))
        for i, datos in enumerate(lista_final):
            tabla.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            tabla.setItem(i, 1, QTableWidgetItem(datos['nombre']))
            tabla.setItem(i, 2, QTableWidgetItem(str(datos['pj'])))
            tabla.setItem(i, 3, QTableWidgetItem(str(datos['g'])))
            tabla.setItem(i, 4, QTableWidgetItem(str(datos['e'])))
            tabla.setItem(i, 5, QTableWidgetItem(str(datos['p'])))
            tabla.setItem(i, 6, QTableWidgetItem(str(datos['gf'])))
            tabla.setItem(i, 7, QTableWidgetItem(str(datos['gc'])))
            tabla.setItem(i, 8, QTableWidgetItem(str(datos['dg'])))
            tabla.setItem(i, 9, QTableWidgetItem(str(datos['pts'])))
            
            for j in range(10):
                if tabla.item(i, j):
                    tabla.item(i, j).setTextAlignment(Qt.AlignCenter)



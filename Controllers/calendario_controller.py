from PySide6.QtWidgets import (
    QMessageBox, QTreeWidgetItem, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QTableWidget, QTableWidgetItem, QSizePolicy,
    QSpinBox, QWidget, QDialog, QHeaderView, QAbstractItemView,
    QAbstractSpinBox, QComboBox, QDateEdit, QTimeEdit, QMenu, QTabWidget
)
from PySide6.QtSql import QSqlQuery
from PySide6.QtCore import Qt, QDate, QTime, QCoreApplication
from PySide6.QtGui import QFont, QColor, QAction
from Views.reloj_widget import RelojDigital, ModoReloj
import random

# ============================================================================
# 1. CLASES PERSONALIZADAS (DISEÑO MEJORADO)
# ============================================================================

class CustomSpinBox(QSpinBox):
    """SpinBox central, grande y oscuro, sin botones nativos"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QSpinBox {
                background-color: #3e3e42;
                color: white;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 5px;
                font-size: 24px;
                font-weight: bold;
                min-height: 50px;
                min-width: 80px;
            }
        """)
        self.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.stepUp()
        else:
            self.stepDown()

def crear_spinbox_con_botones(label_text, valor_inicial=0):
    """Crea el conjunto de botones GIGANTES + y - separados"""
    contenedor = QWidget()
    layout = QHBoxLayout()
    # Aumentamos mucho el espaciado entre botones
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(20) 
    
    spinbox = CustomSpinBox()
    spinbox.setValue(valor_inicial)
    spinbox.setMinimum(0)
    
    # Estilo para botones gigantes y claros
    estilo_btn = """
        QPushButton {
            background-color: #B71C1C;
            color: white;
            border: 3px solid #8B0000;
            border-radius: 10px;
            font-family: Arial;
            font-size: 36px; 
            font-weight: 900;
            padding-bottom: 5px; 
        }
        QPushButton:hover {
            background-color: #ff3333;
            border-color: #ff0000;
        }
        QPushButton:pressed {
            background-color: #8B0000;
            border-color: #500000;
        }
    """
    
    # Botón Menos Gigante
    btn_menos = QPushButton("-")
    btn_menos.setFixedSize(60, 60)
    btn_menos.setCursor(Qt.CursorShape.PointingHandCursor)
    btn_menos.setStyleSheet(estilo_btn)
    btn_menos.clicked.connect(spinbox.stepDown)
    
    # Botón Más Gigante
    btn_mas = QPushButton("+")
    btn_mas.setFixedSize(60, 60)
    btn_mas.setCursor(Qt.CursorShape.PointingHandCursor)
    btn_mas.setStyleSheet(estilo_btn)
    btn_mas.clicked.connect(spinbox.stepUp)
    
    layout.addWidget(btn_menos)
    layout.addWidget(spinbox) # El spinbox se expande
    layout.addWidget(btn_mas)
    
    contenedor.setLayout(layout)
    contenedor.spinbox = spinbox 
    return contenedor


# ============================================================================
# 2. CONTROLADOR PRINCIPAL DEL CALENDARIO
# ============================================================================

class CalendarioController:
    
    def __init__(self, main_window, main_controller=None):
        self.main_view = main_window
        self.main_controller = main_controller
        self.view = main_window # Referencia extra por compatibilidad
        
        self.page_calendario = self.main_view.ui.page_calendario
        self.tree_widget = self.main_view.ui.treeWidget_partidos
        
        # Configurar Árbol
        self.tree_widget.setColumnCount(1)
        if hasattr(self.tree_widget.header(), 'setStretchLastSection'):
            self.tree_widget.header().setStretchLastSection(True)
        
        self.tree_widget.setHeaderHidden(True) 
        self.tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        
        # Inicializar datos
        self.asegurar_columnas_bd()
        self.setup_ui()
        self.init_connections()
        self.cargar_calendario()
    
    def asegurar_columnas_bd(self):
        """Asegura que existen las columnas nuevas en la BD"""
        try:
            QSqlQuery().exec("ALTER TABLE partidos ADD COLUMN fecha TEXT")
        except:
            pass
        try:
            QSqlQuery().exec("ALTER TABLE partidos ADD COLUMN id_arbitro INTEGER")
        except:
            pass

    def setup_ui(self):
        layout_main = self.page_calendario.layout()
        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(10)
        
        self.btn_generar_ronda = QPushButton("Generar Siguiente Ronda")
        self.btn_generar_ronda.setStyleSheet("""
            QPushButton {
                background-color: #2d7d2d;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #3da83d; }
        """)
        
        self.btn_clasificacion = QPushButton("Ver Clasificación")
        self.btn_clasificacion.setStyleSheet("""
            QPushButton {
                background-color: #1a5d7d;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #2a7d9d; }
        """)
        
        self.btn_nueva_temporada = QPushButton("Nueva Temporada")
        self.btn_nueva_temporada.setStyleSheet("""
            QPushButton {
                background-color: #7d2d2d;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #a83d3d; }
        """)
        
        layout_botones.addWidget(self.btn_generar_ronda)
        layout_botones.addWidget(self.btn_clasificacion)
        layout_botones.addWidget(self.btn_nueva_temporada)
        layout_botones.addStretch()
        
        layout_main.insertLayout(0, layout_botones)
        
        self.lbl_ronda_actual = QLabel("Ronda actual: Ninguna generada")
        self.lbl_ronda_actual.setStyleSheet("color: #888; font-style: italic; margin-top: 5px;")
        layout_main.insertWidget(1, self.lbl_ronda_actual)
        
        self.tabla_clasificacion = QTableWidget()
        self.tabla_clasificacion.setVisible(False)
        self.tabla_clasificacion.setStyleSheet("background-color: #252526; color: #ddd; gridline-color: #444;")
        layout_main.addWidget(self.tabla_clasificacion)
        
        self.btn_volver = QPushButton("Volver al Calendario")
        self.btn_volver.setVisible(False)
        layout_main.addWidget(self.btn_volver)
    
    def init_connections(self):
        self.btn_generar_ronda.clicked.connect(self.generar_siguiente_ronda)
        self.btn_clasificacion.clicked.connect(self.mostrar_clasificacion)
        self.btn_nueva_temporada.clicked.connect(self.nueva_temporada)
        self.btn_volver.clicked.connect(self.volver_calendario)
        self.tree_widget.itemDoubleClicked.connect(self.editar_partido)
        self.tree_widget.customContextMenuRequested.connect(self.mostrar_menu_contextual)
    
    def obtener_nombre_equipo(self, id_equipo):
        q = QSqlQuery()
        q.prepare("SELECT nombre FROM equipos WHERE id = ?")
        q.addBindValue(id_equipo)
        if q.exec() and q.next():
            return q.value(0)
        return "Equipo"

    def crear_color_ronda(self, fase):
        if fase == "Final": return QColor(180, 50, 50)
        if fase == "Semifinal": return QColor(50, 80, 180)
        if fase == "Cuartos": return QColor(60, 120, 180)
        if fase == "Octavos": return QColor(60, 160, 160)
        return QColor(80, 80, 80)

    def cargar_calendario(self):
        self.tree_widget.clear()
        self.tree_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        query = QSqlQuery("""
            SELECT DISTINCT fase FROM partidos WHERE fase IS NOT NULL 
            ORDER BY CASE fase 
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
        
        if not rondas:
            self.lbl_ronda_actual.setText("Ronda actual: Ninguna generada")
            self.tree_widget.addTopLevelItem(QTreeWidgetItem(["No hay partidos programados"]))
            return

        self.lbl_ronda_actual.setText(f"Ronda actual: {rondas[-1]}")
        
        for ronda in rondas:
            ronda_item = QTreeWidgetItem([ronda])
            ronda_item.setBackground(0, self.crear_color_ronda(ronda))
            ronda_item.setForeground(0, Qt.GlobalColor.white)
            ronda_item.setExpanded(True)
            
            q = QSqlQuery()
            q.prepare("""
                SELECT id, equipo_local_id, equipo_visitante_id, goles_local, goles_visitante, 
                       jugado, hora, id_arbitro, fecha 
                FROM partidos WHERE fase = ? ORDER BY id
            """)
            q.addBindValue(ronda)
            
            if q.exec():
                while q.next():
                    id_p = q.value(0)
                    local = self.obtener_nombre_equipo(q.value(1))
                    visit = self.obtener_nombre_equipo(q.value(2))
                    gl = q.value(3)
                    gv = q.value(4)
                    jugado = q.value(5)
                    hora = q.value(6) or "21:00"
                    
                    # Fecha
                    fecha = q.value(8)
                    str_fecha = f" [{fecha}]" if fecha else ""
                    
                    # Árbitro
                    id_arb = q.value(7)
                    arb_txt = ""
                    if id_arb:
                        qa = QSqlQuery()
                        qa.prepare("SELECT nombre FROM participantes WHERE id=?")
                        qa.addBindValue(id_arb)
                        if qa.exec() and qa.next():
                            arb_txt = f" (Árb: {qa.value(0)})"

                    if jugado:
                        texto = f"[{hora}]{str_fecha}  {local}  {gl} - {gv}  {visit}{arb_txt}   (Finalizado)"
                    else:
                        texto = f"[{hora}]{str_fecha}  {local}  vs  {visit}{arb_txt}"
                    
                    item_partido = QTreeWidgetItem([texto])
                    item_partido.setData(0, Qt.ItemDataRole.UserRole, id_p)
                    ronda_item.addChild(item_partido)
            
            self.tree_widget.addTopLevelItem(ronda_item)

    def mostrar_menu_contextual(self, pos):
        item = self.tree_widget.itemAt(pos)
        if not item or item.parent() is None:
            return
        
        id_partido = item.data(0, Qt.ItemDataRole.UserRole)
        if not id_partido:
            return
            
        menu = QMenu(self.main_view)
        accion_eliminar = QAction("Eliminar Partido", self.main_view)
        accion_eliminar.triggered.connect(lambda: self.eliminar_partido(id_partido))
        menu.addAction(accion_eliminar)
        
        menu.exec(self.tree_widget.viewport().mapToGlobal(pos))

    def eliminar_partido(self, id_partido):
        if QMessageBox.question(self.main_view, "Confirmar", "¿Eliminar este partido?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            QSqlQuery().exec(f"DELETE FROM partidos WHERE id={id_partido}")
            self.cargar_calendario()
            if self.main_controller:
                self.main_controller.actualizar_clasificacion()

    def generar_siguiente_ronda(self):
        fases_orden = ["Final", "Semifinal", "Cuartos", "Octavos"]
        fase_actual = None
        
        q_fase = QSqlQuery("SELECT DISTINCT fase FROM partidos")
        fases_bd = set()
        while q_fase.next():
            fases_bd.add(q_fase.value(0))
            
        for f in fases_orden:
            if f in fases_bd:
                fase_actual = f
                break
                
        # 1. EMPEZAR TORNEO (SIEMPRE EN OCTAVOS)
        if fase_actual is None:
            qc = QSqlQuery("SELECT count(*) FROM partidos")
            qc.next()
            if qc.value(0) > 0:
                QMessageBox.information(self.main_view, "Info", "Reinicia la temporada.")
                return
            
            eqs = []
            qe = QSqlQuery("SELECT id FROM equipos")
            while qe.next():
                eqs.append(qe.value(0))
                
            if len(eqs) < 2:
                QMessageBox.warning(self.main_view, "Error", "Faltan equipos (mínimo 2).")
                return
            
            # --- CAMBIO: Siempre empieza en Octavos ---
            fase = "Octavos"
            self.generar_partidos_fase(fase, eqs)
            return

        # 2. VERIFICAR PENDIENTES
        qchk = QSqlQuery()
        qchk.prepare("SELECT count(*) FROM partidos WHERE fase=? AND jugado=0")
        qchk.addBindValue(fase_actual)
        if qchk.exec() and qchk.next() and qchk.value(0) > 0:
            QMessageBox.information(self.main_view, "Info", "Partidos pendientes.")
            return
            
        # 3. SIGUIENTE FASE
        sig = "Cuartos" if fase_actual == "Octavos" else "Semifinal" if fase_actual == "Cuartos" else "Final" if fase_actual == "Semifinal" else None
        
        if not sig:
            ganador = "Desconocido"
            qf = QSqlQuery("SELECT equipo_local_id, equipo_visitante_id, goles_local, goles_visitante FROM partidos WHERE fase = 'Final'")
            if qf.exec() and qf.next():
                gl = qf.value(2)
                gv = qf.value(3)
                ganador = self.obtener_nombre_equipo(qf.value(0)) if gl > gv else self.obtener_nombre_equipo(qf.value(1)) if gv > gl else "Empate"
            QMessageBox.information(self.main_view, "¡Fin!", f"🏆 CAMPEÓN: {ganador.upper()} 🏆")
            return

        ganadores = []
        qg = QSqlQuery()
        qg.prepare("SELECT CASE WHEN goles_local > goles_visitante THEN equipo_local_id ELSE equipo_visitante_id END FROM partidos WHERE fase=? ORDER BY id")
        qg.addBindValue(fase_actual)
        
        if qg.exec():
            while qg.next():
                ganadores.append(qg.value(0))
        
        if len(ganadores) < 2:
            QMessageBox.warning(self.main_view, "Error", "Faltan ganadores.")
            return
            
        self.generar_partidos_fase(sig, ganadores)

    def generar_partidos_fase(self, fase, equipos):
        creados = 0
        horas = ["18:00", "19:00", "20:00", "21:00"]
        fecha_hoy = QDate.currentDate().toString("yyyy-MM-dd")
        
        for i in range(0, len(equipos)-1, 2):
            q = QSqlQuery()
            q.prepare("INSERT INTO partidos (fase, equipo_local_id, equipo_visitante_id, jugado, goles_local, goles_visitante, hora, fecha) VALUES (?,?,?,0,0,0,?,?)")
            q.addBindValue(fase)
            q.addBindValue(equipos[i])
            q.addBindValue(equipos[i+1])
            q.addBindValue(random.choice(horas))
            q.addBindValue(fecha_hoy)
            if q.exec():
                creados += 1
        
        if creados > 0:
            QMessageBox.information(self.main_view, "Éxito", f"Ronda {fase} generada.")
            self.cargar_calendario()
        else:
            QMessageBox.warning(self.main_view, "Error", "Fallo al generar.")

    def editar_partido(self, item, column):
        """Abre ventana flotante de edición con RELOJ INTEGRADO"""
        if item.parent() is None: return
        
        id_partido = item.data(0, Qt.ItemDataRole.UserRole)
        if not id_partido: return

        q = QSqlQuery()
        q.prepare("SELECT equipo_local_id, equipo_visitante_id, goles_local, goles_visitante, id_arbitro, fecha, hora FROM partidos WHERE id=?")
        q.addBindValue(id_partido)
        if not q.exec() or not q.next(): return

        id_local = q.value(0)
        id_visitante = q.value(1)
        
        local = self.obtener_nombre_equipo(id_local)
        visit = self.obtener_nombre_equipo(id_visitante)
        
        gl = q.value(2)
        gv = q.value(3)
        id_arb_actual = q.value(4)
        fecha_bd = q.value(5)
        hora_bd = q.value(6)

        dialog = QDialog(self.main_view)
        dialog.setWindowTitle(f"{local} vs {visit}")
        dialog.setFixedSize(500, 800) 
        dialog.setStyleSheet("background-color: #252526; color: white;")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # =========================================================
        # RELOJ DIGITAL - INICIO AUTOMÁTICO Y REINICIO
        # =========================================================
        
        self.reloj_partido = RelojDigital()
        # CONFIGURACIÓN PARA CONTEXTO DE PARTIDO (Modo Timer)
        self.reloj_partido.mode = ModoReloj.TIMER
        self.reloj_partido.duracionPartido = 90 * 60  # Duración configurable
        self.reloj_partido.alarmMessage = "¡FIN DEL TIEMPO REGLAMENTARIO!" 
        self.reloj_partido.alarmEnabled = True
        
        self.reloj_partido.alarmTriggered.connect(lambda msg: QMessageBox.information(dialog, "Tiempo", msg))        
        layout.addWidget(QLabel("⏱ CRONÓMETRO DEL PARTIDO", font=QFont("Arial", 10, QFont.Bold)))
        layout.addWidget(self.reloj_partido)
        
        # --- BOTONES DE CONTROL ---
        layout_reloj_btns = QHBoxLayout()
        
        btn_iniciar_reloj = QPushButton("▶ Iniciar")
        btn_iniciar_reloj.clicked.connect(self.reloj_partido.start)
        btn_iniciar_reloj.setStyleSheet("background-color: #2d7d2d; color: white;")
        
        btn_pausar_reloj = QPushButton("⏸ Pausar")
        btn_pausar_reloj.clicked.connect(self.reloj_partido.pause)
        btn_pausar_reloj.setStyleSheet("background-color: #d8a600; color: black;")
        
        # --- BOTÓN REINICIAR NUEVO ---
        btn_reiniciar_reloj = QPushButton("↺ Reiniciar")
        btn_reiniciar_reloj.clicked.connect(self.reloj_partido.reset)
        btn_reiniciar_reloj.setStyleSheet("background-color: #7d2d2d; color: white;")
        
        layout_reloj_btns.addWidget(btn_iniciar_reloj)
        layout_reloj_btns.addWidget(btn_pausar_reloj)
        layout_reloj_btns.addWidget(btn_reiniciar_reloj) # Añadido
        
        layout.addLayout(layout_reloj_btns)
        
        # --- AUTO-INICIO AL ABRIR ---
        self.reloj_partido.start()
        
        # Separador visual
        linea_reloj = QWidget()
        linea_reloj.setFixedHeight(2)
        linea_reloj.setStyleSheet("background-color: #444; margin: 10px 0;")
        layout.addWidget(linea_reloj)
        # =========================================================

        layout.addWidget(QLabel(f"Goles {local}:", font=QFont("Arial", 12, QFont.Bold)))
        w_local = crear_spinbox_con_botones(local, gl)
        layout.addWidget(w_local)

        layout.addWidget(QLabel(f"Goles {visit}:", font=QFont("Arial", 12, QFont.Bold)))
        w_visit = crear_spinbox_con_botones(visit, gv)
        layout.addWidget(w_visit)

        linea = QWidget()
        linea.setFixedHeight(2)
        linea.setStyleSheet("background-color: #444; margin: 10px 0;")
        layout.addWidget(linea)

        lh = QHBoxLayout()
        v1 = QVBoxLayout()
        v1.addWidget(QLabel("Fecha:"))
        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setStyleSheet("QDateEdit { background-color: #3e3e42; padding: 8px; font-size: 16px; border: 2px solid #555; border-radius: 4px; }")
        date_edit.setMinimumDate(QDate.currentDate())
        if fecha_bd:
            date_edit.setDate(QDate.fromString(fecha_bd, "yyyy-MM-dd"))
        else:
            date_edit.setDate(QDate.currentDate())
        v1.addWidget(date_edit)
        lh.addLayout(v1)

        v2 = QVBoxLayout()
        v2.addWidget(QLabel("Hora:"))
        combo_hora = QComboBox()
        combo_hora.setStyleSheet("QComboBox { background-color: #3e3e42; padding: 8px; font-size: 16px; border: 2px solid #555; border-radius: 4px; } QComboBox::drop-down { border: none; }")
        for h in range(9, 24):
            combo_hora.addItems([f"{h:02d}:00", f"{h:02d}:30"])
        if hora_bd:
            combo_hora.setCurrentText(hora_bd)
        else:
            combo_hora.setCurrentText("21:00")
        v2.addWidget(combo_hora)
        lh.addLayout(v2)
        layout.addLayout(lh)

        layout.addWidget(QLabel("Árbitro asignado:"))
        combo_arb = QComboBox()
        combo_arb.setStyleSheet("QComboBox { background-color: #3e3e42; padding: 8px; font-size: 16px; border: 2px solid #555; border-radius: 4px; }")
        combo_arb.addItem("Sin asignar", None)
        
        qa = QSqlQuery("SELECT id, nombre FROM participantes WHERE tipo_participante LIKE '%Árbitro%' OR tipo_participante = 'Ambos'")
        idx_sel = 0
        i = 1
        while qa.next():
            combo_arb.addItem(qa.value(1), qa.value(0))
            if id_arb_actual and qa.value(0) == id_arb_actual:
                idx_sel = i
            i += 1
        combo_arb.setCurrentIndex(idx_sel)
        layout.addWidget(combo_arb)

        btn_players = QPushButton("Gestionar Goles y Tarjetas (Jugadores)")
        btn_players.setStyleSheet("QPushButton { background-color: #1a5d7d; color: white; padding: 12px; font-size: 16px; font-weight: bold; border-radius: 6px; } QPushButton:hover { background-color: #2a7d9d; }")
        
        def gestionar_y_sumar():
            goles_l_antes = w_local.spinbox.value()
            goles_v_antes = w_visit.spinbox.value()
            goles_l_nuevos, goles_v_nuevos = self.gestionar_jugadores(id_local, id_visitante)
            w_local.spinbox.setValue(goles_l_antes + goles_l_nuevos)
            w_visit.spinbox.setValue(goles_v_antes + goles_v_nuevos)

        btn_players.clicked.connect(gestionar_y_sumar)
        layout.addWidget(btn_players)

        btn_save = QPushButton("GUARDAR RESULTADO DEL PARTIDO")
        btn_save.setStyleSheet("QPushButton { background-color: #2d7d2d; color: white; padding: 15px; font-size: 18px; font-weight: 900; border-radius: 8px; margin-top: 10px; } QPushButton:hover { background-color: #3da83d; }")
        
        def guardar():
            id_arb = combo_arb.currentData()
            f_str = date_edit.date().toString("yyyy-MM-dd")
            h_str = combo_hora.currentText()
            qu = QSqlQuery()
            qu.prepare("UPDATE partidos SET goles_local=?, goles_visitante=?, jugado=1, id_arbitro=?, fecha=?, hora=? WHERE id=?")
            qu.addBindValue(w_local.spinbox.value()); qu.addBindValue(w_visit.spinbox.value())
            qu.addBindValue(id_arb); qu.addBindValue(f_str); qu.addBindValue(h_str); qu.addBindValue(id_partido)
            if qu.exec():
                dialog.accept()
                self.cargar_calendario() 
                if self.main_controller: 
                    self.main_controller.actualizar_clasificacion() 
            else:
                QMessageBox.critical(dialog, "Error", qu.lastError().text())

        btn_save.clicked.connect(guardar)
        layout.addWidget(btn_save)
        
        dialog.setLayout(layout)
        dialog.exec()

    def gestionar_jugadores(self, id_local, id_visitante):
        dialog = QDialog(self.main_view)
        dialog.setWindowTitle("Estadísticas de Jugadores")
        dialog.setFixedSize(800, 600)
        dialog.setStyleSheet("background-color: #252526; color: white;")
        layout = QVBoxLayout(dialog)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; top: -1px; } 
            QTabBar::tab { background: #333; color: #aaa; padding: 10px 20px; font-size: 14px; border: 1px solid #444; border-bottom: none; border-top-left-radius: 4px; border-top-right-radius: 4px; } 
            QTabBar::tab:selected { background: #1a5d7d; color: white; font-weight: bold; }
            QTabBar::tab:hover { background: #444; }
        """)
        
        equipos = [(id_local, "Local"), (id_visitante, "Visitante")]
        tablas = [] 
        
        for eid, tipo_eq in equipos:
            page = QWidget()
            playout = QVBoxLayout(page)
            tabla = QTableWidget()
            tabla.setColumnCount(4)
            tabla.setHorizontalHeaderLabels(["Nombre del Jugador", "Goles (+)", "Amarillas (+)", "Rojas (+)"])
            tabla.setStyleSheet("""
                QTableWidget { background-color: #2b2b2b; color: white; gridline-color: #444; font-size: 14px; selection-background-color: transparent; }
                QHeaderView::section { background-color: #333; padding: 8px; font-weight: bold; border: 1px solid #444; }
                QTableWidget::item { padding: 5px; }
            """)
            tabla.verticalHeader().setVisible(False)
            tabla.horizontalHeader().setStretchLastSection(True)
            tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            
            q = QSqlQuery(f"SELECT id, nombre, goles FROM participantes WHERE id_equipo={eid}")
            row = 0
            while q.next():
                tabla.insertRow(row)
                pid = q.value(0)
                nombre = q.value(1)
                txt = f"{nombre} (Total: {q.value(2)}G)"
                item_nom = QTableWidgetItem(txt)
                item_nom.setFlags(Qt.ItemIsEnabled) 
                item_nom.setData(Qt.UserRole, pid) 
                tabla.setItem(row, 0, item_nom)
                
                for col in range(1, 4):
                    container = QWidget()
                    lay = QHBoxLayout(container); lay.setContentsMargins(5, 2, 5, 2)
                    sp = QSpinBox()
                    sp.setStyleSheet("QSpinBox { background-color: #444; color: white; padding: 5px; font-weight: bold; border: 1px solid #555; }")
                    sp.setAlignment(Qt.AlignCenter)
                    if col == 1: sp.setRange(0, 10) 
                    elif col == 2: sp.setRange(0, 2)
                    elif col == 3: sp.setRange(0, 1)
                    lay.addWidget(sp)
                    tabla.setCellWidget(row, col, container)
                tabla.setRowHeight(row, 50)
                row += 1
            
            playout.addWidget(tabla)
            nombre_equipo = self.obtener_nombre_equipo(eid)
            tabs.addTab(page, f"{nombre_equipo}")
            tablas.append(tabla)
            
        layout.addWidget(tabs)
        
        btn_guardar = QPushButton("CONFIRMAR Y ACTUALIZAR ESTADÍSTICAS")
        btn_guardar.setStyleSheet("QPushButton { background-color: #2d7d2d; color: white; padding: 15px; font-size: 16px; font-weight: bold; border-radius: 6px; } QPushButton:hover { background-color: #3da83d; }")
        
        self.goles_local_sumados = 0
        self.goles_visit_sumados = 0
        
        def guardar_stats():
            try:
                changed = False
                self.goles_local_sumados = 0
                self.goles_visit_sumados = 0
                for i, t in enumerate(tablas):
                    goles_equipo = 0
                    for r in range(t.rowCount()):
                        pid = t.item(r, 0).data(Qt.UserRole)
                        w_gol = t.cellWidget(r, 1).findChild(QSpinBox)
                        w_ama = t.cellWidget(r, 2).findChild(QSpinBox)
                        w_roj = t.cellWidget(r, 3).findChild(QSpinBox)
                        gs = w_gol.value()
                        asum = w_ama.value()
                        rs = w_roj.value()
                        if gs > 0: goles_equipo += gs
                        if gs > 0 or asum > 0 or rs > 0:
                            q = QSqlQuery()
                            q.prepare("UPDATE participantes SET goles=goles+?, tarjetas_amarillas=tarjetas_amarillas+?, tarjetas_rojas=tarjetas_rojas+? WHERE id=?")
                            q.addBindValue(gs); q.addBindValue(asum); q.addBindValue(rs); q.addBindValue(pid)
                            q.exec()
                            changed = True
                    if i == 0: self.goles_local_sumados = goles_equipo
                    else: self.goles_visit_sumados = goles_equipo
                if changed:
                    QMessageBox.information(dialog, "Éxito", "Estadísticas actualizadas.\nLos goles se han sumado al marcador.")
                    dialog.accept()
                else:
                    QMessageBox.information(dialog, "Info", "No hubo cambios para guardar.")
                    dialog.reject()
            except Exception as e:
                QMessageBox.critical(dialog, "Error", str(e))
                
        btn_guardar.clicked.connect(guardar_stats)
        layout.addWidget(btn_guardar)
        
        resultado = dialog.exec()
        if resultado == QDialog.Accepted:
            return self.goles_local_sumados, self.goles_visit_sumados
        else:
            return 0, 0

    def nueva_temporada(self):
        if QMessageBox.question(self.main_view, "Reiniciar", "¿Borrar TODO?", QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes:
            QSqlQuery().exec("DELETE FROM partidos")
            QSqlQuery().exec("UPDATE participantes SET goles=0, tarjetas_amarillas=0, tarjetas_rojas=0")
            self.asegurar_columnas_bd()
            self.cargar_calendario()
            if self.main_controller: self.main_controller.actualizar_clasificacion()
            QMessageBox.information(self.main_view, "Listo", "Temporada reiniciada.")

    def mostrar_clasificacion(self):
        self.main_view.ui.stackedWidget.setCurrentIndex(2)
        
    def volver_calendario(self):
        self.tree_widget.setVisible(True)
        self.tabla_clasificacion.setVisible(False)
        self.btn_volver.setVisible(False)
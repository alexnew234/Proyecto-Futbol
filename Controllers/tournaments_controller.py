from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from PySide6.QtSql import QSqlQuery
import random
from datetime import datetime, timedelta


class TournamentsController:
    """Controlador para manejar la lógica de torneos, rondas y clasificaciones"""
    
    def __init__(self, main_window):
        self.main_view = main_window
        
    def obtener_equipos(self):
        """Obtiene la lista de todos los equipos creados"""
        query = QSqlQuery()
        query.exec("SELECT id, nombre FROM equipos ORDER BY nombre")
        
        equipos = []
        while query.next():
            equipos.append({
                'id': query.value(0),
                'nombre': query.value(1)
            })
        return equipos
    
    def obtener_ronda_actual(self):
        """Determina qué ronda es la actual basándose en los partidos existentes"""
        query = QSqlQuery()
        # Obtener rondas con partidos completamente jugados, ordenadas de más reciente a más antigua
        query.exec("""
            SELECT ronda 
            FROM partidos 
            WHERE ronda IS NOT NULL
            GROUP BY ronda
            HAVING COUNT(*) = SUM(CASE WHEN jugado = 1 THEN 1 ELSE 0 END)
            ORDER BY CASE ronda
                WHEN 'Final' THEN 4
                WHEN 'Semifinal' THEN 3
                WHEN 'Cuartos' THEN 2
                WHEN 'Octavos' THEN 1
                ELSE 0
            END DESC
            LIMIT 1
        """)
        
        if query.next():
            return query.value(0)
        return None
    
    def contar_equipos_en_ronda(self, ronda):
        """Cuenta cuántos equipos están participando en una ronda"""
        query = QSqlQuery()
        query.prepare("""
            SELECT COUNT(DISTINCT id_equipo_local, id_equipo_visitante) 
            FROM partidos 
            WHERE ronda = ?
        """)
        query.addBindValue(ronda)
        
        if query.exec() and query.next():
            return query.value(0) * 2
        return 0
    
    def obtener_ganadores_ronda(self, ronda):
        """Obtiene los ganadores de una ronda específica"""
        query = QSqlQuery()
        query.prepare("""
            SELECT id_equipo_local, id_equipo_visitante, goles_local, goles_visitante
            FROM partidos
            WHERE ronda = ? AND jugado = 1
        """)
        query.addBindValue(ronda)
        
        ganadores = []
        if query.exec():
            while query.next():
                goles_local = query.value(2)
                goles_visitante = query.value(3)
                
                if goles_local > goles_visitante:
                    ganadores.append(query.value(0))
                elif goles_visitante > goles_local:
                    ganadores.append(query.value(1))
        
        return ganadores
    
    def ronda_completada(self, ronda):
        """Verifica si todos los partidos de una ronda están completados"""
        query = QSqlQuery()
        query.prepare("""
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN jugado = 1 THEN 1 ELSE 0 END) as jugados
            FROM partidos
            WHERE ronda = ?
        """)
        query.addBindValue(ronda)
        
        if query.exec() and query.next():
            total = query.value(0)
            jugados = query.value(1) or 0
            return total > 0 and total == jugados
        return False
    
    def generar_siguiente_ronda(self):
        """Genera la siguiente ronda del torneo"""
        equipos = self.obtener_equipos()
        
        if len(equipos) < 2:
            QMessageBox.warning(
                self.main_view,
                "Error",
                "Se necesitan al menos 2 equipos para generar rondas."
            )
            return False
        
        ronda_actual = self.obtener_ronda_actual()
        
        # Definir la secuencia de rondas
        rondas = ["Octavos", "Cuartos", "Semifinal", "Final"]
        
        # Primer ronda: Octavos (si hay más de 8 equipos)
        if ronda_actual is None:
            if len(equipos) > 8:
                siguiente_ronda = "Octavos"
                equipos_participantes = equipos
            elif len(equipos) > 4:
                siguiente_ronda = "Cuartos"
                equipos_participantes = equipos
            elif len(equipos) > 2:
                siguiente_ronda = "Semifinal"
                equipos_participantes = equipos
            else:
                siguiente_ronda = "Final"
                equipos_participantes = equipos
        else:
            # Verificar que la ronda actual está completamente jugada
            if not self.ronda_completada(ronda_actual):
                QMessageBox.warning(
                    self.main_view,
                    "Error",
                    f"La ronda {ronda_actual} no está completada. Completa todos los partidos primero."
                )
                return False
            
            # Obtener ganadores de la ronda anterior
            ganadores_ids = self.obtener_ganadores_ronda(ronda_actual)
            
            if len(ganadores_ids) == 0:
                QMessageBox.warning(
                    self.main_view,
                    "Error",
                    "No hay ganadores en la ronda actual. Completa los partidos primero."
                )
                return False
            
            if len(ganadores_ids) == 1:
                QMessageBox.information(
                    self.main_view,
                    "Torneo finalizado",
                    f"¡El torneo ha terminado! Ganador: {self.obtener_nombre_equipo(ganadores_ids[0])}"
                )
                return False
            
            # Convertir IDs de ganadores a diccionarios con estructura {'id': ..., 'nombre': ...}
            equipos_participantes = []
            for id_ganador in ganadores_ids:
                equipos_participantes.append({
                    'id': id_ganador,
                    'nombre': self.obtener_nombre_equipo(id_ganador)
                })
            
            idx = rondas.index(ronda_actual) if ronda_actual in rondas else -1
            
            if idx + 1 < len(rondas):
                siguiente_ronda = rondas[idx + 1]
            else:
                QMessageBox.information(
                    self.main_view,
                    "Torneo finalizado",
                    f"¡El torneo ha terminado! Ganador: {self.obtener_nombre_equipo(ganadores_ids[0])}"
                )
                return False
        
        # Generar emparejamientos
        equipos_participantes = equipos_participantes.copy()
        random.shuffle(equipos_participantes)
        
        if len(equipos_participantes) % 2 != 0:
            QMessageBox.warning(
                self.main_view,
                "Error",
                f"Se necesita un número par de equipos. Tienes {len(equipos_participantes)}."
            )
            return False
        
        # Crear partidos
        query = QSqlQuery()
        fecha_inicio = datetime.now()
        
        partidos_creados = 0
        for i in range(0, len(equipos_participantes), 2):
            equipo1 = equipos_participantes[i]
            equipo2 = equipos_participantes[i + 1]
            
            # Incrementar fecha para cada partido
            fecha_partido = fecha_inicio + timedelta(days=i//2)
            
            query.prepare("""
                INSERT INTO partidos 
                (fecha, hora, fase, ronda, id_equipo_local, id_equipo_visitante, jugado)
                VALUES (?, ?, ?, ?, ?, ?, 0)
            """)
            query.addBindValue(fecha_partido.strftime("%Y-%m-%d"))
            query.addBindValue("19:00")
            query.addBindValue("Competición")
            query.addBindValue(siguiente_ronda)
            query.addBindValue(equipo1['id'])
            query.addBindValue(equipo2['id'])
            
            if query.exec():
                partidos_creados += 1
            else:
                print(f"Error creando partido: {query.lastError().text()}")
        
        QMessageBox.information(
            self.main_view,
            "Éxito",
            f"Se han creado {partidos_creados} partidos para la ronda {siguiente_ronda}."
        )
        
        return True
    
    def obtener_nombre_equipo(self, id_equipo):
        """Obtiene el nombre de un equipo por su ID"""
        query = QSqlQuery()
        query.prepare("SELECT nombre FROM equipos WHERE id = ?")
        query.addBindValue(id_equipo)
        
        if query.exec() and query.next():
            return query.value(0)
        return "Desconocido"
    
    def calcular_clasificacion(self):
        """Calcula la tabla de posiciones basada en los partidos jugados"""
        query = QSqlQuery()
        query.exec("SELECT id FROM equipos ORDER BY nombre")
        
        clasificacion = []
        
        while query.next():
            id_equipo = query.value(0)
            nombre_equipo = self.obtener_nombre_equipo(id_equipo)
            
            # Valores por defecto
            jugados = 0
            ganados = 0
            empatados = 0
            perdidos = 0
            goles_favor = 0
            goles_contra = 0
            
            # Verificar si el equipo tiene partidos
            check_query = QSqlQuery()
            check_query.prepare("SELECT COUNT(*) FROM partidos WHERE (id_equipo_local = ? OR id_equipo_visitante = ?) AND jugado = 1")
            check_query.addBindValue(id_equipo)
            check_query.addBindValue(id_equipo)
            check_query.exec()
            check_query.next()
            partidos_totales = check_query.value(0)
            
            # Contar partidos jugados, ganados, empatados, perdidos
            partidos_query = QSqlQuery()
            partidos_query.prepare("""
                SELECT COUNT(CASE WHEN jugado = 1 THEN 1 END) as jugados,
                       SUM(CASE WHEN jugado = 1 AND ((id_equipo_local = ? AND goles_local > goles_visitante) OR 
                                                       (id_equipo_visitante = ? AND goles_visitante > goles_local)) THEN 1 ELSE 0 END) as ganados,
                       SUM(CASE WHEN jugado = 1 AND (id_equipo_local = ? OR id_equipo_visitante = ?) AND goles_local = goles_visitante THEN 1 ELSE 0 END) as empatados,
                       SUM(CASE WHEN jugado = 1 AND ((id_equipo_local = ? AND goles_local < goles_visitante) OR 
                                                       (id_equipo_visitante = ? AND goles_visitante < goles_local)) THEN 1 ELSE 0 END) as perdidos,
                       SUM(CASE WHEN jugado = 1 AND id_equipo_local = ? THEN goles_local 
                                WHEN jugado = 1 AND id_equipo_visitante = ? THEN goles_visitante ELSE 0 END) as goles_favor,
                       SUM(CASE WHEN jugado = 1 AND id_equipo_local = ? THEN goles_visitante 
                                WHEN jugado = 1 AND id_equipo_visitante = ? THEN goles_local ELSE 0 END) as goles_contra
                FROM partidos
                WHERE id_equipo_local = ? OR id_equipo_visitante = ?
            """)
            
            # Orden de parámetros: ganados(2), empatados(4), perdidos(2), favor(2), contra(2) = 12
            partidos_query.addBindValue(id_equipo)  # ganados local
            partidos_query.addBindValue(id_equipo)  # ganados visitante
            partidos_query.addBindValue(id_equipo)  # empatados local
            partidos_query.addBindValue(id_equipo)  # empatados visitante
            partidos_query.addBindValue(id_equipo)  # perdidos local
            partidos_query.addBindValue(id_equipo)  # perdidos visitante
            partidos_query.addBindValue(id_equipo)  # favor local
            partidos_query.addBindValue(id_equipo)  # favor visitante
            partidos_query.addBindValue(id_equipo)  # contra local
            partidos_query.addBindValue(id_equipo)  # contra visitante
            partidos_query.addBindValue(id_equipo)  # WHERE local
            partidos_query.addBindValue(id_equipo)  # WHERE visitante
            
            # Ejecutar y procesar resultado (aunque sea NULL)
            if partidos_query.exec():
                if partidos_query.next():
                    jugados = partidos_query.value(0) or 0
                    ganados = partidos_query.value(1) or 0
                    empatados = partidos_query.value(2) or 0
                    perdidos = partidos_query.value(3) or 0
                    goles_favor = partidos_query.value(4) or 0
                    goles_contra = partidos_query.value(5) or 0
            
            puntos = (ganados * 3) + (empatados * 1)
            diferencia_goles = goles_favor - goles_contra
            
            clasificacion.append({
                'nombre': nombre_equipo,
                'jugados': jugados,
                'ganados': ganados,
                'empatados': empatados,
                'perdidos': perdidos,
                'goles_favor': goles_favor,
                'goles_contra': goles_contra,
                'diferencia': diferencia_goles,
                'puntos': puntos
            })
        
        # Ordenar por puntos y diferencia de goles
        clasificacion.sort(key=lambda x: (x['puntos'], x['diferencia']), reverse=True)
        
        return clasificacion
    
    def mostrar_clasificacion(self, table_widget):
        """Muestra la clasificación en una tabla"""
        from PySide6.QtWidgets import QHeaderView
        
        print("DEBUG: mostrar_clasificacion() INICIADO")
        
        clasificacion = self.calcular_clasificacion()
        
        print(f"DEBUG: calcular_clasificacion() retornó {len(clasificacion)} equipos")
        
        table_widget.setRowCount(len(clasificacion))
        table_widget.setColumnCount(9)
        table_widget.setHorizontalHeaderLabels([
            "Equipo", "J", "G", "E", "P", "GF", "GC", "DG", "Pts"
        ])
        
        for fila, equipo in enumerate(clasificacion):
            table_widget.setItem(fila, 0, QTableWidgetItem(equipo['nombre']))
            table_widget.setItem(fila, 1, QTableWidgetItem(str(equipo['jugados'])))
            table_widget.setItem(fila, 2, QTableWidgetItem(str(equipo['ganados'])))
            table_widget.setItem(fila, 3, QTableWidgetItem(str(equipo['empatados'])))
            table_widget.setItem(fila, 4, QTableWidgetItem(str(equipo['perdidos'])))
            table_widget.setItem(fila, 5, QTableWidgetItem(str(equipo['goles_favor'])))
            table_widget.setItem(fila, 6, QTableWidgetItem(str(equipo['goles_contra'])))
            table_widget.setItem(fila, 7, QTableWidgetItem(str(equipo['diferencia'])))
            table_widget.setItem(fila, 8, QTableWidgetItem(str(equipo['puntos'])))
        
        # Ajustar el tamaño de las columnas
        header = table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, 9):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        
        print("DEBUG: mostrar_clasificacion() COMPLETADO")

import os
import sqlite3
from PySide6.QtSql import QSqlDatabase, QSqlQuery

# --- CONFIGURACIÓN DE RUTA ABSOLUTA ---
USER_DATA_FOLDER = os.path.join(os.path.expanduser("~"), "TorneoFutbolData")

if not os.path.exists(USER_DATA_FOLDER):
    try:
        os.makedirs(USER_DATA_FOLDER)
    except Exception as e:
        print(f"[ERROR CRÍTICO] No se pudo crear carpeta de datos: {e}")

DB_PATH = os.path.join(USER_DATA_FOLDER, "torneo_futbol.db")

def get_db_path():
    """Devuelve la ruta absoluta de la base de datos"""
    return DB_PATH

def inicializar_db():
    """Configura la conexión y crea las tablas"""
    if QSqlDatabase.contains("qt_sql_default_connection"):
        db = QSqlDatabase.database("qt_sql_default_connection")
    else:
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(DB_PATH)
    
    if not db.open():
        print(f"[ERROR] No se pudo conectar a la BD en: {DB_PATH}")
        return False

    print(f"[OK] Base de datos conectada en: {DB_PATH}")

    query = QSqlQuery()
    
    # TABLA EQUIPOS
    query.exec("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            curso TEXT,
            color_camiseta TEXT,
            ruta_escudo TEXT
        )
    """)

    # TABLA PARTICIPANTES
    query.exec("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha_nacimiento TEXT,
            curso TEXT,
            tipo_participante TEXT,
            posicion TEXT,
            tarjetas_amarillas INTEGER DEFAULT 0,
            tarjetas_rojas INTEGER DEFAULT 0,
            goles INTEGER DEFAULT 0,
            id_equipo INTEGER,
            FOREIGN KEY(id_equipo) REFERENCES equipos(id)
        )
    """)
    
    # TABLA PARTIDOS (ACTUALIZADA CON ÁRBITRO)
    # Si la tabla ya existe, SQLite no añade la columna mágicamente con este comando.
    # Truco: Borraremos la tabla antigua si no tiene la columna (manualmente o reiniciando la DB).
    query.exec("""
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fase TEXT,
            equipo_local_id INTEGER,
            equipo_visitante_id INTEGER,
            goles_local INTEGER DEFAULT 0,
            goles_visitante INTEGER DEFAULT 0,
            jugado INTEGER DEFAULT 0,
            hora TEXT,
            id_arbitro INTEGER,  -- <--- NUEVO CAMPO
            FOREIGN KEY(id_arbitro) REFERENCES participantes(id)
        )
    """)
    
    return True
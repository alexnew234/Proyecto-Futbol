import sys
import os
from PySide6.QtSql import QSqlDatabase, QSqlQuery

def conectar():
    """
    Realiza la conexión a la BBDD y crea el archivo si no existe.
    Según el PDF, activamos Foreign Keys y creamos tablas.
    """
    # Calculamos la ruta absoluta para que funcione en cualquier ordenador
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "torneoFutbol_sqlite.db")

    # Configuración del driver QSQLITE [cite: 5, 34]
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path)

    if not db.open():
        print("Error: No se pudo conectar a la base de datos.")
        return False
    
    print(f"BBDD conectada en: {db_path}") # [cite: 10]

    # Activar Claves Foráneas (Importante según PDF) [cite: 14, 40]
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON;")

    # Crear las tablas
    crear_tablas(query)
    
    return True

def crear_tablas(query):
    """ Crea las tablas necesarias si no existen """
    
    # 1. Tabla EQUIPOS (Necesaria primero por las relaciones)
    query.exec("""
    CREATE TABLE IF NOT EXISTS equipos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        curso TEXT,
        color_camiseta TEXT,
        ruta_escudo TEXT
    )
    """)

    # 2. Tabla PARTICIPANTES (Basada en el PDF + relación equipo) [cite: 17-27]
    query.exec("""
    CREATE TABLE IF NOT EXISTS participantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        fecha_nacimiento TEXT,
        curso TEXT,
        tipo_participante TEXT NOT NULL,
        posicion TEXT,
        t_amarillas INTEGER DEFAULT 0,
        t_rojas INTEGER DEFAULT 0,
        goles INTEGER DEFAULT 0,
        id_equipo INTEGER,
        FOREIGN KEY (id_equipo) REFERENCES equipos(id) ON DELETE SET NULL
    )
    """)

    # 3. Tabla PARTIDOS
    query.exec("""
    CREATE TABLE IF NOT EXISTS partidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha TEXT,
        hora TEXT,
        fase TEXT,
        ronda TEXT,
        id_equipo_local INTEGER,
        id_equipo_visitante INTEGER,
        goles_local INTEGER DEFAULT 0,
        goles_visitante INTEGER DEFAULT 0,
        id_arbitro INTEGER,
        jugado BOOLEAN DEFAULT 0,
        FOREIGN KEY (id_equipo_local) REFERENCES equipos(id),
        FOREIGN KEY (id_equipo_visitante) REFERENCES equipos(id)
    )
    """)
    
    # Agregar columna 'ronda' si no existe (para migraciones de BD existentes)
    check_query = QSqlQuery()
    check_query.exec("PRAGMA table_info(partidos)")
    campos = []
    while check_query.next():
        campos.append(check_query.value(1))
    
    if 'ronda' not in campos:
        query.exec("ALTER TABLE partidos ADD COLUMN ronda TEXT")
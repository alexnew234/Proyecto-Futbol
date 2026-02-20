#!/usr/bin/env python
"""
Prueba rapida de estructura de base de datos para el proyecto.
"""

import sqlite3
import sys
from pathlib import Path

from torneo_db.database import get_db_path, inicializar_db

REQUIRED_TABLES = {
    'equipos',
    'participantes',
    'partidos',
}

REQUIRED_COLUMNS = {
    'equipos': {'id', 'nombre'},
    'participantes': {'id', 'nombre', 'id_equipo', 'goles', 'tarjetas_amarillas', 'tarjetas_rojas'},
    'partidos': {
        'id',
        'fase',
        'equipo_local_id',
        'equipo_visitante_id',
        'goles_local',
        'goles_visitante',
        'jugado',
    },
}


def fetch_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return {row[1] for row in rows}


def test_database_structure() -> bool:
    print('\n' + '=' * 60)
    print('PRUEBA DE ESTRUCTURA DE BASE DE DATOS')
    print('=' * 60)

    if not inicializar_db():
        print('[ERROR] No se pudo inicializar la base de datos.')
        return False

    db_path = Path(get_db_path())
    print(f'[OK] Base de datos: {db_path}')

    if not db_path.exists():
        print(f'[ERROR] No existe el archivo de BD: {db_path}')
        return False

    conn = sqlite3.connect(db_path)
    try:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        }

        missing_tables = REQUIRED_TABLES - tables
        if missing_tables:
            print(f'[ERROR] Faltan tablas: {sorted(missing_tables)}')
            return False

        for table, expected_cols in REQUIRED_COLUMNS.items():
            cols = fetch_columns(conn, table)
            missing_cols = expected_cols - cols
            if missing_cols:
                print(f'[ERROR] Tabla {table}: faltan columnas {sorted(missing_cols)}')
                return False

        print('[OK] Estructura de base de datos valida.')
        return True
    finally:
        conn.close()


def main() -> int:
    success = test_database_structure()
    if success:
        print('\nTODAS LAS PRUEBAS PASARON')
        return 0

    print('\nLAS PRUEBAS FALLARON')
    return 1


if __name__ == '__main__':
    sys.exit(main())

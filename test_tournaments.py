#!/usr/bin/env python
"""
Script de prueba para verificar que el sistema de torneos funciona correctamente
"""
import sys
<<<<<<< Updated upstream
=======
from pathlib import Path
import pytest
>>>>>>> Stashed changes
from PySide6.QtWidgets import QApplication
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from Models.database import conectar

def test_database_structure():
    """Verifica la estructura de la base de datos"""
    print("\n" + "="*60)
    print("PRUEBA DE ESTRUCTURA DE BASE DE DATOS")
    print("="*60)
    
    # Conectar a la base de datos
    conectar()
    
    # Verificar tabla partidos
    query = QSqlQuery()
    query.exec('PRAGMA table_info(partidos)')
    
    campos = {}
    while query.next():
        campos[query.value(1)] = query.value(2)
    
    print("\n📋 Campos de la tabla 'partidos':")
    for campo, tipo in campos.items():
        print(f"   - {campo}: {tipo}")
    
    # Verificar campo ronda
    if 'ronda' in campos:
        print("\n✓ Campo 'ronda' presente correctamente")
    else:
        print("\n✗ Error: Campo 'ronda' no encontrado")
        return False
<<<<<<< Updated upstream
    
    print("\n✓ Estructura de base de datos válida")
    return True
=======
    return columna in _fetch_columns(tabla)


@pytest.fixture(scope="session", autouse=True)
def _qt_app():
    app = QApplication.instance() or QApplication(sys.argv)
    yield app


def test_db_schema() -> None:
    print("\n" + "=" * 60)
    print("PRUEBA GLOBAL DE BASE DE DATOS")
    print("=" * 60)

    assert inicializar_db(), "\n[ERROR] No se pudo inicializar la BD."

    db_path = get_db_path()
    assert Path(db_path).exists(), f"\n[ERROR] No se encontro la BD en: {db_path}"
    print(f"\n[OK] BD en: {db_path}")

    # Tablas esperadas
    tablas = {"equipos", "participantes", "partidos"}
    q = QSqlQuery()
    q.exec("SELECT name FROM sqlite_master WHERE type='table'")
    existentes = set()
    while q.next():
        existentes.add(q.value(0))

    faltan = tablas - existentes
    assert not faltan, f"\n[ERROR] Faltan tablas: {', '.join(sorted(faltan))}"

    # Columnas esperadas
    req_equipos = {"id", "nombre", "curso", "color_camiseta", "ruta_escudo"}
    req_participantes = {
        "id",
        "nombre",
        "fecha_nacimiento",
        "curso",
        "tipo_participante",
        "posicion",
        "tarjetas_amarillas",
        "tarjetas_rojas",
        "goles",
        "id_equipo",
    }
    req_partidos = {
        "id",
        "fase",
        "equipo_local_id",
        "equipo_visitante_id",
        "goles_local",
        "goles_visitante",
        "jugado",
        "hora",
        "id_arbitro",
        "fecha",
    }

    col_equipos = _fetch_columns("equipos")
    col_participantes = _fetch_columns("participantes")

    assert req_equipos.issubset(col_equipos), (
        "\n[ERROR] Esquema de 'equipos' incompleto. "
        f"Faltan: {req_equipos - col_equipos}"
    )

    assert req_participantes.issubset(col_participantes), (
        "\n[ERROR] Esquema de 'participantes' incompleto. "
        f"Faltan: {req_participantes - col_participantes}"
    )

    # La app agrega 'fecha' en runtime si no existe; lo garantizamos aqui.
    assert _ensure_column("partidos", "fecha", "TEXT"), (
        "\n[ERROR] No se pudo garantizar la columna 'fecha' en 'partidos'."
    )

    col_partidos = _fetch_columns("partidos")
    assert req_partidos.issubset(col_partidos), (
        "\n[ERROR] Esquema de 'partidos' incompleto. "
        f"Faltan: {req_partidos - col_partidos}"
    )

    print("\n[OK] Esquema de BD valido.")
>>>>>>> Stashed changes

def main():
    # Crear aplicación
    app = QApplication(sys.argv)
<<<<<<< Updated upstream
    
    # Ejecutar pruebas
    success = test_database_structure()
    
    if success:
        print("\n" + "="*60)
        print("TODAS LAS PRUEBAS PASARON ✓")
        print("="*60)
        print("\nLa aplicación está lista para usar")
        print("\nFuncionalidades disponibles:")
        print("  1. Generar Siguiente Ronda (botón verde en Calendario)")
        print("  2. Ver Clasificación (botón azul en Calendario)")
        print("  3. Rondas soportadas: Octavos, Cuartos, Semifinal, Final")
        print("="*60 + "\n")
    else:
        print("\n✗ Las pruebas fallaron")
        sys.exit(1)
=======
    try:
        test_db_schema()
        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS PASARON")
        print("=" * 60)
        return 0
    except AssertionError as exc:
        print(f"\n[FAIL] Las pruebas fallaron. {exc}")
        return 1

>>>>>>> Stashed changes

if __name__ == "__main__":
    main()

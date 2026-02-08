#!/usr/bin/env python
"""
Prueba global basica del proyecto (BD + esquema principal).
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtSql import QSqlQuery

# Asegurar que la libreria local se encuentre aunque no este instalada con pip -e
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "torneofutbol_db"))

try:
    from torneo_db.database import inicializar_db, get_db_path
except Exception as exc:
    print("[ERROR] No se pudo importar 'torneo_db'.", exc)
    sys.exit(1)


def _fetch_columns(tabla: str) -> set[str]:
    columnas = set()
    q = QSqlQuery()
    q.exec(f"PRAGMA table_info({tabla})")
    while q.next():
        columnas.add(q.value(1))
    return columnas


def _ensure_column(tabla: str, columna: str, tipo: str) -> bool:
    columnas = _fetch_columns(tabla)
    if columna in columnas:
        return True
    q = QSqlQuery()
    ok = q.exec(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")
    if not ok:
        return False
    return columna in _fetch_columns(tabla)


def test_db_schema() -> bool:
    print("\n" + "=" * 60)
    print("PRUEBA GLOBAL DE BASE DE DATOS")
    print("=" * 60)

    if not inicializar_db():
        print("\n[ERROR] No se pudo inicializar la BD.")
        return False

    db_path = get_db_path()
    if not Path(db_path).exists():
        print(f"\n[ERROR] No se encontro la BD en: {db_path}")
        return False
    print(f"\n[OK] BD en: {db_path}")

    # Tablas esperadas
    tablas = {"equipos", "participantes", "partidos"}
    q = QSqlQuery()
    q.exec("SELECT name FROM sqlite_master WHERE type='table'")
    existentes = set()
    while q.next():
        existentes.add(q.value(0))

    faltan = tablas - existentes
    if faltan:
        print(f"\n[ERROR] Faltan tablas: {', '.join(sorted(faltan))}")
        return False

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

    if not req_equipos.issubset(col_equipos):
        print("\n[ERROR] Esquema de 'equipos' incompleto.")
        print("Faltan:", req_equipos - col_equipos)
        return False

    if not req_participantes.issubset(col_participantes):
        print("\n[ERROR] Esquema de 'participantes' incompleto.")
        print("Faltan:", req_participantes - col_participantes)
        return False

    # La app agrega 'fecha' en runtime si no existe; lo garantizamos aqui.
    if not _ensure_column("partidos", "fecha", "TEXT"):
        print("\n[ERROR] No se pudo garantizar la columna 'fecha' en 'partidos'.")
        return False

    col_partidos = _fetch_columns("partidos")
    if not req_partidos.issubset(col_partidos):
        print("\n[ERROR] Esquema de 'partidos' incompleto.")
        print("Faltan:", req_partidos - col_partidos)
        return False

    print("\n[OK] Esquema de BD valido.")
    return True


def main() -> int:
    app = QApplication(sys.argv)
    ok = test_db_schema()
    if ok:
        print("\n" + "=" * 60)
        print("TODAS LAS PRUEBAS PASARON")
        print("=" * 60)
        return 0
    print("\n[FAIL] Las pruebas fallaron.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

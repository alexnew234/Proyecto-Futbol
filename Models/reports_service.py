import csv
import glob
import html
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QMarginsF, Qt
from PySide6.QtGui import QImage, QPageLayout, QPageSize, QTextDocument
from PySide6.QtPrintSupport import QPrinter

try:
    from torneo_db.database import get_db_path
except Exception:
    def get_db_path():
        return os.path.join(os.path.expanduser("~"), "TorneoFutbolData", "torneo_futbol.db")


class ReportsService:
    REPORTS = {
        "equipos_jugadores": {
            "template": "informe_equipos_jugadores.jrxml",
            "prefix": "informe_equipos_jugadores",
            "title": "Informe Equipos y Jugadores",
        },
        "partidos_resultados": {
            "template": "informe_partidos_resultados.jrxml",
            "prefix": "informe_partidos_resultados",
            "title": "Informe Partidos y Resultados",
        },
        "clasificacion_eliminatorias": {
            "template": "informe_clasificacion_eliminatorias.jrxml",
            "prefix": "informe_clasificacion_eliminatorias",
            "title": "Informe Clasificacion y Eliminatorias",
        },
    }

    def __init__(self):
        self.root = Path(__file__).resolve().parent.parent
        self.reports_dir = self.root / "reports"
        # Requisito de entrega: mantener los JRXML en la carpeta reports.
        self.templates_dir = self.reports_dir
        # Compatibilidad con versiones anteriores donde estaban en reports/templates.
        self.legacy_templates_dir = self.reports_dir / "templates"
        self.lib_dir = self.reports_dir / "lib"
        self.logo_path = self.root / "Resources" / "img" / "logo_rfef.jpg"
        self.torneo_nombre = "Gestor de Torneos de Futbol"
        self._ensure_dirs()
        self._ensure_templates_in_reports_root()

    def _ensure_dirs(self):
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.legacy_templates_dir.mkdir(parents=True, exist_ok=True)
        self.lib_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_templates_in_reports_root(self):
        for cfg in self.REPORTS.values():
            name = cfg["template"]
            root_tpl = self.reports_dir / name
            legacy_tpl = self.legacy_templates_dir / name
            if root_tpl.exists():
                continue
            if legacy_tpl.exists():
                try:
                    shutil.copy2(legacy_tpl, root_tpl)
                except Exception:
                    pass

    def _resolve_template_path(self, report_key):
        name = self.REPORTS[report_key]["template"]
        root_tpl = self.reports_dir / name
        if root_tpl.exists():
            return root_tpl
        legacy_tpl = self.legacy_templates_dir / name
        if legacy_tpl.exists():
            return legacy_tpl
        return root_tpl

    def _legacy_template_path(self, report_key):
        return self.legacy_templates_dir / self.REPORTS[report_key]["template"]

    def get_default_output_dir(self):
        return str(self.reports_dir)

    def _db_path(self):
        db = Path(get_db_path())
        db.parent.mkdir(parents=True, exist_ok=True)
        return str(db)

    def _connect(self):
        con = sqlite3.connect(self._db_path())
        con.row_factory = sqlite3.Row
        return con

    def list_equipos(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute("SELECT nombre FROM equipos ORDER BY nombre")
            return [r[0] for r in cur.fetchall()]
        finally:
            con.close()

    def list_fases(self):
        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(
                """
                SELECT DISTINCT fase
                FROM partidos
                WHERE fase IS NOT NULL AND trim(fase) <> ''
                ORDER BY CASE fase
                    WHEN 'Octavos' THEN 1
                    WHEN 'Cuartos' THEN 2
                    WHEN 'Semifinal' THEN 3
                    WHEN 'Final' THEN 4
                    ELSE 5
                END
                """
            )
            return [r[0] for r in cur.fetchall()]
        finally:
            con.close()

    def generate_report(self, report_key, filters, output_dir="", export_csv=False, force_native=False):
        if report_key not in self.REPORTS:
            raise ValueError(f"Tipo de informe no soportado: {report_key}")

        self._ensure_dirs()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = self.reports_dir / f"{self.REPORTS[report_key]['prefix']}_{stamp}"
        pdf_path = base.with_suffix(".pdf")
        csv_path = base.with_suffix(".csv")
        jasper_path = base.with_suffix(".jasper")
        jrxml = self._resolve_template_path(report_key)

        result = {
            "report_key": report_key,
            "engine": "",
            "pdf_path": str(pdf_path),
            "csv_path": "",
            "jasper_path": "",
            "jrxml_path": str(jrxml),
            "internal_pdf_path": str(pdf_path),
            "internal_csv_path": "",
            "warnings": [],
        }

        data = None
        generated_jasper = False

        if not force_native:
            try:
                self._generate_with_jasper(report_key, filters, jrxml, base)
                generated_jasper = True
                result["engine"] = "Jasper"
            except Exception as exc:
                # Si el JRXML de reports/ fue guardado en formato incompatible, intentamos la copia estable.
                legacy_jrxml = self._legacy_template_path(report_key)
                tried_legacy = False
                if legacy_jrxml.exists() and legacy_jrxml.resolve() != Path(jrxml).resolve():
                    tried_legacy = True
                    try:
                        self._generate_with_jasper(report_key, filters, legacy_jrxml, base)
                        generated_jasper = True
                        result["engine"] = "Jasper"
                        result["jrxml_path"] = str(legacy_jrxml)
                        result["warnings"].append(
                            "El JRXML principal no fue compatible; se uso la copia de seguridad en reports/templates."
                        )
                    except Exception as legacy_exc:
                        result["warnings"].append(f"Jasper no disponible (plantilla principal): {exc}")
                        result["warnings"].append(f"Jasper no disponible (copia seguridad): {legacy_exc}")

                if not generated_jasper and not tried_legacy:
                    result["warnings"].append(f"Jasper no disponible: {exc}")

        if not generated_jasper:
            data = self._fetch_data(report_key, filters)
            self._generate_native_pdf(report_key, data, filters, str(pdf_path))
            result["engine"] = "Nativo"

        if export_csv:
            if data is None:
                data = self._fetch_data(report_key, filters)
            self._write_csv(report_key, data, str(csv_path))
            result["csv_path"] = str(csv_path)
            result["internal_csv_path"] = str(csv_path)

        if generated_jasper and jasper_path.exists():
            result["jasper_path"] = str(jasper_path)

        dest = Path(output_dir).resolve() if output_dir else self.reports_dir.resolve()
        if dest != self.reports_dir.resolve():
            dest.mkdir(parents=True, exist_ok=True)
            moved_pdf = dest / pdf_path.name
            shutil.copy2(pdf_path, moved_pdf)
            result["pdf_path"] = str(moved_pdf)
            if result["csv_path"]:
                moved_csv = dest / csv_path.name
                shutil.copy2(csv_path, moved_csv)
                result["csv_path"] = str(moved_csv)

        return result

    def _generate_with_jasper(self, report_key, filters, jrxml_path, output_base):
        if not jrxml_path.exists():
            raise FileNotFoundError(f"No se encontro la plantilla JRXML: {jrxml_path}")

        self._ensure_java_home()
        jdbc_jar = self._ensure_sqlite_jdbc_jar()

        from pyreportjasper import PyReportJasper

        rpt = PyReportJasper()
        rpt.config(
            input_file=str(jrxml_path),
            output_file=str(output_base),
            output_formats=["pdf"],
            parameters=self._jasper_params(report_key, filters),
            db_connection={
                "driver": "generic",
                "jdbc_driver": "org.sqlite.JDBC",
                "jdbc_url": f"jdbc:sqlite:{self._db_path()}",
                "jdbc_dir": jdbc_jar,
                "username": "",
                "password": "",
            },
            locale="es_ES",
        )
        rpt.compile(write_jasper=True)
        rpt.process_report()

        if not output_base.with_suffix(".pdf").exists():
            raise RuntimeError("Jasper no genero el PDF")

    def _jasper_params(self, report_key, filters):
        return {
            "P_TORNEO_NOMBRE": self.torneo_nombre,
            "P_GENERADO": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "P_LOGO_PATH": str(self.logo_path.resolve()) if self.logo_path.exists() else "",
            "P_EQUIPO": (filters.get("equipo") or "").strip(),
            "P_ELIMINATORIA": (filters.get("eliminatoria") or "").strip(),
            "P_JUGADOR_DESTACADO": (filters.get("jugador_destacado") or "").strip(),
            "P_FECHA_DESDE": (filters.get("fecha_desde") or "").strip(),
            "P_FECHA_HASTA": (filters.get("fecha_hasta") or "").strip(),
            "P_TIPO_INFORME": report_key,
        }

    def _ensure_java_home(self):
        home = os.environ.get("JAVA_HOME", "").strip()
        if home and Path(home, "bin", "server", "jvm.dll").exists():
            return

        candidates = [
            Path("C:/JAVA"),
            Path("C:/Program Files/Java"),
            Path("C:/Program Files/Eclipse Adoptium"),
            Path("C:/Program Files/Amazon Corretto"),
        ]
        for base in candidates:
            direct = base / "bin" / "server" / "jvm.dll"
            if direct.exists():
                os.environ["JAVA_HOME"] = str(base)
                return
            if base.exists():
                for jvm in base.glob("**/bin/server/jvm.dll"):
                    os.environ["JAVA_HOME"] = str(jvm.parents[2])
                    return

        try:
            proc = subprocess.run(
                ["java", "-XshowSettings:properties", "-version"],
                capture_output=True,
                text=True,
                check=False,
            )
            output = (proc.stdout or "") + "\n" + (proc.stderr or "")
            for line in output.splitlines():
                if "java.home" in line and "=" in line:
                    candidate = line.split("=", 1)[1].strip()
                    if Path(candidate, "bin", "server", "jvm.dll").exists():
                        os.environ["JAVA_HOME"] = candidate
                        return
        except Exception:
            pass

        raise RuntimeError("JAVA_HOME no configurado (sin jvm.dll).")

    def _ensure_sqlite_jdbc_jar(self):
        env_jar = os.environ.get("SQLITE_JDBC_JAR", "").strip()
        if env_jar and Path(env_jar).exists():
            return env_jar

        local = sorted(self.lib_dir.glob("sqlite-jdbc*.jar"), key=lambda p: p.stat().st_mtime, reverse=True)
        if local:
            return str(local[0])

        home = Path.home()
        patterns = [
            str(home / "Downloads" / "sqlite-jdbc*.jar"),
            str(home / ".m2" / "repository" / "org" / "xerial" / "sqlite-jdbc" / "*" / "sqlite-jdbc*.jar"),
            str(home / ".gradle" / "caches" / "modules-2" / "files-2.1" / "org.xerial" / "sqlite-jdbc" / "*" / "*" / "sqlite-jdbc*.jar"),
        ]
        found = []
        for pattern in patterns:
            found.extend([Path(p) for p in glob.glob(pattern) if Path(p).is_file()])

        if not found:
            raise RuntimeError("No se encontro sqlite-jdbc.jar (ponlo en reports/lib).")

        found.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        source = found[0]
        target = self.lib_dir / source.name
        try:
            shutil.copy2(source, target)
            return str(target)
        except Exception:
            return str(source)
    def _fetch_data(self, report_key, filters):
        if report_key == "equipos_jugadores":
            return self._data_equipos_jugadores(filters)
        if report_key == "partidos_resultados":
            return self._data_partidos_resultados(filters)
        if report_key == "clasificacion_eliminatorias":
            return self._data_clasificacion_eliminatorias(filters)
        raise ValueError(f"No hay loader para {report_key}")

    def _data_equipos_jugadores(self, filters):
        equipo_filter = (filters.get("equipo") or "").strip()
        jugador_filter = (filters.get("jugador_destacado") or "").strip()
        fecha_desde = (filters.get("fecha_desde") or "").strip()
        fecha_hasta = (filters.get("fecha_hasta") or "").strip()
        like_jugador = f"%{jugador_filter}%"

        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(
                """
                SELECT e.id, e.nombre
                FROM equipos e
                WHERE (? = '' OR e.nombre = ?)
                  AND (
                    (? = '' AND ? = '')
                    OR EXISTS (
                        SELECT 1
                        FROM partidos p
                        WHERE (p.equipo_local_id = e.id OR p.equipo_visitante_id = e.id)
                          AND (? = '' OR COALESCE(p.fecha, '') >= ?)
                          AND (? = '' OR COALESCE(p.fecha, '') <= ?)
                    )
                  )
                ORDER BY e.nombre ASC
                """,
                (
                    equipo_filter,
                    equipo_filter,
                    fecha_desde,
                    fecha_hasta,
                    fecha_desde,
                    fecha_desde,
                    fecha_hasta,
                    fecha_hasta,
                ),
            )
            equipos = cur.fetchall()

            rows = []
            teams = []

            for eq in equipos:
                cur.execute(
                    """
                    SELECT nombre, COALESCE(posicion, '-') AS posicion,
                           COALESCE(goles, 0) AS goles,
                           COALESCE(tarjetas_amarillas, 0) AS amarillas,
                           COALESCE(tarjetas_rojas, 0) AS rojas
                    FROM participantes
                    WHERE id_equipo = ?
                      AND (tipo_participante LIKE '%Jugador%' OR tipo_participante = 'Ambos')
                      AND (? = '' OR nombre LIKE ?)
                    ORDER BY nombre ASC
                    """,
                    (eq["id"], jugador_filter, like_jugador),
                )
                players_db = cur.fetchall()

                if players_db:
                    total_g = sum(int(p["goles"] or 0) for p in players_db)
                    total_a = sum(int(p["amarillas"] or 0) for p in players_db)
                    total_r = sum(int(p["rojas"] or 0) for p in players_db)
                    avg_g = round(total_g / len(players_db), 2)
                    max_g = max(int(p["goles"] or 0) for p in players_db)
                    max_t = max(int(p["amarillas"] or 0) + int(p["rojas"] or 0) for p in players_db)
                else:
                    total_g = total_a = total_r = 0
                    avg_g = 0.0
                    max_g = max_t = 0

                team_rows = []
                if players_db:
                    for p in players_db:
                        goles = int(p["goles"] or 0)
                        amarillas = int(p["amarillas"] or 0)
                        rojas = int(p["rojas"] or 0)
                        tarjetas = amarillas + rojas
                        row = {
                            "equipo": eq["nombre"],
                            "jugador": p["nombre"],
                            "posicion": p["posicion"] or "-",
                            "goles": goles,
                            "amarillas": amarillas,
                            "rojas": rojas,
                            "top_goles": "SI" if max_g > 0 and goles == max_g else "",
                            "top_tarjetas": "SI" if max_t > 0 and tarjetas == max_t else "",
                            "total_goles_equipo": total_g,
                            "total_amarillas_equipo": total_a,
                            "total_rojas_equipo": total_r,
                            "promedio_goles_equipo": avg_g,
                        }
                        rows.append(row)
                        team_rows.append(row)
                else:
                    row = {
                        "equipo": eq["nombre"],
                        "jugador": "(Sin jugadores)",
                        "posicion": "-",
                        "goles": 0,
                        "amarillas": 0,
                        "rojas": 0,
                        "top_goles": "",
                        "top_tarjetas": "",
                        "total_goles_equipo": 0,
                        "total_amarillas_equipo": 0,
                        "total_rojas_equipo": 0,
                        "promedio_goles_equipo": 0.0,
                    }
                    rows.append(row)
                    team_rows.append(row)

                teams.append(
                    {
                        "equipo": eq["nombre"],
                        "total_goles": total_g,
                        "total_amarillas": total_a,
                        "total_rojas": total_r,
                        "promedio_goles": avg_g,
                        "jugadores": team_rows,
                    }
                )

            return {
                "rows": rows,
                "teams": teams,
                "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        finally:
            con.close()

    def _data_partidos_resultados(self, filters):
        fase_filter = (filters.get("eliminatoria") or "").strip()
        fecha_desde = (filters.get("fecha_desde") or "").strip()
        fecha_hasta = (filters.get("fecha_hasta") or "").strip()

        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute(
                """
                SELECT p.id, p.fase, p.equipo_local_id, p.equipo_visitante_id,
                       e1.nombre AS equipo_local, e2.nombre AS equipo_visitante,
                       COALESCE(a.nombre, 'Sin arbitro') AS arbitro,
                       COALESCE(p.fecha, '') AS fecha,
                       COALESCE(p.hora, '') AS hora,
                       COALESCE(p.jugado, 0) AS jugado,
                       COALESCE(p.goles_local, 0) AS goles_local,
                       COALESCE(p.goles_visitante, 0) AS goles_visitante
                FROM partidos p
                JOIN equipos e1 ON e1.id = p.equipo_local_id
                JOIN equipos e2 ON e2.id = p.equipo_visitante_id
                LEFT JOIN participantes a ON a.id = p.id_arbitro
                WHERE (? = '' OR p.fase = ?)
                  AND (? = '' OR COALESCE(p.fecha, '') >= ?)
                  AND (? = '' OR COALESCE(p.fecha, '') <= ?)
                ORDER BY CASE p.fase
                    WHEN 'Octavos' THEN 1
                    WHEN 'Cuartos' THEN 2
                    WHEN 'Semifinal' THEN 3
                    WHEN 'Final' THEN 4
                    ELSE 5 END,
                    COALESCE(p.fecha, '9999-12-31') ASC,
                    COALESCE(p.hora, '23:59') ASC,
                    p.id ASC
                """,
                (fase_filter, fase_filter, fecha_desde, fecha_desde, fecha_hasta, fecha_hasta),
            )

            history = {}
            rows = []
            pending = 0

            for m in cur.fetchall():
                key = tuple(sorted((m["equipo_local_id"], m["equipo_visitante_id"])))
                prev = history.get(key, {"jugados": 0, "empates": 0, "wins": {}, "detalles": []})
                gl_prev = prev["wins"].get(m["equipo_local_id"], 0)
                gv_prev = prev["wins"].get(m["equipo_visitante_id"], 0)
                resumen = f"{prev['jugados']} previos ({gl_prev}G-{prev['empates']}E-{gv_prev}G)"
                ultimos = " | ".join(prev["detalles"][-5:]) if prev["detalles"] else "Sin historial"
                hist = f"{resumen}: {ultimos}"

                jugado = int(m["jugado"] or 0) == 1
                res = f"{int(m['goles_local'])} - {int(m['goles_visitante'])}" if jugado else "[PENDIENTE]"
                estado = "Jugado" if jugado else "Pendiente"

                rows.append(
                    {
                        "id": int(m["id"]),
                        "fase": m["fase"] or "",
                        "fecha": m["fecha"] or "",
                        "hora": m["hora"] or "",
                        "equipo_local": m["equipo_local"],
                        "equipo_visitante": m["equipo_visitante"],
                        "arbitro": m["arbitro"],
                        "resultado": res,
                        "estado": estado,
                        "historial": hist,
                    }
                )

                if jugado:
                    prev = history.setdefault(key, {"jugados": 0, "empates": 0, "wins": {}, "detalles": []})
                    prev["jugados"] += 1
                    gl = int(m["goles_local"] or 0)
                    gv = int(m["goles_visitante"] or 0)
                    if gl > gv:
                        prev["wins"][m["equipo_local_id"]] = prev["wins"].get(m["equipo_local_id"], 0) + 1
                    elif gv > gl:
                        prev["wins"][m["equipo_visitante_id"]] = prev["wins"].get(m["equipo_visitante_id"], 0) + 1
                    else:
                        prev["empates"] += 1

                    fecha_txt = (m["fecha"] or "").strip() or "s/f"
                    detalle = f"{fecha_txt} {m['equipo_local']} {gl}-{gv} {m['equipo_visitante']}"
                    prev["detalles"].append(detalle)
                else:
                    pending += 1

            return {
                "rows": rows,
                "pending_count": pending,
                "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        finally:
            con.close()
    def _data_clasificacion_eliminatorias(self, filters):
        fase_filter = (filters.get("eliminatoria") or "").strip()
        fecha_desde = (filters.get("fecha_desde") or "").strip()
        fecha_hasta = (filters.get("fecha_hasta") or "").strip()

        con = self._connect()
        try:
            cur = con.cursor()
            cur.execute("SELECT id, nombre FROM equipos ORDER BY nombre")
            equipos = cur.fetchall()

            cur.execute(
                """
                SELECT p.id, p.fase, p.equipo_local_id, p.equipo_visitante_id,
                       e1.nombre AS local_nombre, e2.nombre AS visitante_nombre,
                       COALESCE(p.goles_local, 0) AS goles_local,
                       COALESCE(p.goles_visitante, 0) AS goles_visitante,
                       COALESCE(p.jugado, 0) AS jugado
                FROM partidos p
                JOIN equipos e1 ON e1.id = p.equipo_local_id
                JOIN equipos e2 ON e2.id = p.equipo_visitante_id
                WHERE (? = '' OR p.fase = ?)
                  AND (? = '' OR COALESCE(p.fecha, '') >= ?)
                  AND (? = '' OR COALESCE(p.fecha, '') <= ?)
                ORDER BY CASE p.fase
                    WHEN 'Octavos' THEN 1
                    WHEN 'Cuartos' THEN 2
                    WHEN 'Semifinal' THEN 3
                    WHEN 'Final' THEN 4
                    ELSE 5 END,
                    p.id ASC
                """,
                (fase_filter, fase_filter, fecha_desde, fecha_desde, fecha_hasta, fecha_hasta),
            )
            matches = cur.fetchall()

            stats = {
                int(eq["id"]): {
                    "equipo": eq["nombre"],
                    "pj": 0,
                    "g": 0,
                    "e": 0,
                    "p": 0,
                    "gf": 0,
                    "gc": 0,
                }
                for eq in equipos
            }

            played = [m for m in matches if int(m["jugado"] or 0) == 1]
            goals_phase = {}

            for m in played:
                local_id = int(m["equipo_local_id"])
                visit_id = int(m["equipo_visitante_id"])
                gl = int(m["goles_local"] or 0)
                gv = int(m["goles_visitante"] or 0)
                fase = m["fase"] or ""

                goals_phase[fase] = goals_phase.get(fase, 0) + gl + gv

                stats[local_id]["pj"] += 1
                stats[local_id]["gf"] += gl
                stats[local_id]["gc"] += gv
                stats[visit_id]["pj"] += 1
                stats[visit_id]["gf"] += gv
                stats[visit_id]["gc"] += gl

                if gl > gv:
                    stats[local_id]["g"] += 1
                    stats[visit_id]["p"] += 1
                elif gv > gl:
                    stats[visit_id]["g"] += 1
                    stats[local_id]["p"] += 1
                else:
                    stats[local_id]["e"] += 1
                    stats[visit_id]["e"] += 1

            ranking = []
            for team_id, v in stats.items():
                dg = v["gf"] - v["gc"]
                pts = v["g"] * 3 + v["e"]
                ranking.append(
                    {
                        "team_id": team_id,
                        "equipo": v["equipo"],
                        "pj": v["pj"],
                        "g": v["g"],
                        "e": v["e"],
                        "p": v["p"],
                        "gf": v["gf"],
                        "gc": v["gc"],
                        "dg": dg,
                        "pts": pts,
                    }
                )

            ranking.sort(key=lambda x: (-x["pts"], -x["dg"], -x["gf"], str(x["equipo"]).lower()))
            cutoff = (len(ranking) + 1) // 2 if ranking else 0

            for i, row in enumerate(ranking, start=1):
                row["posicion"] = i
                row["estado"] = "CLASIFICADO" if i <= cutoff else "ELIMINADO"

            total_goles = sum(int(m["goles_local"] or 0) + int(m["goles_visitante"] or 0) for m in played)
            total_partidos = len(played)
            promedio = round(total_goles / total_partidos, 2) if total_partidos else 0.0

            cur.execute("SELECT COALESCE(SUM(tarjetas_amarillas + tarjetas_rojas), 0) FROM participantes")
            total_tarjetas = int(cur.fetchone()[0] or 0)

            mas_victorias = ranking[0]["equipo"] if ranking else "-"
            mas_goles = sorted(ranking, key=lambda x: (x["gf"], x["pts"], x["dg"]), reverse=True)[0]["equipo"] if ranking else "-"
            menos_recibidos = sorted(ranking, key=lambda x: (x["gc"], -x["pts"], -x["dg"]))[0]["equipo"] if ranking else "-"

            bracket_rows = []
            for m in matches:
                jugado = int(m["jugado"] or 0) == 1
                gl = int(m["goles_local"] or 0)
                gv = int(m["goles_visitante"] or 0)
                eliminado = "-"
                if not jugado:
                    ganador = "PENDIENTE"
                    icon = "PEN"
                elif gl > gv:
                    ganador = m["local_nombre"]
                    icon = "OK"
                    eliminado = m["visitante_nombre"]
                elif gv > gl:
                    ganador = m["visitante_nombre"]
                    icon = "OK"
                    eliminado = m["local_nombre"]
                else:
                    ganador = "EMPATE"
                    icon = "EQ"
                    eliminado = "-"

                bracket_rows.append(
                    {
                        "fase": m["fase"] or "",
                        "local": m["local_nombre"],
                        "visitante": m["visitante_nombre"],
                        "resultado": f"{gl} - {gv}" if jugado else "PENDIENTE",
                        "ganador": ganador,
                        "eliminado": eliminado,
                        "icono": icon,
                    }
                )

            return {
                "rows": ranking,
                "total_goles": total_goles,
                "total_partidos": total_partidos,
                "promedio_goles_partido": promedio,
                "total_tarjetas": total_tarjetas,
                "equipo_mas_victorias": mas_victorias,
                "equipo_mas_goles": mas_goles,
                "equipo_menos_recibidos": menos_recibidos,
                "goles_por_fase": self._format_goals_phase(goals_phase),
                "cuadro_eliminatorias": self._format_bracket_text(bracket_rows),
                "bracket_rows": bracket_rows,
                "generated_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        finally:
            con.close()

    def _format_goals_phase(self, goals_phase):
        if not goals_phase:
            return "Sin partidos jugados"
        ordered = ["Octavos", "Cuartos", "Semifinal", "Final"]
        chunks = [f"{f}: {goals_phase[f]}" for f in ordered if f in goals_phase]
        chunks.extend([f"{f}: {g}" for f, g in goals_phase.items() if f not in set(ordered)])
        return " | ".join(chunks)

    def _format_bracket_text(self, rows):
        if not rows:
            return "Sin eliminatorias"
        return " | ".join([f"{r['fase']}: {r['local']} vs {r['visitante']} -> {r['ganador']}" for r in rows])

    def _generate_native_pdf(self, report_key, data, filters, output_pdf):
        title = self.REPORTS[report_key]["title"]
        if report_key == "equipos_jugadores":
            body = self._html_equipos_jugadores(data)
        elif report_key == "partidos_resultados":
            body = self._html_partidos_resultados(data)
        else:
            body = self._html_clasificacion(data)

        tags = []
        for key, label in [
            ("equipo", "Equipo"),
            ("eliminatoria", "Eliminatoria"),
            ("jugador_destacado", "Jugador destacado"),
            ("fecha_desde", "Desde"),
            ("fecha_hasta", "Hasta"),
        ]:
            val = (filters.get(key) or "").strip()
            if val:
                tags.append(f"{label}: {val}")
        filtros = " | ".join(tags) if tags else "Sin filtros"

        html_doc = self._html_base(title, filtros, body)
        self._print_html_to_pdf(html_doc, output_pdf)

    def _prepare_logo_preview(self, target_height=72):
        if not self.logo_path.exists():
            return "", 0, 0

        try:
            image = QImage(str(self.logo_path))
            if image.isNull():
                return self.logo_path.resolve().as_uri(), 0, target_height

            scaled = image.scaledToHeight(target_height, Qt.TransformationMode.SmoothTransformation)
            preview_path = self.reports_dir / "_logo_header_preview.png"
            if scaled.save(str(preview_path), "PNG"):
                return preview_path.resolve().as_uri(), scaled.width(), scaled.height()
        except Exception:
            pass

        return self.logo_path.resolve().as_uri(), 0, target_height

    def _html_base(self, title, filtros, body):
        logo = ""
        logo_cell_width = 84
        if self.logo_path.exists():
            logo_uri, logo_w, logo_h = self._prepare_logo_preview(target_height=72)
            if logo_uri:
                logo_cell_width = max(84, logo_w + 12) if logo_w else 108
                logo = (
                    f"<img src='{logo_uri}' "
                    f"style='display:block; width:{logo_w}px; height:{logo_h}px; border:0;'/>"
                    if logo_w and logo_h
                    else f"<img src='{logo_uri}' style='display:block; border:0;'/>"
                )

        return f"""
        <html>
        <head>
            <meta charset='utf-8'/>
            <style>
                body {{ font-family: Arial, sans-serif; color: #111; font-size: 10pt; }}
                .title {{ font-size: 16pt; font-weight: bold; color: #b71c1c; }}
                .muted {{ color: #555; font-size: 9pt; }}
                .header-table {{ width: 100%; border-collapse: collapse; border-bottom: 2px solid #b71c1c; margin-bottom: 8px; }}
                .logo-cell {{ width: {logo_cell_width}px; vertical-align: top; }}
                .text-cell {{ vertical-align: top; padding-left: 8px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
                th {{ background: #b71c1c; color: white; border: 1px solid #8a1111; padding: 5px; font-size: 9pt; }}
                td {{ border: 1px solid #ddd; padding: 5px; font-size: 9pt; }}
                .card {{ border: 1px solid #ddd; border-left: 4px solid #b71c1c; padding: 8px; margin-top: 8px; }}
                .badge {{ font-weight: bold; }}
                .badge-main {{ color: #b71c1c; }}
                .badge-ok {{ color: #1b5e20; }}
                .badge-out {{ color: #b71c1c; }}
                .badge-pending {{ color: #ef6c00; }}
            </style>
        </head>
        <body>
            <table class='header-table'>
                <tr>
                    <td class='logo-cell'>{logo}</td>
                    <td class='text-cell'>
                    <div class='title'>{html.escape(self.torneo_nombre)}</div>
                    <div class='muted'>{html.escape(title)}</div>
                    <div class='muted'>Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</div>
                    <div class='muted'>Filtros: {html.escape(filtros)}</div>
                    </td>
                </tr>
            </table>
            {body}
        </body>
        </html>
        """

    def _html_equipos_jugadores(self, data):
        chunks = []
        for team in data.get("teams", []):
            chunks.append(f"<h3>{html.escape(team['equipo'])}</h3>")
            chunks.append("<table><tr><th>Jugador</th><th>Posicion</th><th>Goles</th><th>Amarillas</th><th>Rojas</th><th>Top Goles</th><th>Top Tarjetas</th></tr>")
            for p in team["jugadores"]:
                chunks.append(
                    "<tr>"
                    f"<td>{html.escape(str(p['jugador']))}</td>"
                    f"<td>{html.escape(str(p['posicion']))}</td>"
                    f"<td>{p['goles']}</td><td>{p['amarillas']}</td><td>{p['rojas']}</td>"
                    f"<td>{html.escape(p['top_goles'] or '')}</td><td>{html.escape(p['top_tarjetas'] or '')}</td>"
                    "</tr>"
                )
            chunks.append("</table>")
            chunks.append(
                "<div class='card'>"
                f"<span class='badge badge-main'>Total goles:</span> {team['total_goles']} | "
                f"<span class='badge badge-main'>Total amarillas:</span> {team['total_amarillas']} | "
                f"<span class='badge badge-main'>Total rojas:</span> {team['total_rojas']} | "
                f"<span class='badge badge-main'>Promedio goles/jugador:</span> {team['promedio_goles']}"
                "</div>"
            )
        return "".join(chunks) if chunks else "<div class='card'>No hay datos para este informe.</div>"

    def _html_partidos_resultados(self, data):
        rows = data.get("rows", [])
        if not rows:
            return "<div class='card'>No hay partidos para los filtros seleccionados.</div>"

        chunks = [
            f"<div class='card'><span class='badge badge-main'>Partidos pendientes:</span> {data.get('pending_count', 0)}</div>",
            "<table><tr><th>ID</th><th>Eliminatoria</th><th>Fecha</th><th>Hora</th><th>Local</th><th>Visitante</th><th>Arbitro</th><th>Resultado</th><th>Estado</th><th>Historial</th></tr>",
        ]
        for r in rows:
            estado = "<span class='badge'>Pendiente</span>" if r["estado"] == "Pendiente" else "Jugado"
            chunks.append(
                "<tr>"
                f"<td>{r['id']}</td><td>{html.escape(r['fase'])}</td><td>{html.escape(r['fecha'])}</td><td>{html.escape(r['hora'])}</td>"
                f"<td>{html.escape(r['equipo_local'])}</td><td>{html.escape(r['equipo_visitante'])}</td><td>{html.escape(r['arbitro'])}</td>"
                f"<td>{html.escape(r['resultado'])}</td><td>{estado}</td><td>{html.escape(r['historial'])}</td>"
                "</tr>"
            )
        chunks.append("</table>")
        return "".join(chunks)

    def _html_clasificacion(self, data):
        rows = data.get("rows", [])
        chunks = []
        if rows:
            chunks.append("<table><tr><th>Pos</th><th>Equipo</th><th>PJ</th><th>G</th><th>E</th><th>P</th><th>GF</th><th>GC</th><th>DG</th><th>Pts</th><th>Estado</th></tr>")
            for r in rows:
                estado = (
                    "<span class='badge badge-ok'>CLASIFICADO</span>"
                    if r["estado"] == "CLASIFICADO"
                    else "<span class='badge badge-out'>ELIMINADO</span>"
                )
                chunks.append(
                    "<tr>"
                    f"<td>{r['posicion']}</td><td>{html.escape(r['equipo'])}</td><td>{r['pj']}</td><td>{r['g']}</td><td>{r['e']}</td><td>{r['p']}</td>"
                    f"<td>{r['gf']}</td><td>{r['gc']}</td><td>{r['dg']}</td><td>{r['pts']}</td><td>{estado}</td>"
                    "</tr>"
                )
            chunks.append("</table>")
        else:
            chunks.append("<div class='card'>No hay datos de clasificacion.</div>")

        chunks.append(
            "<div class='card'>"
            f"<span class='badge badge-main'>Total goles:</span> {data.get('total_goles', 0)} | "
            f"<span class='badge badge-main'>Total tarjetas:</span> {data.get('total_tarjetas', 0)} | "
            f"<span class='badge badge-main'>Promedio goles/partido:</span> {data.get('promedio_goles_partido', 0)}"
            "</div>"
        )
        chunks.append(
            "<div class='card'>"
            f"<span class='badge badge-main'>Mas victorias:</span> {html.escape(str(data.get('equipo_mas_victorias', '-')))} | "
            f"<span class='badge badge-main'>Mas goles:</span> {html.escape(str(data.get('equipo_mas_goles', '-')))} | "
            f"<span class='badge badge-main'>Menos goles recibidos:</span> {html.escape(str(data.get('equipo_menos_recibidos', '-')))}"
            "</div>"
        )
        chunks.append(
            "<div class='card'>"
            f"<span class='badge badge-main'>Goles por eliminatoria:</span> {html.escape(str(data.get('goles_por_fase', '-')))}"
            "</div>"
        )

        bracket = data.get("bracket_rows", [])
        if bracket:
            chunks.append("<h3>Cuadro de Eliminatorias</h3>")
            chunks.append("<table><tr><th>Fase</th><th>Local</th><th>Visitante</th><th>Resultado</th><th>Ganador</th><th>Estado</th><th>Visual</th></tr>")
            for r in bracket:
                if r["icono"] == "PEN":
                    est = "Pendiente"
                    visual = "<span class='badge badge-pending'>PENDIENTE</span>"
                elif r["icono"] == "EQ":
                    est = "Empate"
                    visual = "<span class='badge badge-pending'>EMPATE</span>"
                else:
                    est = "Definido"
                    ganador = html.escape(r["ganador"])
                    eliminado = html.escape(r.get("eliminado", "-"))
                    visual = (
                        f"<span class='badge badge-ok'>OK {ganador}</span> / "
                        f"<span class='badge badge-out'>OUT {eliminado}</span>"
                    )
                chunks.append(
                    "<tr>"
                    f"<td>{html.escape(r['fase'])}</td><td>{html.escape(r['local'])}</td><td>{html.escape(r['visitante'])}</td>"
                    f"<td>{html.escape(r['resultado'])}</td><td>{html.escape(r['ganador'])}</td><td>{html.escape(est)}</td><td>{visual}</td>"
                    "</tr>"
                )
            chunks.append("</table>")

        return "".join(chunks)

    def _print_html_to_pdf(self, html_content, output_pdf):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(output_pdf)
        printer.setPageLayout(
            QPageLayout(
                QPageSize(QPageSize.PageSizeId.A4),
                QPageLayout.Orientation.Portrait,
                QMarginsF(12, 12, 12, 12),
            )
        )
        doc = QTextDocument()
        doc.setHtml(html_content)
        printer_fn = getattr(doc, "print_", None) or getattr(doc, "print", None)
        if printer_fn is None:
            raise RuntimeError("QTextDocument no soporta impresion PDF en este entorno")
        printer_fn(printer)
        if not Path(output_pdf).exists():
            raise RuntimeError("No se pudo escribir el PDF nativo")

    def _write_csv(self, report_key, data, csv_path):
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if report_key == "equipos_jugadores":
                w.writerow(["Equipo", "Jugador", "Posicion", "Goles", "Amarillas", "Rojas", "Top Goles", "Top Tarjetas", "Total Goles Eq", "Total Amarillas Eq", "Total Rojas Eq", "Promedio Goles Eq"])
                for r in data.get("rows", []):
                    w.writerow([r["equipo"], r["jugador"], r["posicion"], r["goles"], r["amarillas"], r["rojas"], r["top_goles"], r["top_tarjetas"], r["total_goles_equipo"], r["total_amarillas_equipo"], r["total_rojas_equipo"], r["promedio_goles_equipo"]])
            elif report_key == "partidos_resultados":
                w.writerow(["ID", "Eliminatoria", "Fecha", "Hora", "Equipo Local", "Equipo Visitante", "Arbitro", "Resultado", "Estado", "Historial"])
                for r in data.get("rows", []):
                    w.writerow([r["id"], r["fase"], r["fecha"], r["hora"], r["equipo_local"], r["equipo_visitante"], r["arbitro"], r["resultado"], r["estado"], r["historial"]])
            else:
                w.writerow(["CLASIFICACION"])
                w.writerow(["Pos", "Equipo", "PJ", "G", "E", "P", "GF", "GC", "DG", "Pts", "Estado"])
                for r in data.get("rows", []):
                    w.writerow([r["posicion"], r["equipo"], r["pj"], r["g"], r["e"], r["p"], r["gf"], r["gc"], r["dg"], r["pts"], r["estado"]])
                w.writerow([])
                w.writerow(["ESTADISTICAS GLOBALES"])
                w.writerow(["Total goles", data.get("total_goles", 0)])
                w.writerow(["Total tarjetas", data.get("total_tarjetas", 0)])
                w.writerow(["Promedio goles/partido", data.get("promedio_goles_partido", 0)])
                w.writerow(["Mas victorias", data.get("equipo_mas_victorias", "-")])
                w.writerow(["Mas goles", data.get("equipo_mas_goles", "-")])
                w.writerow(["Menos goles recibidos", data.get("equipo_menos_recibidos", "-")])
                w.writerow(["Goles por eliminatoria", data.get("goles_por_fase", "-")])
                w.writerow([])
                w.writerow(["CUADRO ELIMINATORIAS"])
                w.writerow(["Fase", "Local", "Visitante", "Resultado", "Ganador", "Estado"])
                for r in data.get("bracket_rows", []):
                    w.writerow([r["fase"], r["local"], r["visitante"], r["resultado"], r["ganador"], "Pendiente" if r["icono"] == "PEN" else "Definido"])

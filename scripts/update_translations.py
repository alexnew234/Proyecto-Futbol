# -*- coding: utf-8 -*-
import re
import xml.etree.ElementTree as ET
from pathlib import Path

TS_PATH = Path("translations/app_en.ts")

TRANSLATIONS = {
    "Form": {
        "Form": "Form",
        "Nombre del equipo": "Team Name",
        "Curso": "Course",
        "Color de camiseta": "Shirt Color",
        "Logo": "Logo",
        "Enviar": "Submit",
        "10": "10",
        "23": "23",
        "56": "56",
        ":": ":",
    },
    "MainWindow": {
        "Exportar CSV": "Export CSV",
        "Guardar tabla en Excel/CSV": "Save table to Excel/CSV",
        "Equipos": "Teams",
        "Participantes": "Participants",
        "Partidos": "Matches",
        "Clasificación": "Standings",
        "Créditos": "Credits",
        "Ayuda": "Help",
        "Salir (Inicio)": "Exit (Home)",
        "(Todos/Jugador/Árbitro)": "(All/Player/Referee)",
        "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Fase Final</span></p></body></html>": "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt; font-weight:700;\">Final Stage</span></p></body></html>",
        "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Calendario del torneo</span></p></body></html>": "<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">Tournament Calendar</span></p></body></html>",
        "<html><head/><body><p><br/></p></body></html>": "<html><head/><body><p><br/></p></body></html>",
        "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Equipo Local</span></p></body></html>": "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Home Team</span></p></body></html>",
        "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Equipo Visitante</span></p></body></html>": "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Away Team</span></p></body></html>",
        "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">VS</span></p></body></html>": "<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">VS</span></p></body></html>",
        "Añadir equipo": "Add Team",
        "Buscar:": "Search:",
        "Color Camiseta": "Shirt Color",
        "Cuartos": "Quarterfinals",
        "Curso": "Course",
        "Datos Generales": "General Data",
        "Detalles": "Details",
        "Editar equipo": "Edit Team",
        "Eliminar equipo": "Delete Team",
        "Enfrentamiento": "Matchup",
        "Escudo": "Logo",
        "Estado": "Status",
        "Fecha": "Date",
        "Fecha Nacimiento": "Birth Date",
        "Fecha: ": "Date: ",
        "Filtrar por:": "Filter by:",
        "Final": "Final",
        "Generar Rondas": "Generate Rounds",
        "Goles": "Goals",
        "Hora": "Time",
        "Jug Locales": "Home Players",
        "Jug Visitantes": "Away Players",
        "Jugador": "Player",
        "MainWindow": "MainWindow",
        "Marcador Global": "Overall Score",
        "Nombre": "Name",
        "Nuevo Participante": "New Participant",
        "Posición": "Position",
        "Salir": "Exit",
        "Semifinales": "Semifinals",
        "Tarjetas Amarillas": "Yellow Cards",
        "Tarjetas Rojas": "Red Cards",
        "toolBar": "Toolbar",
        "Árbitro": "Referee",
    },
    "DashboardView": {
        "Panel de Control RFEF": "RFEF Control Panel",
        "⚙️ Configuración del Reloj": "⚙️ Clock Settings",
        "Gestión de Partidos": "Match Management",
        "Resultados / Clasificación": "Results / Standings",
        "Equipos": "Teams",
        "Participantes": "Participants",
    },
    "RelojConfigView": {
        "ALARMA: {mensaje}": "ALARM: {mensaje}",
        "Aviso del Reloj": "Clock Alert",
        "SEÑAL RECIBIDA: timerFinished()": "SIGNAL RECEIVED: timerFinished()",
        "Propiedades del Componente": "Component Properties",
        "Modo de Funcionamiento:": "Operating Mode:",
        "Reloj Digital (Hora)": "Digital Clock (Time)",
        "Cronómetro / Temporizador": "Stopwatch / Timer",
        "Formato 24 Horas": "24-Hour Format",
        "Modo Cuenta Regresiva (Solo Timer)": "Countdown Mode (Timer Only)",
        "Configuración de Alarma y Tiempos": "Alarm and Time Settings",
        "Alarma Activada": "Alarm Enabled",
        "Mensaje de Alarma:": "Alarm Message:",
        "Hora de Alarma (Modo Reloj):": "Alarm Time (Clock Mode):",
        "Duración / Límite (Segundos):": "Duration / Limit (Seconds):",
        "Control Manual": "Manual Control",
        "Iniciar": "Start",
        "Pausar": "Pause",
        "Reiniciar": "Reset",
        "VISTA PREVIA DEL COMPONENTE": "COMPONENT PREVIEW",
        "¡Tiempo completado!": "Time completed!",
        "Esperando señal...": "Waiting for signal...",
    },
    "FormUniversalView": {
        "Gestión RFEF": "RFEF Management",
        "Registro": "Registration",
        "Nombre Equipo:": "Team Name:",
        "Curso:": "Course:",
        "Color:": "Color:",
        "Escudo:": "Logo:",
        "Seleccionar Escudo...": "Select Logo...",
        "Datos Personales": "Personal Data",
        "Nombre:": "Name:",
        "Fecha Nacim.:": "Birth Date:",
        "Tipo:": "Type:",
        "Posición:": "Position:",
        "Equipo:": "Team:",
        "Ej: 1º DAW": "e.g., 1st DAW",
        "Jugador": "Player",
        "Árbitro": "Referee",
        "Ambos": "Both",
        "Portero": "Goalkeeper",
        "Defensa": "Defender",
        "Centrocampista": "Midfielder",
        "Delantero": "Forward",
        "N/A": "N/A",
        "Estadísticas Iniciales": "Initial Statistics",
        "T. Amarillas:": "Yellow Cards:",
        "T. Rojas:": "Red Cards:",
        "Goles:": "Goals:",
        "GUARDAR": "SAVE",
        "Alta de Equipo": "Team Registration",
        "Ficha de Participante": "Participant Profile",
        "Editar Equipo": "Edit Team",
        "Actualizar Datos": "Update Data",
        "Editar Participante": "Edit Participant",
        "Actualizar Participante": "Update Participant",
    },
    "RelojDigital": {
        "¡Aviso del Reloj!": "Clock alert!",
    },
    "UniversalController": {
        "Seleccionar Escudo": "Select Logo",
        "Imágenes (*.png *.jpg)": "Images (*.png *.jpg)",
        "Imagen": "Image",
        "Imagen actual": "Current image",
        "Error": "Error",
        "El nombre no puede estar vacío.": "The name cannot be empty.",
        "El nombre del equipo no puede contener números.": "The team name cannot contain numbers.",
        "Equipo actualizado correctamente": "Team updated successfully",
        "Equipo creado correctamente": "Team created successfully",
        "Éxito": "Success",
        "Error SQL": "SQL Error",
        "El nombre del participante no puede contener números.": "The participant name cannot contain numbers.",
        "Participante actualizado correctamente": "Participant updated successfully",
        "Participante registrado correctamente": "Participant registered successfully",
    },
    "EquiposController": {
        "Aviso": "Notice",
        "Selecciona un equipo de la lista primero": "Select a team from the list first",
        "Error": "Error",
        "No se pudieron leer los datos": "Could not read the data",
        "Por favor, selecciona un equipo para eliminar.": "Please select a team to delete.",
        "Confirmar borrado": "Confirm deletion",
        "¿Estás seguro de que quieres eliminar el equipo '{nombre}'?\nSe borrarán AUTOMÁTICAMENTE todos sus jugadores.": (
            "Are you sure you want to delete the team '{nombre}'?\n"
            "All its players will be AUTOMATICALLY deleted."
        ),
        "Éxito": "Success",
        "Equipo eliminado.": "Team deleted.",
        "Falló el borrado del equipo.": "Failed to delete the team.",
        "No se encontró el ID del equipo.": "Team ID not found.",
        "Sin imagen": "No image",
        "Error: {error}": "Error: {error}",
    },
    "ParticipantesController": {
        "Todos": "All",
        "Jugador": "Player",
        "Árbitro": "Referee",
        "--- Rankings ---": "--- Rankings ---",
        "Máximos Goleadores": "Top Scorers",
        "Más Tarjetas": "Most Cards",
        "Editar": "Edit",
        "Eliminar": "Delete",
        "Confirmar eliminación": "Confirm deletion",
        "¿Deseas eliminar al participante '{nombre}'?": "Do you want to delete participant '{nombre}'?",
        "Éxito": "Success",
        "Participante '{nombre}' eliminado correctamente.": "Participant '{nombre}' deleted successfully.",
        "Error": "Error",
        "No se pudo eliminar el participante: {error}": "Could not delete participant: {error}",
    },
    "MainController": {
        "⚙️ Config. Reloj": "⚙️ Clock Config",
        "Idioma / Language:": "Language:",
        "🇪🇸 Español": "🇪🇸 Spanish",
        "🇺🇸 English": "🇺🇸 English",
        "Error": "Error",
        "No hay datos para exportar.": "No data to export.",
        "Guardar Clasificación": "Save Standings",
        "Archivos CSV (*.csv)": "CSV Files (*.csv)",
        "Éxito": "Success",
        "Datos exportados correctamente.": "Data exported successfully.",
        "Error al guardar: {error}": "Error while saving: {error}",
        "Col {col}": "Col {col}",
        "Acerca de - Gestor de Torneos": "About - Tournament Manager",
        "Ayuda - Guía Rápida": "Help - Quick Guide",
        "Configuración": "Settings",
        "Pos": "Pos",
        "Equipo": "Team",
        "PJ": "MP",
        "G": "W",
        "E": "D",
        "P": "L",
        "GF": "GF",
        "GC": "GA",
        "DG": "GD",
        "Pts": "Pts",
        """
        <h3>⚽ Gestor de Torneos de Fútbol</h3>
        <p>Aplicación para la gestión integral de competiciones deportivas.</p>
        <hr>
        <p><b>👤 Autor:</b> Alex</p>
        <p><b>📅 Fecha de Actualización:</b> 29 de Enero de 2026</p>
        <p><b>🏷️ Versión:</b> 1.0.0 (Release Final)</p>
        <hr>
        <p><i>Desarrollado con Python 3.13, PySide6 y SQLite.</i></p>
        """: """
        <h3>⚽ Football Tournament Manager</h3>
        <p>Application for comprehensive management of sports competitions.</p>
        <hr>
        <p><b>👤 Author:</b> Alex</p>
        <p><b>📅 Last Updated:</b> January 29, 2026</p>
        <p><b>🏷️ Version:</b> 1.0.0 (Final Release)</p>
        <hr>
        <p><i>Developed with Python 3.13, PySide6 and SQLite.</i></p>
        """,
        """
        <h3>📖 Cómo utilizar el Gestor</h3>
        <ol>
            <li><b>Crear Equipos:</b> Ve a la pestaña 'Equipos' y registra los clubes participantes.</li>
            <li><b>Generar Torneo:</b> En la pestaña 'Partidos', pulsa el botón verde <b>'Generar Siguiente Ronda'</b>.</li>
            <li><b>Registrar Resultados:</b> Haz <b>doble clic</b> sobre un partido del calendario para editar el marcador, la fecha y asignar goles a jugadores.</li>
            <li><b>Eliminar Errores:</b> Haz <b>clic derecho</b> sobre un partido si necesitas borrarlo.</li>
            <li><b>Ver Clasificación:</b> Consulta la tabla actualizada automáticamente en la sección 'Clasificación'.</li>
        </ol>
        <p><i>Nota: Es necesario completar todos los partidos de una ronda para poder generar la siguiente.</i></p>
        """: """
        <h3>📖 How to use the Manager</h3>
        <ol>
            <li><b>Create Teams:</b> Go to the 'Teams' tab and register participating clubs.</li>
            <li><b>Generate Tournament:</b> In the 'Matches' tab, click the green <b>'Generate Next Round'</b> button.</li>
            <li><b>Record Results:</b> Double-click a match in the calendar to edit the score, date, and assign goals to players.</li>
            <li><b>Delete Errors:</b> Right-click a match if you need to delete it.</li>
            <li><b>View Standings:</b> Check the automatically updated table in the 'Standings' section.</li>
        </ol>
        <p><i>Note: You must complete all matches in a round to generate the next one.</i></p>
        """,
    },
    "Calendario": {
        "Generar Siguiente Ronda": "Generate Next Round",
        "Ver Clasificación": "View Standings",
        "Nueva Temporada": "New Season",
        "Volver al Calendario": "Back to Calendar",
        "Equipo": "Team",
        "Octavos": "Round of 16",
        "Cuartos": "Quarterfinals",
        "Semifinal": "Semifinal",
        "Final": "Final",
        "Ronda actual: Ninguna generada": "Current round: None generated",
        "No hay partidos programados": "No matches scheduled",
        "Ronda actual: {fase}": "Current round: {fase}",
        "vs": "vs",
        "Finalizado": "Finished",
        "Árb:": "Ref:",
        "Eliminar Partido": "Delete Match",
        "Confirmar": "Confirm",
        "¿Eliminar este partido?": "Delete this match?",
        "Info": "Info",
        "Reinicia la temporada.": "Restart the season.",
        "Error": "Error",
        "Faltan equipos (mínimo 2).": "Not enough teams (minimum 2).",
        "Partidos pendientes.": "Pending matches.",
        "Desconocido": "Unknown",
        "Empate": "Draw",
        "🏆 CAMPEÓN: {ganador} 🏆": "🏆 CHAMPION: {ganador} 🏆",
        "¡Fin!": "Finished!",
        "Faltan ganadores.": "Missing winners.",
        "Éxito": "Success",
        "Ronda {fase} generada.": "Round {fase} generated.",
        "Fallo al generar.": "Failed to generate.",
        "{local} vs {visit}": "{local} vs {visit}",
        "Goles {equipo}:": "Goals {equipo}:",
        "Fecha:": "Date:",
        "Hora:": "Time:",
        "Árbitro asignado:": "Assigned referee:",
        "Sin asignar": "Unassigned",
        "Gestionar Goles y Tarjetas": "Manage Goals and Cards",
        "⏱ CRONÓMETRO": "⏱ STOPWATCH",
        "¡Tiempo de partido finalizado!": "Match time finished!",
        "Árbitro": "Referee",
        "▶ Iniciar": "▶ Start",
        "⏸ Pausar": "⏸ Pause",
        "↺ Reiniciar": "↺ Reset",
        "GUARDAR RESULTADO DEL PARTIDO": "SAVE MATCH RESULT",
        "Estadísticas de Jugadores": "Player Statistics",
        "Nombre del Jugador": "Player Name",
        "Goles (+)": "Goals (+)",
        "Amarillas (+)": "Yellow Cards (+)",
        "Rojas (+)": "Red Cards (+)",
        "{nombre} (Total: {goles}G)": "{nombre} (Total: {goles}G)",
        "CONFIRMAR Y ACTUALIZAR ESTADÍSTICAS": "CONFIRM AND UPDATE STATISTICS",
        "Estadísticas actualizadas.\nLos goles se han sumado al marcador.": "Statistics updated.\nGoals have been added to the score.",
        "No hubo cambios para guardar.": "No changes to save.",
        "Resultado actualizado.": "Result updated.",
        "Reiniciar": "Reset",
        "¿Borrar TODO?": "Delete EVERYTHING?",
        "Listo": "Done",
        "Temporada reiniciada.": "Season restarted.",
    },
}


def upsert_message(ctx, source, translation):
    for msg in ctx.findall("message"):
        if msg.findtext("source") == source:
            tr_el = msg.find("translation")
            if tr_el is None:
                tr_el = ET.SubElement(msg, "translation")
            tr_el.text = translation
            if "type" in tr_el.attrib:
                del tr_el.attrib["type"]
            return
    msg = ET.SubElement(ctx, "message")
    src_el = ET.SubElement(msg, "source")
    src_el.text = source
    tr_el = ET.SubElement(msg, "translation")
    tr_el.text = translation


def main():
    if not TS_PATH.exists():
        raise SystemExit(f"No se encuentra {TS_PATH}")

    tree = ET.parse(TS_PATH)
    root = tree.getroot()

    context_map = {}
    for ctx in root.findall("context"):
        name = ctx.findtext("name")
        if name:
            context_map[name] = ctx

    for ctx_name, messages in TRANSLATIONS.items():
        ctx = context_map.get(ctx_name)
        if ctx is None:
            ctx = ET.SubElement(root, "context")
            name_el = ET.SubElement(ctx, "name")
            name_el.text = ctx_name
            context_map[ctx_name] = ctx
        for source, translation in messages.items():
            upsert_message(ctx, source, translation)

    # Eliminar entradas corruptas (p.ej. Clasificaci?n, ?? Config. Reloj)
    for ctx in root.findall("context"):
        for msg in list(ctx.findall("message")):
            src = msg.findtext("source") or ""
            if "�" in src or "??" in src or re.search(r"[A-Za-z]\?[A-Za-z]", src):
                ctx.remove(msg)

    ET.indent(tree, space="    ", level=0)
    tree.write(TS_PATH, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()

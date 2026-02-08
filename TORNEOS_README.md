# ⚽ Gestor de Torneos de Fútbol

Aplicación de escritorio desarrollada en Python con PySide6 para la gestión integral de torneos, equipos, participantes, calendarios y clasificaciones automáticas.

**Requisitos**
- Python 3.13
- PySide6
- SQLite (incluido en Python)
- Windows 10/11 recomendado

**Instalación (código fuente)**
Si utilizas el ejecutable `GestorTorneos.exe`, no necesitas instalar la librería de BD manualmente.

1. Abre una terminal.
2. Entra en la carpeta `torneofutbol_db`.
3. Ejecuta `pip install -e .`.
4. Desde la raíz del proyecto, ejecuta `python main.py`.

**Uso rápido**
1. Crea equipos en la pestaña `Equipos`.
2. Agrega participantes en `Participantes`.
3. Genera la primera ronda en `Partidos` con `Generar Siguiente Ronda`.
4. Doble clic en un partido para editar marcador, fecha, hora, árbitro y gestionar goles o tarjetas.
5. Guarda el resultado para actualizar la clasificación automáticamente.

**Reloj y cronómetro**
- El cronómetro del partido aparece en el diálogo de edición del partido.
- La alarma muestra un aviso en la interfaz y puede mostrar un popup.
- Al guardar un partido se muestra la duración registrada en el mismo aviso de resultado actualizado.
- Si quieres que el cronómetro del partido use tu configuración, entra en "Config. Reloj" y selecciona "Cronómetro / Temporizador". Si se queda en "Reloj Digital", se usan los valores por defecto (90 min).

**Configuraciones recomendadas**
- En `Config. Reloj` ajusta `Duración / Límite (Segundos)` según el formato del torneo.
- Activa o desactiva `Modo Cuenta Regresiva` según si quieres cuenta atrás o cronómetro ascendente.
- Personaliza el `Mensaje de Alarma` para que el aviso sea claro durante el partido.

**Consideraciones**
- Las fases avanzan automáticamente: Octavos -> Cuartos -> Semifinal -> Final.
- No se puede generar la siguiente ronda si hay partidos pendientes.
- `Nueva Temporada` borra los partidos y reinicia estadísticas de jugadores.
- La tabla de clasificación se recalcula al guardar resultados.
- Puedes exportar la clasificación a CSV desde la pestaña `Clasificación`.

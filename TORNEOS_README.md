# ⚽ Gestor de Torneos de Fútbol

Aplicación de escritorio desarrollada en Python con PySide6 para la gestión integral de torneos, equipos, participantes, calendarios y clasificaciones automáticas.

---

## 📋 Resumen de Implementación

Se ha implementado un sistema modular completo con arquitectura MVC. El sistema gestiona automáticamente las fases del torneo (Octavos, Cuartos, Semifinal, Final), sincroniza estadísticas de jugadores con el marcador global y calcula la clasificación en tiempo real.

---

## 🚀 Guía de Instalación (Imprescindible)

Este proyecto utiliza una **arquitectura modular estricta**. El acceso a datos se ha separado en una librería externa para cumplir con los requisitos de diseño.

<<<<<<< Updated upstream
### 1. Instalación de la Librería de Base de Datos
**Paso obligatorio.** El programa fallará si no se instala primero este módulo.
Nota: Si utilizas directamente el archivo GestorTorneos.exe, no es necesario realizar esta instalación manual ya que la librería viene integrada en el ejecutable. Este paso es solo para ejecutar el código fuente (.py).

1.  Abre una terminal.
2.  Navega a la carpeta de la librería externa (`torneofutbol_db`):
    cd ruta/a/torneofutbol_db


3.  Instálala en el sistema:
    pip install -e .


### 3. Ejecución
Ejecutable o 
python main.py
=======
**Ventana de Informes (Tarea 5)**
- Abre `Informes` desde el menú superior.
- La interfaz de informes está definida en `Views/reports_window.ui` (Qt Designer).
- Selecciona uno de los 3 informes:
  - `Informe Equipos y Jugadores`
  - `Informe Partidos y Resultados`
  - `Informe Clasificación y Eliminatorias`
- Configura filtros opcionales: equipo, jugador destacado, eliminatoria y rango de fechas.
- En `Partidos y Resultados` se incluye historial de enfrentamientos con resultados previos.
- En `Clasificación y Eliminatorias` se incluye cuadro visual con indicadores `[OK]/[OUT]/[PEN]/[EQ]`.
- Todos los reportes incluyen encabezado, pie con metadatos y numeración de página.
- Elige la carpeta de salida para PDF/CSV y pulsa `Generar y guardar`.
- Los archivos base (`.jrxml`, `.jasper`, `.pdf`, `.csv`) se generan en `reports/`.
- Si eliges otra ruta de salida, se copia allí el PDF/CSV final.

**Requisitos para Jasper (generación PDF desde JRXML)**
- `pip install pyreportjasper`
- Java JDK instalado y `JAVA_HOME` válido.
- Driver SQLite JDBC (`sqlite-jdbc*.jar`) en `reports/lib/`.
  - Alternativamente, define `SQLITE_JDBC_JAR` con la ruta completa del `.jar`.
- Si Jasper no está disponible, la app usa automáticamente un motor nativo de respaldo para no bloquear la generación.

**Consideraciones**
- Las fases avanzan automáticamente: Octavos -> Cuartos -> Semifinal -> Final.
- No se puede generar la siguiente ronda si hay partidos pendientes.
- `Nueva Temporada` borra los partidos y reinicia estadísticas de jugadores.
- La tabla de clasificación se recalcula al guardar resultados.
- Puedes exportar la clasificación a CSV desde la pestaña `Clasificación`.
>>>>>>> Stashed changes

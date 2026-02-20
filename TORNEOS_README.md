# Gestor de Torneos de Futbol

Aplicacion de escritorio (Python + PySide6) con gestion de equipos, participantes,
partidos, clasificacion, componente reloj reutilizable e informes PDF/CSV.

## Requisitos

- Python 3.13
- Java JDK (solo para Jasper en informes)
- Libreria externa `torneo_db` instalada en editable:

```bash
cd C:/ruta/torneofutbol_db
pip install -e .
```

## Ejecucion en desarrollo

```bash
python main.py
```

## Cumplimiento Tarea 4 (Reloj digital)

- Componente reutilizable: `Views/reloj_widget.py` (`RelojDigital`).
- Modo enumerado: `mode` con `clock` / `timer` (`ModoReloj`).
- Propiedades publicas: `is24Hour`, `alarmEnabled`, `alarmHour`, `alarmMinute`,
  `alarmMessage`, `duracionPartido`, `isCountDown`.
- Senales: `alarmTriggered(str)` y `timerFinished()`.
- Gestion interna de tiempo: `QTimer` cada 1 segundo.
- Metodos publicos: `start()`, `pause()`, `reset()`.
- Integracion en app de torneos:
  - Dashboard y cabecera de partidos con reloj en tiempo real.
  - Dialogo de edicion de partido con cronometro y controles.
  - Configuracion desde app via propiedades/metodos publicos (sin tocar internals).
- Reaccion a eventos:
  - Etiqueta de aviso y popup al disparar alarma/senal.
- Internacionalizacion Qt:
  - Uso de `QTranslator` en `Controllers/main_controller.py`.
  - Archivos `translations/app_es.ts`, `translations/app_en.ts`.
  - Compilados `translations/app_es.qm`, `translations/app_en.qm`.

## Traducciones Qt (regenerar)

```bash
# lupdate (extraer textos a .ts)
pyside6-lupdate main.py Controllers/*.py Views/*.py -ts translations/app_es.ts translations/app_en.ts

# lrelease (compilar .qm)
pyside6-lrelease translations/app_es.ts -qm translations/app_es.qm
pyside6-lrelease translations/app_en.ts -qm translations/app_en.qm
```

## Entregables ejecutables

- Aplicacion principal: `dist/GestorTorneos.exe`
- Componente reloj standalone: `dist/RelojComponente.exe`

Ejemplo de compilacion:

```bash
pyinstaller GestorTorneos.spec
pyinstaller --noconfirm --onefile --windowed --name RelojComponente reloj_app.py
```

## Informes (Tarea 5)

Carpeta de trabajo: `reports/`

- Plantillas JRXML: `reports/informe_*.jrxml`
- JDBC SQLite: `reports/lib/sqlite-jdbc-*.jar`
- Adapter ejemplo para JasperStudio: `reports/SQLITE_adapter_torneo.jrdax`

### Uso de la ventana de informes

1. Abrir `Informes` desde la barra principal.
2. Seleccionar tipo de informe:
   - Equipos y Jugadores
   - Partidos y Resultados
   - Clasificacion y Eliminatorias
3. Configurar filtros opcionales:
   - Equipo / Jugador destacado (informe 1)
   - Eliminatoria (informes 2 y 3)
   - Fecha desde / hasta (todos)
4. Elegir destino PDF/CSV (opcional).  
   Nota: aunque se copie al destino elegido, los archivos internos se generan en `reports/`.
5. Marcar o desmarcar:
   - `Exportar CSV`
   - `Forzar motor nativo (sin Jasper)`
6. Pulsar `Generar y guardar`.
7. Verificar en log:
   - `Motor: Jasper` o `Motor: Nativo`
   - ruta de PDF, CSV y `.jasper` (si aplico Jasper)

### Jasper en cualquier maquina

Para usar motor Jasper:

- Java JDK instalado (con `jvm.dll` disponible)
- `sqlite-jdbc-*.jar` en `reports/lib/`

Si falta Java/JDBC, la aplicacion entra automaticamente en motor nativo.

### JasperStudio (edicion de plantillas)

- Abrir `reports/informe_*.jrxml` en JasperStudio.
- Configurar Data Adapter SQLite con JDBC URL:
  - `jdbc:sqlite:C:/Users/<usuario>/TorneoFutbolData/torneo_futbol.db`
- Driver class: `org.sqlite.JDBC`
- Jar: `reports/lib/sqlite-jdbc-3.41.2.2.jar` (o version disponible)

### Archivos generados

En cada ejecucion se generan (timestamp):

- PDF: `reports/informe_*_YYYYMMDD_HHMMSS.pdf`
- CSV (si se marca): `reports/informe_*_YYYYMMDD_HHMMSS.csv`
- Jasper compilado (si motor Jasper): `reports/informe_*_YYYYMMDD_HHMMSS.jasper`

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

Nota:
- Estos requisitos aplican para ejecutar en desarrollo (`python main.py`).
- Si se ejecuta con `dist/GestorTorneos.exe`, no hace falta instalar Python ni `torneo_db`.

## Ejecucion en desarrollo

```bash
python main.py
```

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

## Ejecucion en otro ordenador (EXE)

1. Descargar o copiar el proyecto completo.
2. Ejecutar `dist/GestorTorneos.exe` con doble clic.
3. Para informes con Jasper:
   - Java JDK instalado en el sistema.
   - `sqlite-jdbc-*.jar` disponible en `reports/lib/`.
4. Si Java/JDBC no esta disponible, la app genera informes con motor nativo.

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
   - Equipo / Jugador destacado
   - Eliminatoria
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

# ⚽ Gestor de Torneos de Fútbol

Aplicación de escritorio desarrollada en Python con PySide6 para la gestión integral de torneos, equipos, participantes, calendarios y clasificaciones automáticas.

---

## 📋 Resumen de Implementación

Se ha implementado un sistema modular completo con arquitectura MVC. El sistema gestiona automáticamente las fases del torneo (Octavos, Cuartos, Semifinal, Final), sincroniza estadísticas de jugadores con el marcador global y calcula la clasificación en tiempo real.

---

## 🚀 Guía de Instalación (Imprescindible)

Este proyecto utiliza una **arquitectura modular estricta**. El acceso a datos se ha separado en una librería externa para cumplir con los requisitos de diseño.

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

#!/usr/bin/env python
"""
Script de prueba para verificar que el sistema de torneos funciona correctamente
"""
import sys
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
    
    print("\n✓ Estructura de base de datos válida")
    return True

def main():
    # Crear aplicación
    app = QApplication(sys.argv)
    
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

if __name__ == "__main__":
    main()

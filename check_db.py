#!/usr/bin/env python
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from Models.database import conectar

app = QApplication(sys.argv)
conectar()

query = QSqlQuery()
query.exec("SELECT name FROM sqlite_master WHERE type='table'")
print('Tablas en la BD:')
while query.next():
    print(f'  - {query.value(0)}')

print('\nCampos de partidos:')
query2 = QSqlQuery()
query2.exec("PRAGMA table_info(partidos)")
while query2.next():
    print(f'  - {query2.value(1)} ({query2.value(2)})')

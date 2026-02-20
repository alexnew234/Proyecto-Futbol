# -*- mode: python ; coding: utf-8 -*-

import os

project_root = os.path.abspath('.')
db_lib_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'torneofutbol_db')
data_dirs = []

for folder_name in ('Resources', 'translations', 'reports'):
    folder_path = os.path.join(project_root, folder_name)
    if os.path.exists(folder_path):
        data_dirs.append((folder_path, folder_name))


a = Analysis(
    ['main.py'],
    pathex=[project_root, db_lib_path],
    binaries=[],
    datas=data_dirs,
    hiddenimports=['torneo_db', 'pyreportjasper', 'jpype', 'jpype.imports'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='GestorTorneos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

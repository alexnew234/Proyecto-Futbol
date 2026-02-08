# -*- mode: python ; coding: utf-8 -*-

import os

project_root = os.path.abspath(os.getcwd())
db_pkg_root = os.path.join(project_root, "torneofutbol_db")

a = Analysis(
    ['main.py'],
    pathex=[project_root, db_pkg_root],
    binaries=[],
    datas=[
        (os.path.join(project_root, "Resources"), "Resources"),
        (os.path.join(project_root, "translations"), "translations"),
    ],
    hiddenimports=['torneo_db'],
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

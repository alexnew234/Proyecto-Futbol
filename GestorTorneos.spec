# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=['C:\\Users\\Alex\\Desktop\\torneofutbol_db'],
    binaries=[],
<<<<<<< Updated upstream
    datas=[('Resources', 'Resources')],
    hiddenimports=['torneo_db'],
=======
    datas=[
        (os.path.join(project_root, "Resources"), "Resources"),
        (os.path.join(project_root, "translations"), "translations"),
        (os.path.join(project_root, "reports"), "reports"),
    ],
    hiddenimports=['torneo_db', 'pyreportjasper', 'jpype', 'jpype.imports'],
>>>>>>> Stashed changes
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

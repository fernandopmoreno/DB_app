# -*- mode: python ; coding: utf-8 -*-


a = Analysis(['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
       ('.env', '.'),
       ('csv', 'csv'),
       ('doc', 'doc'),
       ('excel', 'excel'),
       ('fonts', 'fonts'),
       ('images', 'images'),
       ('pdfs', 'pdfs'),
       ('sql', 'sql'),
       ('tables', 'tables')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False)
pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DB_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None 
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DB_app',
)

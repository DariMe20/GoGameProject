# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['gui\\controllers\\MainMenuPageController.py'],
    pathex=[],
    binaries=[],
    datas=[('gui', 'gui'), ('utils', 'utils'), ('agent', 'agent'), ('dlgo', 'dlgo'), ('reinforcement_learning', 'reinforcement_learning')],
    hiddenimports=['encoders', 'game_rules_implementation', 'keras_networks'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MainMenuPageController',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

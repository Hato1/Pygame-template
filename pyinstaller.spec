# -*- mode: python ; coding: utf-8 -*-

import sys
import tomllib
import pkgutil
from importlib.resources import files

platform = sys.platform
if platform.startswith('darwin'):
    platform = "mac"
if platform.startswith("win"):
    platform = "win"

# Extract program name and version from pyproject.toml
with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)
name = data['project']['name']
version = data['project']['version']


a = Analysis(
    [files(name) / "main.py"],
    pathex=[],
    binaries=[],
    datas=[(files(name) / "assets", "assets")],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name=f'{name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# in one-file mode COLLECT is not used.
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=f'{name}-{version}-{platform}',
)

import sys

from PyInstaller.building.build_main import COLLECT, EXE, PYZ, Analysis

# Platform specific configuration
platform_configs = {
    "win32": {"icon": "assets/icon.ico", "extra_binaries": [], "extension": ".exe"},
    "darwin": {"icon": "assets/icon.icns", "extra_binaries": [], "extension": ".app"},
    "linux": {"icon": "assets/icon.png", "extra_binaries": [], "extension": ""},
}

# Get current platform
current_platform = sys.platform
config = platform_configs.get(current_platform, platform_configs["linux"])

a = Analysis(
    ["musa/__main__.py"],
    pathex=[],
    binaries=config["extra_binaries"],
    datas=[
        ("assets/*", "assets"),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

# Executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Musa",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=config["icon"],
)

# Collects all files
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="Musa",
)

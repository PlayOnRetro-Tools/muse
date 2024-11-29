import os
import sys
from typing import List, Tuple

from PyInstaller.building.build_main import EXE, PYZ, Analysis
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Platform specific configuration
platform_configs = {
    "win32": {"icon": "assets/musa_256.ico", "extra_binaries": [], "extension": ".exe"},
    "darwin": {
        "icon": "assets/musa_256.icns",
        "extra_binaries": [],
        "extension": ".app",
    },
    "linux": {"icon": "assets/musa_256.png", "extra_binaries": [], "extension": ""},
}

# Get current platform
current_platform = sys.platform
config = platform_configs.get(current_platform, platform_configs["linux"])

# Get absolute paths
spec_root = os.path.dirname(os.path.abspath(__name__))
app_root = os.path.join(spec_root, "musa")
main_script = os.path.join(app_root, "__main__.py")

# Ensure app folder is in the path
sys.path.insert(0, spec_root)

qt_modules = collect_submodules("PyQt5")
qt_data = collect_data_files("PyQt5")
app_submodules = collect_submodules("musa")


a = Analysis(
    [main_script],
    pathex=[app_root, spec_root],
    binaries=config["extra_binaries"],
    datas=[*qt_data, ("assets/*", "assets"), (app_root, "musa")],
    hiddenimports=[*qt_modules, *app_submodules, "PyQt5.sip"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)


def remove_duplicates(modules: List[Tuple]):
    seen = set()
    return [x for x in modules if not (x[0] in seen or seen.add(x[0]))]


a.data = remove_duplicates(a.datas)
a.binaries = remove_duplicates(a.binaries)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    exclude_binaries=False,
    name="muse",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=config["icon"],
)

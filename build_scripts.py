import os
import platform
import subprocess
from pathlib import Path

_APP_NAME = "musa"


def check_requirements():
    """Check if all required tools are installed"""
    try:
        import PyInstaller

        return True
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run(["poetry", "add", "--group", "dev", "pyinstaller"], check=True)
        return True


def clean_builds_dir():
    """Cleans previous build artifacts"""
    build_dir = Path("dist")
    if build_dir.exists():
        import shutil

        shutil.rmtree(build_dir)
        shutil.rmtree("build", ignore_errors=True)
        for file in Path(".").glob("*.spec"):
            file.unlink()


def build_application():
    """Build for the current platform"""
    if not os.environ.get("POETRY_ACTIVE"):
        print(
            "Must be run within Poetry environment: Use 'poetry run python build_scripts.py'"
        )
        return False

    clean_builds_dir()

    # Build using pyinstaller
    subprocess.run(
        [
            "pyinstaller",
            "--clean",
            "--windowed",
            "build_spec.py",
        ],
        check=True,
    )

    # Get output directory based on platform
    platform_name = platform.system().lower()
    if platform_name == "darwin":
        output_dir = f"dist/{_APP_NAME}.app"
    elif platform_name == "windows":
        output_dir = f"dist/{_APP_NAME}"
    else:
        output_dir = f"dist/{_APP_NAME}"

    print(f"Build completed! Output directory: {output_dir}")
    return True


if __name__ == "__main__":
    if check_requirements():
        build_application()

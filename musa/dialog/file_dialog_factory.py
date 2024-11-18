from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import QFileDialog

from .preview_image_dialog import ImageFileDialog


class FileDialogFactory:
    @staticmethod
    def open_file(file_types: str) -> Optional[Path]:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(
            None,
            "Open File...",
            "",
            file_types,
            options=options,
        )

        if file:
            return Path(file)

    @staticmethod
    def save_file(file_types: str, default_ext: str) -> Optional[Path]:
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getSaveFileName(
            None,
            "Save File As...",
            "",
            file_types,
            options=options,
        )

        if file:
            if not file.endswith(default_ext):
                file += default_ext
            return Path(file)

    @staticmethod
    def open_image() -> Optional[Path]:
        dialog = ImageFileDialog(
            None, "Open Sprite Sheet Image...", "", "Image Files (*.png)"
        )
        if dialog.exec_() == QFileDialog.accepted:
            file = dialog.selectedFiles()[0]
            return Path(file)

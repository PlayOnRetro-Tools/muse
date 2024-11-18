import os
from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout


class ImageFileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setMinimumSize(self.width() + 256, self.height())

        self.file_selected = None
        self.files_selected = None

        self.preview_label = QLabel("Preview", self)
        self.preview_label.setMinimumSize(256, 256)
        self.preview_label.setAlignment(Qt.AlignCenter)

        # Add preview to layout
        box = QVBoxLayout()
        box.addWidget(self.preview_label)
        box.addStretch()
        self.layout().addLayout(box, 1, 3, 1, 1)

        # Connect signal
        self.currentChanged.connect(self.show_preview)
        self.fileSelected.connect(self.on_file_selected)
        self.filesSelected.connect(self.on_files_selected)

    def on_file_selected(self, file: str):
        self.file_selected = file

    def on_files_selected(self, files: List[str]):
        self.files_selected = files

    def show_preview(self, path: str):
        if os.path.isfile(path):
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.preview_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.FastTransformation,
                )
                self.preview_label.setPixmap(scaled_pixmap)
            else:
                self.preview_label.setText("Not an image")
        else:
            self.preview_label.setText("Preview")

    def get_file_selected(self) -> str:
        return self.file_selected

    def get_files_selected(self) -> List[str]:
        return self.files_selected

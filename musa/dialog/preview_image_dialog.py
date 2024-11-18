import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QLabel, QVBoxLayout


class ImageFileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)
        self.setFixedSize(self.width() + 256, self.height())

        self.preview_label = QLabel("Preview", self)
        self.preview_label.setFixedSize(256, 256)
        self.preview_label.setAlignment(Qt.AlignCenter)

        # Add preview to layout
        box = QVBoxLayout()
        box.addWidget(self.preview_label)
        box.addStretch()
        self.layout().addLayout(box, 1, 3, 1, 1)

        # Connect signal
        self.currentChanged.connect(self.show_preview)

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

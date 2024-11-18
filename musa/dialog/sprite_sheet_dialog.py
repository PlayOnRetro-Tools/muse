from pathlib import Path
from typing import List

from PyQt5.QtCore import QPoint, QRegExp, Qt
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator
from PyQt5.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
)

from musa.model.types import Point, Size
from musa.util.image import Image
from musa.widget import ClickableImageLabel, ColorPickerButton


class SpriteSheetDialog(QDialog):
    def __init__(self, image_path: Path, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.image = QImage(image_path.resolve().as_posix())

        # Cache checker board image
        self.checker = Image.checker_board(self.image.size())

        self.frame_size = Size(32, 32)  # Default size
        self.offset = Point(0, 0)
        self.setup_ui()

        self.update_display()

    def setup_ui(self):
        self.setWindowTitle("Sprite Sheet Extract")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        main_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        left_layout = QVBoxLayout()

        # Alpha channel
        alpha_layout = QHBoxLayout()
        alpha_layout.addWidget(QLabel("Alpha:"))
        self.alpha_btn = ColorPickerButton(self)
        alpha_layout.addWidget(self.alpha_btn)
        left_layout.addLayout(alpha_layout)

        # Sprite sheet display
        self.scroll_area = QScrollArea()
        self.scroll_area.setMouseTracking(True)
        self.display = ClickableImageLabel(self.scroll_area)
        self.display.clickedAt.connect(self.pick_alpha_color)
        self.scroll_area.setWidget(self.display)
        left_layout.addWidget(self.scroll_area)

        # Connect signals
        self.alpha_btn.clicked.connect(lambda clicked: self.pick_alpha())

        # Frame size input
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Frame Width:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(8, self.image.width())
        self.width_spin.setValue(self.frame_size.w)
        self.width_spin.setSingleStep(8)
        self.width_spin.valueChanged.connect(self.update_frame_size)
        size_layout.addWidget(self.width_spin)

        size_layout.addWidget(QLabel("Frame Height:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(8, self.image.height())
        self.height_spin.setValue(self.frame_size.h)
        self.height_spin.setSingleStep(8)
        self.height_spin.valueChanged.connect(self.update_frame_size)
        size_layout.addWidget(self.height_spin)
        right_layout.addLayout(size_layout)

        # Offset input
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Offset X:"))
        self.offset_x_spin = QSpinBox()
        self.offset_x_spin.setRange(0, self.image.width())
        self.offset_x_spin.setValue(self.offset.x)
        self.offset_x_spin.valueChanged.connect(self.update_frame_size)
        size_layout.addWidget(self.offset_x_spin)

        size_layout.addWidget(QLabel("Offset Y:"))
        self.offset_y_spin = QSpinBox()
        self.offset_y_spin.setRange(0, self.image.height())
        self.offset_y_spin.setValue(self.offset.y)
        self.offset_y_spin.valueChanged.connect(self.update_frame_size)
        size_layout.addWidget(self.offset_y_spin)
        right_layout.addLayout(size_layout)

        # Base name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Base Name:"))
        self.base_name = QLineEdit("sprite")
        self.base_name.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9_()]*")))
        name_layout.addWidget(self.base_name)
        right_layout.addLayout(name_layout)

        # Buttons
        button_layout = QHBoxLayout()
        extract_btn = QPushButton("Extract")
        extract_btn.clicked.connect(self.validate_extract)
        button_layout.addWidget(extract_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        right_layout.addLayout(button_layout)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def pick_alpha(self):
        self.display.toggle_click()

    def pick_alpha_color(self, pos: QPoint):
        self.display.toggle_click()
        color = self.image.pixelColor(pos.x(), pos.y())
        self.alpha_btn.set_color(color)

        # Update the image
        self.image = Image.remove_background(self.image, color)
        self.update_display()

    def update_frame_size(self):
        self.frame_size = Size(self.width_spin.value(), self.height_spin.value())
        self.offset = Point(self.offset_x_spin.value(), self.offset_y_spin.value())
        self.update_display()

    def update_display(self):
        pixmap = QPixmap.fromImage(self.image)
        grid = Image.grid(
            pixmap.size(),
            self.frame_size.w,
            self.frame_size.h,
            self.offset.x,
            self.offset.y,
        )

        result = Image.flatten([self.checker, pixmap, grid], pixmap.size())
        self.display.setFixedSize(result.size())
        self.display.setPixmap(result)

    def validate_extract(self):
        width = self.width_spin.value()
        height = self.height_spin.value()

        if self.image.width() % width != 0 or self.image.height() % height != 0:
            QMessageBox.warning(
                self,
                "Invalid Dimensions",
                "Image Dimensions must be a multiple of frame size!",
            )
            return

        self.sprites = self.get_sprites()

    def get_sprites(self) -> List[QPixmap]:
        return Image.extract_sprites(
            self.image,
            self.frame_size.w,
            self.frame_size.h,
            self.offset.x,
            self.offset.y,
        )

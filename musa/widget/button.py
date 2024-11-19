from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton

from musa.util.image import Image


class ColorPickerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = None
        self.setFixedSize(24, 24)
        self.setCursor(Qt.PointingHandCursor)

        # Initial icon
        pixmap = Image.checker_board(self.size(), 4)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(self.size())

    def update_color(self):
        pixmap = QPixmap(self.size())
        pixmap.fill(self.color)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(self.size())

    def set_color(self, color: QColor):
        self.color = color
        self.update_color()

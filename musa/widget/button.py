from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QIcon, QLinearGradient, QPainter, QPixmap
from PyQt5.QtWidgets import QPushButton

from musa.util.image import Image


class AlphaColorPickerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(36, 20)
        self.setCursor(Qt.PointingHandCursor)

        # Current transparent color
        self.color: QColor = None

        # Initial icon
        self.checker = Image.checker_board(self.size(), 4)
        self.setIcon(QIcon(self.checker))
        self.setIconSize(self.size())

    def update_color(self):
        pixmap = QPixmap(self.checker)
        gradient = QLinearGradient(0, 0, 48, 16)
        gradient.setColorAt(
            0, QColor(self.color.red(), self.color.green(), self.color.blue(), 255)
        )
        gradient.setColorAt(
            1, QColor(self.color.red(), self.color.green(), self.color.blue(), 0)
        )

        painter = QPainter(pixmap)
        painter.fillRect(pixmap.rect(), QBrush(gradient))
        painter.end()

        self.setIcon(QIcon(pixmap))
        self.setIconSize(self.size())

    def set_color(self, color: QColor):
        self.color = color
        self.update_color()

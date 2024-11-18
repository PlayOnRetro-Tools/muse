from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton


class ClickableImageLabel(QLabel):
    clickedAt = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.can_click = False

    def toggle_click(self):
        self.can_click = not self.can_click
        if self.can_click:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        if self.can_click and event.button() == Qt.LeftButton:
            self.clickedAt.emit(event.pos())
        super().mousePressEvent(event)


class ColorPickerButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor(255, 0, 255, 255)  # Defaults to magenta
        self.setFixedSize(32, 32)
        self.setCursor(Qt.PointingHandCursor)
        self.update_color()

    def update_color(self):
        pixmap = QPixmap(self.size())
        pixmap.fill(self.color)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(self.size())

    def set_color(self, color: QColor):
        self.color = color
        self.update_color()

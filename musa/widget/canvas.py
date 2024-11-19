from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget


class Magnifier(QWidget):
    """Magnifiying lens"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.source_pixmap = None
        self.magnified_pos = QPoint()
        self.zoom_factor = 10
        self.size = 128

        self.setFixedSize(self.size, self.size)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def set_source_pixmap(self, pixmap: QPixmap):
        self.source_pixmap = pixmap

    def update_magnified_area(self, pos: QPoint):
        self.magnified_pos = pos
        self.update()

    def paintEvent(self, event):
        if not self.source_pixmap:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Create clipping path
        path = QPainterPath()
        path.addEllipse(0, 0, self.size, self.size)
        painter.setClipPath(path)

        # compute area to magnify
        size = self.size / self.zoom_factor
        x = self.magnified_pos.x() - size / 2
        y = self.magnified_pos.y() - size / 2

        # Extract and scale the source area
        source_rect = self.source_pixmap.rect()
        x = max(0, min(x, source_rect.width() - size))
        y = max(0, min(y, source_rect.height() - size))

        area = self.source_pixmap.copy(int(x), int(y), int(size), int(size))
        scaled = area.scaled(
            self.size, self.size, Qt.KeepAspectRatio, Qt.FastTransformation
        )

        # Draw the magnified image
        painter.drawPixmap(0, 0, scaled)

        # Draw Crosshair
        painter.setPen(QPen(QColor(255, 255, 255), 1.5))
        center = self.size // 2
        # Horizontal
        painter.drawLine(center - 10, center, center + 10, center)
        # Vertical
        painter.drawLine(center, center - 10, center, center + 10)

        # Draw coordinates
        painter.setFont(QFont("Arial", 8))
        text = f"({self.magnified_pos.x()}, {self.magnified_pos.y()})"

        metrics = painter.fontMetrics()
        text_width = metrics.width(text)
        text_height = metrics.height()
        text_x = (self.size - text_width) // 2
        text_y = self.size - 20

        # Text bacground
        painter.fillRect(
            text_x - 2,
            text_y - text_height,
            text_width + 4,
            text_height + 2,
            QColor(0, 0, 0, 127),
        )

        # Draw text
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(text_x, text_y, text)

        # Draw border
        painter.setPen(QPen(QColor(0, 0, 0, 127), 1.5))
        painter.drawEllipse(0, 0, self.size - 1, self.size - 1)


class MagnifiyingCanvasLabel(QLabel):
    clicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.can_click = False
        self.magnifier = Magnifier(self)
        self.magnifier.hide()
        self.setMouseTracking(True)

    def toggle_click(self):
        self.can_click = not self.can_click
        if self.can_click:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)
        if self.magnifier:
            self.magnifier.set_source_pixmap(pixmap)

    def mousePressEvent(self, event):
        if self.can_click and event.button() == Qt.LeftButton:
            self.clicked.emit(event.pos())
            self.magnifier.hide()
        elif event.button() == Qt.RightButton:
            self.magnifier.hide()
            self.can_click = False
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.can_click:
            return

        pos = event.pos()
        scaled_pos = self._get_scaled_position(pos)
        if scaled_pos is None:
            self.magnifier.hide()
            return

        global_pos = self.mapToGlobal(pos)
        self.magnifier.move(global_pos + QPoint(20, 20))
        self.magnifier.update_magnified_area(scaled_pos)
        self.magnifier.show()

    def leaveEvent(self, event):
        self.magnifier.hide()

    def _get_scaled_position(self, pos):
        if not self.can_click:
            return None

        img_rect = self._get_scaled_rect()

        if not img_rect.contains(pos):
            return None

        x_ratio = (pos.x() - img_rect.left()) / img_rect.width()
        y_ratio = (pos.y() - img_rect.top()) / img_rect.height()

        original_x = int(x_ratio * self.pixmap().width())
        original_y = int(y_ratio * self.pixmap().height())

        return QPoint(original_x, original_y)

    def _get_scaled_rect(self):
        if not self.can_click:
            return None

        img_ratio = self.pixmap().width() / self.pixmap().height()
        label_ratio = self.width() / self.height()

        if img_ratio > label_ratio:
            w = self.width()
            h = int(w / img_ratio)
            x = 0
            y = (self.height() - w) // 2
        else:
            h = self.height()
            w = int(h * img_ratio)
            x = (self.width() - w) // 2
            y = 0

        return self.rect().adjusted(x, y, -x, -y)

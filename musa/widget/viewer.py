from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel, QWidget


class Magnifier(QWidget):
    """Magnifiying lens"""

    def __init__(self, parent=None, zoom_factor: int = 8, radius: int = 64):
        super().__init__(parent)

        self.lens_size = radius * 2
        self.magnified_pos = QPoint()
        self.zoom_factor = zoom_factor
        self.source_pixmap: QPixmap = None

        self.setFixedSize(self.lens_size, self.lens_size)
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
        path.addEllipse(0, 0, self.lens_size, self.lens_size)
        painter.setClipPath(path)

        # compute area to magnify
        size = self.lens_size / self.zoom_factor

        # Rectangle at x,y with center at mouse coords
        x = int(self.magnified_pos.x() - size / 2)
        y = int(self.magnified_pos.y() - size / 2)

        # Extract and scale the source area
        source_rect = self.source_pixmap.rect()

        # Adjust the size of the copy if we are at the edges

        # x = max(0, min(x, source_rect.width() - size))
        # y = max(0, min(y, source_rect.height() - size))

        area = self.source_pixmap.copy(x, y, int(size), int(size))
        scaled = area.scaled(
            self.lens_size, self.lens_size, Qt.KeepAspectRatio, Qt.FastTransformation
        )

        # Compose the final image accounting for source image edges
        result = QPixmap(self.lens_size, self.lens_size)
        result.fill(Qt.black)
        pix = QPainter(result)
        pix.drawPixmap(0, 0, scaled)
        pix.end()

        painter.drawPixmap(0, 0, result)

        # Draw Crosshair
        pen = QPen(QColor(255, 255, 255), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        center = self.lens_size // 2

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
        text_x = (self.lens_size - text_width) // 2
        text_y = self.lens_size - 20

        # Text background
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
        painter.drawEllipse(0, 0, self.lens_size - 1, self.lens_size - 1)


class ImageViewer(QLabel):
    clicked = pyqtSignal(object)
    zoomChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.can_click = False

        # Zoom parameters
        self.zoom_factor = 1.0
        self.min_zoom = 1.0
        self.max_zoom = 8.0
        self.zoom_step = 0.1

        # Original pixmap
        self.original_pixmap: QPixmap = None

        # Magnifier setup
        self.magnifier = Magnifier(self)
        self.magnifier.hide()

        # Hover and zoom tracking
        self.setMouseTracking(True)

    def toggle_click(self):
        self.can_click = not self.can_click
        if self.can_click:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def setPixmap(self, pixmap: QPixmap):
        """Set the original pixmap"""
        self.original_pixmap = pixmap
        self._update_displayed_pixmap()

        if self.magnifier:
            self.magnifier.set_source_pixmap(pixmap)

    def set_zoom(self, zoom_level: float):
        self.zoom_factor = max(self.min_zoom, min(self.max_zoom, zoom_level))
        self._update_displayed_pixmap()

    def _update_displayed_pixmap(self):
        """Apply zoom and update pixmap"""
        if not self.original_pixmap:
            return

        # Scale the pixmap
        transform = QTransform()
        transform.scale(self.zoom_factor, self.zoom_factor)

        # Apply zoom
        zoomed_pixmap = self.original_pixmap.transformed(transform)
        super().setPixmap(zoomed_pixmap)

        self.zoomChanged.emit(self.zoom_factor)

    def mousePressEvent(self, event):
        if self.can_click and event.button() == Qt.LeftButton:
            original_pos = self._map_to_original_coords(event.pos())

            if original_pos:
                self.clicked.emit(original_pos)
                self.magnifier.hide()

        elif event.button() == Qt.RightButton:
            self.magnifier.hide()
            self.toggle_click()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not self.can_click:
            return

        scaled_pos = self._map_to_original_coords(event.pos())

        if scaled_pos is None:
            self.magnifier.hide()
            return

        global_pos = self.mapToGlobal(event.pos())
        self.magnifier.move(global_pos + QPoint(16, -16))
        self.magnifier.update_magnified_area(scaled_pos)
        self.magnifier.show()

    def leaveEvent(self, event):
        self.magnifier.hide()

    def _map_to_original_coords(self, pos) -> QPoint:
        """Map mouse widget coordinates to original image coordinates"""

        if not self.original_pixmap:
            return None

        pixmap_pos = pos - self._get_pixmap_offset()

        # Account for scaling
        point = QPoint(
            int(pixmap_pos.x() / self.zoom_factor),
            int(pixmap_pos.y() / self.zoom_factor),
        )

        # Point within image bounds?
        if self.original_pixmap.rect().contains(point):
            return point
        return None

    def _get_pixmap_offset(self) -> QPoint:
        if not self.pixmap():
            return QPoint(0, 0)

        # Get the scaled size
        scaled_size = self.pixmap().size()

        # Offset to center
        return QPoint(
            (self.width() - scaled_size.width()) // 2,
            (self.height() - scaled_size.height()) // 2,
        )

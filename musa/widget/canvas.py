from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QPainter, QPainterPath, QPen, QPixmap, QTransform
from PyQt5.QtWidgets import QLabel, QWidget


class Magnifier(QWidget):
    """Magnifiying lens"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.source_pixmap = None
        self.magnified_pos = QPoint()
        self.zoom_factor = 12
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
        pen = QPen(QColor(255, 255, 255), 1.5)
        pen.setCosmetic(True)
        painter.setPen(pen)
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
        painter.drawEllipse(0, 0, self.size - 1, self.size - 1)


class MagnifiyingCanvasLabel(QLabel):
    clicked = pyqtSignal(object)
    zoomChanged = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.can_click = False

        # Zoom parameters
        self.current_zoom = 1.0
        self.min_zoom = 1.0
        self.max_zoom = 5.0
        self.zoom_step = 0.1

        # Original pixmap
        self.original_pixmap = None

        # Magnifier setup
        self.magnifier = Magnifier(self)
        self.magnifier.hide()

        # Hover and zoom tracking
        self.setMouseTracking(True)

        # Tracking pan
        self.pan_start = QPoint()
        self.current_pan = QPoint()
        self.is_panning = False

    def toggle_click(self):
        self.can_click = not self.can_click
        if self.can_click:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def setPixmap(self, pixmap: QPixmap):
        """Set the original pixmap and initialize zoom"""
        self.original_pixmap = pixmap
        self.current_pan = QPoint()
        self._update_displayed_pixmap()

        if self.magnifier:
            self.magnifier.set_source_pixmap(pixmap)

    def _update_displayed_pixmap(self):
        """Apply zoom and update pixmap"""
        if not self.original_pixmap:
            return

        # Create transform pixmap
        transform = QTransform()
        transform.scale(self.current_zoom, self.current_zoom)

        # Apply zoom and pan
        zoomed_pixmap = self.original_pixmap.transformed(transform)
        super().setPixmap(zoomed_pixmap)

        self.zoomChanged.emit(self.current_zoom)

    def set_zoom(self, zoom_level: float):
        self.current_zoom = max(self.min_zoom, min(self.max_zoom, zoom_level))
        self._update_displayed_pixmap()

    def wheelEvent(self, event):
        # Zoom with Ctrl Key
        if event.modifiers() & Qt.ControlModifier:
            # Zoom direction
            zoom_delta = (
                self.zoom_step if event.angleDelta().y() > 0 else -self.zoom_step
            )

            # Calculate new zoom
            new_zoom = self.current_zoom + zoom_delta
            new_zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))

            # Update zoom
            self.current_zoom = new_zoom
            self._update_displayed_pixmap()

    def mousePressEvent(self, event):
        if self.can_click and event.button() == Qt.LeftButton:
            # Emit click position in original image coordinates
            original_pos = self._map_to_original_coords(event.pos())

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

    def _map_to_original_coords(self, pos):
        """Convert widget coordinates to original image coordinates"""
        if not self.original_pixmap:
            return None

        img_width = self.original_pixmap.width() * self.current_zoom
        img_height = self.original_pixmap.height() * self.current_zoom

        # Point within image bounds?
        if pos.x() < 0 or pos.x() > img_width or pos.y() < 0 or pos.y() > img_height:
            return None

        original_x = int(pos.x() / self.current_zoom)
        original_y = int(pos.y() / self.current_zoom)

        return QPoint(original_x, original_y)

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

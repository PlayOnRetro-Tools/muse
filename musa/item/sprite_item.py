from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem


class SpriteItem(QGraphicsPixmapItem):
    def __init__(self, pixmap: QPixmap, parent=None):
        super().__init__(pixmap, parent)
        self.setFlag(QGraphicsPixmapItem.ItemIsMovable)
        self.setFlag(QGraphicsPixmapItem.ItemIsSelectable)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)

        if event.button() == Qt.LeftButton and event.modifiers() & Qt.ControlModifier:
            # Snap to grid
            pos = self.pos()
            grid_size = 8
            self.setPos(
                round(pos.x() / grid_size) * grid_size,
                round(pos.y() / grid_size) * grid_size,
            )

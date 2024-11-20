from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from musa.item import SpriteItem


class EditorScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        size = 512
        self.setSceneRect(-size / 2, -size / 2, size, size)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            image = QImage(event.mimeData().imageData())

            # Convert the event to scene coordinates
            pos = event.scenePos()

            # Create the sprite item
            item = SpriteItem(QPixmap.fromImage(image))
            item.setPos(pos)
            self.addItem(item)

            event.acceptProposedAction()


class EditorView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setAcceptDrops(True)
        self.setRenderHint(QPainter.Antialiasing)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

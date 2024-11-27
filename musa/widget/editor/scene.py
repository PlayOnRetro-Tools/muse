from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene

from musa.model.animation import Animation
from musa.model.frame import Frame
from musa.model.sprite import Sprite
from musa.widget.editor.item import SpriteItem


class EditorScene(QGraphicsScene):
    _SIZE = 256

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSceneRect(-self._SIZE / 2, -self._SIZE / 2, self._SIZE, self._SIZE)
        self.connections()

        self.scratch_pad_frame = Frame()
        self.current_frame: Frame = None
        self.current_animation: Animation = None

    def set_frame(self, frame: Frame):
        self.current_frame = frame

    def set_animation(self, animation: Animation):
        self.current_animation = animation

    def connections(self):
        self.selectionChanged.connect(self._on_selection_changed)

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

            # Create the sprite item and model data
            offset_x = image.size().width() // 2
            offset_y = image.size().height() // 2

            pos = pos - QPoint(offset_x, offset_y)
            sprite = Sprite(x=pos.x(), y=pos.y())

            item = SpriteItem(QPixmap.fromImage(image), sprite.id)
            item.setPos(pos)

            self.addItem(item)
            self.scratch_pad_frame.add_sprite(sprite)

            event.acceptProposedAction()

    def _on_selection_changed(self):
        pass

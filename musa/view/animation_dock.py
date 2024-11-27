from PyQt5.QtWidgets import QHBoxLayout, QWidget

from musa.model.animation_collection import AnimationCollection
from musa.widget.animation_list import AnimationListWidget
from musa.widget.frame_list import FrameListWidget
from musa.widget.sprite_list import SpriteListWidget


class AnimationDock(QWidget):
    def __init__(self, collection: AnimationCollection, parent=None):
        super().__init__(parent)
        self.collection = collection
        self.setup_ui()
        self.connections()

    def setup_ui(self):
        layout = QHBoxLayout()

        self.animation_list = AnimationListWidget(self.collection)
        self.frame_list = FrameListWidget()
        self.sprite_list = SpriteListWidget()

        layout.addWidget(self.animation_list, 1)
        layout.addWidget(self.frame_list, 1)
        layout.addWidget(self.sprite_list, 2)

        self.setLayout(layout)

    def connections(self):
        self.animation_list.animationSelected.connect(self.frame_list.set_animation)
        self.frame_list.frameSelected.connect(self.sprite_list.set_frame)

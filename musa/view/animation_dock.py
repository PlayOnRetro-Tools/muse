from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QWidget

from musa.model.animation import Animation
from musa.model.animation_collection import AnimationCollection
from musa.model.frame import Frame
from musa.widget.animation_list import AnimationListWidget
from musa.widget.frame_list import FrameListWidget


class AnimationDock(QWidget):
    frameSelected = pyqtSignal(Frame)
    animationSelected = pyqtSignal(Animation)

    def __init__(self, collection: AnimationCollection, parent=None):
        super().__init__(parent)
        self.collection = collection
        self.setup_ui()
        self.connections()

    def setup_ui(self):
        layout = QHBoxLayout()

        self.animation_list = AnimationListWidget(self.collection)
        self.frame_list = FrameListWidget()

        layout.addWidget(self.animation_list, 1)
        layout.addWidget(self.frame_list, 1)

        self.setLayout(layout)

    def connections(self):
        self.animation_list.animationSelected.connect(self.frame_list.set_animation)
        self.animation_list.animationSelected.connect(self.animationSelected)
        self.frame_list.frameSelected.connect(self.frameSelected)

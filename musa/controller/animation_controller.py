from PyQt5.QtCore import QObject, pyqtSignal

from musa.model.animation import AnimationsModel


class AnimationController(QObject):
    def __init__(self, model: AnimationsModel):
        super().__init__()
        self.model = model

    def add_frame(self, index: int):
        pass

    def add_animation(self):
        pass

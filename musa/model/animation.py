from dataclasses import dataclass, field
from typing import Dict, Iterator, List

from PyQt5.QtCore import QObject, pyqtSignal

from .frame import Frame
from .iterator import CollectionIterator, T
from .serializable import Serializable


@dataclass
class Animation(Serializable):
    frames: List[Frame] = field(default_factory=list)

    def add_frame(self, frame: Frame):
        self.frames.append(frame)

    def remove_frame(self, frame: Frame):
        index = self.frames.index(frame)
        self.frames.pop(index)

    def get_frame(self, index: int) -> Frame:
        return self.frames[index]

    def __iter__(self) -> Iterator[T]:
        return CollectionIterator(self.frames)


class AnimationsModel(QObject):
    createdAnimation = pyqtSignal(str)
    removedAnimation = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.animations: Dict[str, Animation] = {}

    def create_animation(self, name: str) -> Animation:
        if name not in self.animations:
            self.animations[name] = Animation(name=name)
            self.createdAnimation.emit(name)
            return self.get_animation(name)

    def remove_animation(self, name: str):
        self.animations.pop(name)
        self.removedAnimation.emit(name)

    def get_animation(self, name: str) -> Animation:
        return self.animations.get(name, None)

    def get_animations(self) -> List[str]:
        return list(self.animations.keys())

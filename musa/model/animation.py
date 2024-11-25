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

    def __iter__(self) -> Iterator[T]:
        return CollectionIterator(self.frames)


class AnimationsModel(QObject):
    addedAnimation = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.animations: Dict[str, Animation] = {}

    def add_animation(self, name: str):
        if name not in self.animations:
            self.animations[name] = Animation(name=name)
            self.addedAnimation.emit(name)

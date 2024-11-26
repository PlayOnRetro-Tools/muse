from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional, Set
from uuid import UUID

from .frame import Frame
from .iterator import CollectionIterator, I
from .observable import AnimationSignals
from .serializable import Serializable, T


@dataclass
class Animation(Serializable):
    name: str = ""
    frames: List[Frame] = field(default_factory=list)
    signals: AnimationSignals = field(default_factory=AnimationSignals, init=False)
    _modified_frames: Set[UUID] = field(default_factory=set, init=False)

    @classmethod
    def from_dict(cls: type[T], data: Dict[str, Any]) -> "Animation":
        frames_data = data.pop("frames", [])
        animation = super().from_dict(data)
        animation.frames = [Frame.from_dict(f) for f in frames_data]
        return animation

    def add_frame(self, frame: Frame) -> None:
        self.frames.append(frame)
        self.signals.frameAdded.emit(self.id)
        self.signals.animationModified.emit(self.id)

    def remove_frame(self, frame_id: UUID) -> Optional[Frame]:
        for i, frame in enumerate(self.frames):
            if frame.id == frame_id:
                frame = self.frames.pop(i)
                self.signals.frameRemoved.emit(self.id, frame_id)
                self.signals.animationModified.emit(self.id)
                return frame
        return None

    def get_frame(self, frame_id: UUID) -> Optional[Frame]:
        return next((f for f in self.frames if f.id == frame_id), None)

    def update_frame(self, frame_id: UUID, **kwargs) -> bool:
        if frame := self.get_frame(frame_id):
            for key, value in kwargs.items():
                if hasattr(frame, key):
                    setattr(frame, key, value)
            self.signals.frameModified.emit(self.id, frame_id)
            self.signals.animationModified.emit(self.id)
            return True
        return False

    def mark_frame_modified(self, frame_id: UUID):
        self._modified_frames.add(frame_id)
        self.signals.frameModified.emit(self.id, frame_id)
        self.signals.animationModified.emit(self.id)

    def commit_frame_changes(self):
        for frame in self.frames:
            if frame.is_modified:
                self.mark_frame_modified(frame.id)
            frame.clear_modified_flag()
        self._modified_frames.clear()

    @property
    def total_ticks(self) -> int:
        return sum(frame.ticks for frame in self.frames)

    def __iter__(self) -> Iterator[I]:
        return CollectionIterator(self.frames)

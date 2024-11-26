from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional
from uuid import UUID

from .frame import Frame
from .iterator import CollectionIterator, I
from .serializable import Serializable, T


@dataclass
class Animation(Serializable):
    name: str = ""
    frames: List[Frame] = field(default_factory=list)

    @classmethod
    def from_dict(cls: type[T], data: Dict[str, Any]) -> "Animation":
        frames_data = data.pop("frames", [])
        animation = super().from_dict(data)
        animation.frames = [Frame.from_dict(f) for f in frames_data]
        return animation

    def add_frame(self, frame: Frame) -> None:
        self.frames.append(frame)

    def remove_frame(self, frame_id: UUID) -> Optional[Frame]:
        for i, frame in enumerate(self.frames):
            if frame.id == frame_id:
                return self.frames.pop(i)
        return None

    def get_frame(self, frame_id: UUID) -> Optional[Frame]:
        return next((f for f in self.frames if f.id == frame_id), None)

    @property
    def total_ticks(self) -> int:
        return sum(frame.ticks for frame in self.frames)

    def __iter__(self) -> Iterator[I]:
        return CollectionIterator(self.frames)


# class AnimationDataModel:
#     # ... (Previous methods remain the same) ...

#     def set_sprite_property(self, animation_index, frame_index, sprite_index, property_name, value):
#         """Update a sprite property"""
#         pass

#     def move_sprite(self, animation_index, frame_index, from_index, to_index):
#         """Move a sprite in the z-order"""
#         pass

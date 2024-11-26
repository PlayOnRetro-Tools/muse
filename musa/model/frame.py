from dataclasses import dataclass, field
from typing import Any, Dict, Iterator, List, Optional
from uuid import UUID

from .iterator import CollectionIterator, I
from .serializable import Serializable, T
from .sprite import Sprite


@dataclass
class Frame(Serializable):
    name: str = ""
    ticks: int = 1
    sprites: List[Sprite] = field(default_factory=list)

    @classmethod
    def from_dict(cls: type[T], data: Dict[str, Any]) -> "Frame":
        sprites_data = data.pop("sprites", [])
        frame = super().from_dict(data)
        frame.sprites = [Sprite.from_dict(s) for s in sprites_data]
        return frame

    def add_sprite(self, sprite: Sprite) -> None:
        self.sprites.append(sprite)

    def remove_sprite(self, sprite_id: UUID) -> Optional[Sprite]:
        for i, sprite in enumerate(self.sprites):
            if sprite.id == sprite_id:
                return self.sprites.pop(i)
        return None

    def get_sprite(self, sprite_id: UUID) -> Optional[Sprite]:
        return next((s for s in self.sprites if s.id == sprite_id), None)

    def __iter__(self) -> Iterator[I]:
        return CollectionIterator(self.sprites)

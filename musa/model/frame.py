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
    _modified: bool = field(default=False, init=False)

    @classmethod
    def from_dict(cls: type[T], data: Dict[str, Any]) -> "Frame":
        sprites_data = data.pop("sprites", [])
        frame = super().from_dict(data)
        frame.sprites = [Sprite.from_dict(s) for s in sprites_data]
        return frame

    def add_sprite(self, sprite: Sprite) -> None:
        self.sprites.append(sprite)
        self._modified = True

    def remove_sprite(self, sprite_id: UUID) -> Optional[Sprite]:
        for i, sprite in enumerate(self.sprites):
            if sprite.id == sprite_id:
                self._modified = True
                return self.sprites.pop(i)
        return None

    def update_sprite(self, sprite_id: UUID, **kwargs) -> bool:
        if sprite := self.get_sprite(sprite_id):
            if sprite.update(**kwargs):
                self._modified = True
                return True
        return False

    def get_sprite(self, sprite_id: UUID) -> Optional[Sprite]:
        return next((s for s in self.sprites if s.id == sprite_id), None)

    def clear_modified_flag(self):
        self._modified = False

    @property
    def is_modified(self) -> bool:
        return self._modified

    def __iter__(self) -> Iterator[I]:
        return CollectionIterator(self.sprites)

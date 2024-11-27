from dataclasses import dataclass

from .serializable import Serializable


@dataclass
class Sprite(Serializable):
    name: str = ""
    x: int = 0
    y: int = 0
    h_flip: bool = False
    v_flip: bool = False
    sprite_index: int = 0
    z_index: int = 0
    opacity: float = 1.0
    visible: bool = True

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

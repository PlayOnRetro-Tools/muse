from dataclasses import dataclass

from .serializable import Serializable


@dataclass
class Piece(Serializable):
    x: int = 0
    y: int = 0
    h_flip: bool = False
    v_flip: bool = False
    sprite_index: int = 0

    def update(self, x: int, y: int, h_flip: bool, v_flip: bool, sprite: int):
        self.x = x
        self.y = y
        self.h_flip = h_flip
        self.v_flip = v_flip
        self.sprite_index = sprite

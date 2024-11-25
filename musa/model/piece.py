from dataclasses import dataclass

from .serializable import Serializable


@dataclass
class Piece(Serializable):
    x: int = 0
    y: int = 0
    h_flip: bool = False
    v_flip: bool = False
    sprite_index: int = 0
    z_index: int = 0

from dataclasses import dataclass, field
from typing import Iterator, List

from .iterator import CollectionIterator, T
from .piece import Piece
from .serializable import Serializable


@dataclass
class Frame(Serializable):
    pieces: List[Piece] = field(default_factory=list)
    length_ticks: int = 1

    def add_piece(self, piece: Piece):
        self.pieces.append(piece)

    def remove_piece(self, piece: Piece):
        index = self.pieces.index(piece)
        self.pieces.pop(index)

    def get_piece(self, index: int) -> Piece:
        return self.pieces[index]

    def __iter__(self) -> Iterator[T]:
        return CollectionIterator(self.pieces)

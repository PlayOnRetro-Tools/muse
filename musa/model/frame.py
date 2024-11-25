from typing import Dict, Iterator, List

from .iterator import CollectionIterator, T
from .piece import Piece
from .serializable import Serializable


class Frame(Serializable):
    def __init__(self, name: str, pieces: List[Piece] = None, ticks: int = 1):
        super().__init__(name=name)
        self.pieces: Dict[str, Piece] = {}
        self.ticks = ticks

        if pieces:
            self.pieces = {piece.name: piece for piece in pieces}

    def get_piece(self, name: str):
        return self.pieces.get(name)

    def add_piece(self, piece: Piece):
        self.pieces.append(piece)

    def remove_piece(self, piece: Piece):
        index = self.pieces.index(piece)
        self.pieces.pop(index)

    def __iter__(self) -> Iterator[T]:
        return CollectionIterator(list(self.pieces.values()))

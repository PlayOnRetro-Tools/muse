from typing import Generic, List, TypeVar

I = TypeVar("I")


class CollectionIterator(Generic[I]):
    def __init__(self, collection: List[I]):
        self.collection = collection
        self.index = 0

    def __next__(self) -> I:
        if self.index < len(self.collection):
            item = self.collection[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration()

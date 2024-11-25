from typing import Generic, List, TypeVar

T = TypeVar("T")


class CollectionIterator(Generic[T]):
    def __init__(self, collection: List[T]):
        self.collection = collection
        self.index = 0

    def __next__(self) -> T:
        if self.index < len(self.collection):
            item = self.collection[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration()

from binheapnode import *


TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


class BinomialHeap(Generic[TKey, TValue]):
    def __init__(self, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        self._head = None
        self._length = 0

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __len__(self) -> int:
        return self._length

    def insert(self, key: TKey, value: TValue) -> None:
        self._length += 1
        self._head = merge(BinHeapNode(key, value), self._head)

    def extract_min(self) -> Tuple[TKey, TValue]:
        if self._head is None:
            raise IndexError('Empty heap')

        self._length -= 1

        min_prev, minimum = min_and_prev(self._head)

        if min_prev is None:
            self._head = minimum.rt_sibling
        else:
            min_prev.rt_sibling = minimum.rt_sibling

        self._head = merge(self._head, child_heap(minimum))

        return (minimum.key, minimum.value)

    def get_minimum(self) -> Tuple[TKey, TValue]:
        if self._head is None:
            raise IndexError('Empty heap')

        _, minimum = min_and_prev(self._head)
        return (minimum.key, minimum.value)

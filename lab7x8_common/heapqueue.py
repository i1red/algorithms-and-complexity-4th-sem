from lab8_fibonacci_heap.fibonacciheap import FibonacciHeap
from lab7_binomial_heap.binomialheap import BinomialHeap
from typing import *


TPriority = TypeVar('TPriority')
TValue = TypeVar('TValue')


class PriorityQueue(Generic[TPriority, TValue]):
    def __init__(self, heap_type: Union[Type[FibonacciHeap], Type[BinomialHeap]] = BinomialHeap) -> None:
        self._heap = heap_type()
        self._counter = 0

    def __len__(self) -> int:
        return len(self._heap)

    def push(self, priority: TPriority, value: TValue) -> None:
        self._heap.insert((priority, self._counter), value)
        self._counter += 1

    def pop(self) -> Tuple[TPriority, TValue]:
        key, val = self._heap.extract_min()
        return (key[0], val)

    def top(self) -> Tuple[TPriority, TValue]:
        key, val = self._heap.get_minimum()
        return (key[0], val)

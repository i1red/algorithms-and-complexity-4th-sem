import functools
from lab8_fibonacci_heap.fibonacciheap import FibonacciHeap
from lab7_binomial_heap.binomialheap import BinomialHeap
from lab7_binomial_heap.binheapnode import merge
from utils.heap import HeapMixin
from typing import TypeVar


Heap = TypeVar('Heap', FibonacciHeap, BinomialHeap)


def _move_heap_refs(lt: HeapMixin, rt: HeapMixin, result: HeapMixin) -> None:
    result._refs.update(lt._refs)
    result._refs.update(rt._refs)
    lt._refs.clear()
    rt._refs.clear()

def _move_heap_len(lt: Heap, rt: Heap, result: Heap) -> None:
    result._length = lt._length + rt._length
    lt._length = rt._length = 0


@functools.singledispatch
def move_heaps(lt, rt):
    raise NotImplementedError


@move_heaps.register
def _(lt: FibonacciHeap, rt: FibonacciHeap) -> FibonacciHeap:
    result = FibonacciHeap()

    _move_heap_refs(lt, rt, result)
    _move_heap_len(lt, rt, result)

    lt_min, rt_min = lt._min, rt._min
    lt._min = rt._min = None

    if lt_min is not None and rt_min is not None:
        lt_right, rt_left = lt_min.right, rt_min.left
        lt_right.left, rt_left.right = rt_left, lt_right
        lt_min.right, rt_min.left = rt_min, lt_min
        result._min = lt_min if lt_min.key < rt_min.key else rt_min
    elif lt_min is not None:
        result._min = lt_min
    elif rt_min is not None:
        result._min = rt_min

    return result


@move_heaps.register
def _(lt: BinomialHeap, rt: BinomialHeap) -> BinomialHeap:
    result = BinomialHeap()

    _move_heap_refs(lt, rt, result)
    _move_heap_len(lt, rt, result)

    result._head = merge(lt._head, rt._head)
    lt._head = rt._head = None

    return result

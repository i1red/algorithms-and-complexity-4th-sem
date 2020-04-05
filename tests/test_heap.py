import pytest
import random
from lab8_fibonacci_heap.fibonacciheap import FibonacciHeap
from lab7_binomial_heap.binomialheap import BinomialHeap
from lab8x9_common.moveheaps import move_heaps


BOUND = 1000
SORTED_INPUT = sorted([(random.randint(-BOUND, BOUND), random.randint(-BOUND, BOUND)) for _ in range(BOUND)])
SHUFFLED_INPUT = [(random.randint(-BOUND, BOUND), random.randint(-BOUND, BOUND)) for _ in range(BOUND)]


@pytest.fixture(params=[lambda: move_heaps(FibonacciHeap(SHUFFLED_INPUT), FibonacciHeap(SORTED_INPUT)),
                        lambda: move_heaps(BinomialHeap(SHUFFLED_INPUT), BinomialHeap(SORTED_INPUT))])
def heap(request):
    return request.param()


def test_extract_min(heap):
    keys = []
    length = len(heap)

    while len(heap) > 0:
        key, _ = heap.extract_min()
        keys.append(key)
        length -= 1

        assert len(heap) == length

    assert sorted(keys) == keys


def test_extract_min_empty_heap(heap):
    while len(heap) > 0:
        heap.extract_min()

    with pytest.raises(IndexError):
        heap.extract_min()


def test_getitem(heap):
    items = []

    for i in range(len(heap)):
        item_ref = heap[i]
        items.append((item_ref.key, item_ref.value))

    assert sorted(items) == sorted(SORTED_INPUT + SHUFFLED_INPUT)


def test_decrease_key(heap):
    ref = heap[len(heap) // 2]
    new_key = -BOUND - 1

    assert heap.decrease_key(ref, new_key)
    assert ref.key == new_key
    assert heap.get_minimum()[0] == new_key


def test_references(heap):
    index = len(heap) // 2
    first_ref = heap[index]
    second_ref = heap[index]

    heap.remove(first_ref)

    assert first_ref is second_ref
    assert not first_ref.is_valid() and not second_ref.is_valid()

from fibonacciheap import FibonacciHeap
import random


BOUND = 1000
SORTED_INPUT = sorted([(random.randint(-BOUND, BOUND), random.randint(-BOUND, BOUND)) for _ in range(BOUND)])


def test_references(heap):
    index = len(heap) // 2
    print(index)
    first_ref = heap[index]
    second_ref = heap[index]

    heap.remove(first_ref)

    assert first_ref is second_ref
    assert not first_ref.is_valid() and not second_ref.is_valid()


if __name__ == '__main__':
    test_references(FibonacciHeap(SORTED_INPUT))
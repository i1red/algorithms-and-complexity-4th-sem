import pytest
import random
from lab8x9_common.heapqueue import PriorityQueue

BOUND = 1000
DIF_PRIORITY_INPUT = [(random.randint(-BOUND, BOUND), random.randint(-BOUND, BOUND)) for _ in range(BOUND)]
SAME_PRIORITY_INPUT = [(0, random.randint(-BOUND, BOUND)) for _ in range(BOUND)]


@pytest.fixture(params=[DIF_PRIORITY_INPUT, SAME_PRIORITY_INPUT])
def input(request):
    return request.param


def test_queue(input):
    queue = PriorityQueue()

    for priority, value in input:
        queue.push(priority, value)

    items = []
    while len(queue) > 0:
        items.append(queue.pop())

    #timsort is stable, that's why sorting list of pairs by first element will keep pairs in a proper order
    assert items == sorted(input, key=lambda x: x[0])

import random
from binomialheap import BinomialHeap


if __name__ == '__main__':
    bheap = BinomialHeap()

    for i in range(30):
        bheap.insert(random.randint(-30, 30), i)

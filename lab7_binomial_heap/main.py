import random
from binomialheap import BinomialHeap


if __name__ == '__main__':
    bheap = BinomialHeap()

    for i in range(30):
        bheap.insert(i, 0)

    print(len(bheap))
    keys = []
    values = []
    while len(bheap) > 0:
        key, value = bheap.extract_min()
        keys.append(key)
        values.append(value)

    print(keys, len(keys))
    print(values, len(values))

from fibonacciheap import FibonacciHeap


if __name__ == '__main__':
    fib_heap = FibonacciHeap()

    for i in range(30):
        fib_heap.insert(i, 0)

    keys = []
    values = []
    while len(fib_heap) > 0:
        key, value = fib_heap.extract_min()
        keys.append(key)
        values.append(value)
        print(len(fib_heap))

    print(keys, len(keys))
    print(values, len(values))
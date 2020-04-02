import math
from typing import *


TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


class FibHeapNode:
    def __init__(self, key: Any, value: Any, degree: int = 0, mark: bool = False,
                 child: Optional['FibHeapNode'] = None, left: Optional['FibHeapNode'] = None,
                 right: Optional['FibHeapNode'] = None, parent: Optional['FibHeapNode'] = None) -> None:
        self.key = key
        self.value = value
        self.degree = degree
        self.mark = mark
        self.child = child
        self.left = left if left is not None else self
        self.right = right if right is not None else self
        self.parent = parent

    def add_child(self, child: 'FibHeapNode') -> None:
        if self.child is None:
            self.child = child
        else:
            self.child.left.right = child
            child.left = self.child.left
            self.child.left = child
            child.right = self.child

        self.degree += 1

class FibonacciHeap(Generic[TKey, TValue]):
    def __init__(self, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        self._min = None
        self._length = 0

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __len__(self) -> int:
        return self._length

    def insert(self, key: TKey, value: TValue) -> None:
        self._length += 1
        self._insert_node(FibHeapNode(key, value))

    def extract_min(self) -> Tuple[TKey, TValue]:
        if self._min is None:
            raise IndexError('Empty heap')

        self._length -= 1

        minimum = self._min
        tmp = minimum.child

        if tmp is not None:
            while True:
                tmp.parent = None
                self._insert_node(tmp)

                tmp = tmp.right
                if tmp is minimum.child:
                    break

        self._delete_root(minimum)
        if self._min is minimum.right:
            self._consolidate()

        return (minimum.key, minimum.value)

    def _consolidate(self) -> None:
        nodes_by_degree = [None for _ in range(len(self) + 1)]

        tmp = self._min
        while True:
            tmp_degree = tmp.degree

            while (other := nodes_by_degree[tmp_degree]) is not None:
                if tmp.key > other.key:
                    tmp, other = other, tmp

                self._link(other, tmp)
                nodes_by_degree[tmp_degree] = None
                tmp_degree += 1

            nodes_by_degree[tmp_degree] = tmp

            tmp = tmp.right
            if tmp is self._min:
                break

        self._min = None

        for node in nodes_by_degree:
            if node is not None:
                # noinspection PyTypeChecker
                self._insert_node(node)

    def _insert_node(self, node: FibHeapNode) -> None:
        if self._min is None:
            self._min = node
        elif self._min.key > node.key:
            node.right, node.left = self._min.right, self._min

            self._min.right.left = node
            self._min.right = node
            self._min = node
        else:
            node.right, node.left = self._min, self._min.left

            self._min.left.right = node
            self._min.left = node

    def _max_degree(self) -> int:
        return int(math.log(len(self), (1 + math.sqrt(5)) / 2))

    def _link(self, new_child: FibHeapNode, new_parent: FibHeapNode) -> None:
        self._delete_root(new_child)
        new_parent.add_child(new_child)
        new_child.mark = False

    def _delete_root(self, old_root: FibHeapNode) -> None:
        if old_root is self._min and old_root.right is self._min:
            self._min = None
        else:
            old_root.left.right = old_root.right
            old_root.right.left = old_root.left

            if old_root is self._min:
                self._min = self._min.right


import weakref
from typing import *


class ImmutableRef:
    def __init__(self, node: Union['FibHeapNode', 'BinHeapNode'], heap: Union['FibonacciHeap', 'BinomialHeap']) -> None:
        self._node = node
        self._heap = heap

    @property
    def key(self) -> Any:
        return self._node.key

    @property
    def value(self) -> Any:
        return self._node.value

    def is_valid(self) -> bool:
        return self._node is not None and self._heap is not None


class HeapMixin:
    def __init__(self):
        self._refs = weakref.WeakValueDictionary()

    def __len__(self) -> int:
        raise NotImplementedError

    def _get_node(self, index: int) -> Union['FibHeapNode', 'BinHeapNode']:
        raise NotImplementedError

    def __getitem__(self, index: int) -> ImmutableRef:
        if index < 0:
            index += len(self)

        if index < 0 or index >= len(self):
            raise IndexError('Index is out of range')

        node = self._get_node(index)
        node_id = id(node)
        in_refs = node_id in self._refs

        result = self._refs[node_id] if in_refs else ImmutableRef(node, self)
        if not in_refs:
            self._refs[node_id] = result

        return result

    def _make_node_link_invalid(self, node: Union['FibHeapNode', 'BinHeapNode']) -> None:
        node_id = id(node)
        if node_id in self._refs:
            ref = self._refs[node_id]
            ref._node = ref._heap = None
            del self._refs[node_id]


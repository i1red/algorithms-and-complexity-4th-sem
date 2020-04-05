from binheapnode import *
from utils.heap import *


TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


class BinomialHeap(Generic[TKey, TValue], HeapMixin):
    def __init__(self, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        super().__init__()
        self._head = None
        self._length = 0

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __len__(self) -> int:
        return self._length

    def insert(self, key: TKey, value: TValue) -> None:
        self._length += 1
        self._head = merge(BinHeapNode(key, value), self._head)

    def extract_min(self) -> Tuple[TKey, TValue]:
        if self._head is None:
            raise IndexError('Empty heap')

        self._length -= 1

        min_prev, minimum = min_and_prev(self._head)
        self._make_node_link_invalid(minimum)
        self._remove_node(min_prev, minimum)

        return (minimum.key, minimum.value)

    def get_minimum(self) -> Tuple[TKey, TValue]:
        if self._head is None:
            raise IndexError('Empty heap')

        _, minimum = min_and_prev(self._head)
        return (minimum.key, minimum.value)

    def decrease_key(self, ref: ImmutableRef, new_key: TKey) -> bool:
        if ref._heap is not self:
            raise ValueError('Element does NOT belong to heap')

        node = ref._node
        if new_key > node.key:
            return False

        node.key = new_key
        self._emerge_node(node, lambda x: x.parent.key > x.key)
        return True

    def remove(self, ref: ImmutableRef) -> None:
        if ref._heap is not self:
            raise ValueError('Element does NOT belong to heap')

        self._length -= 1

        node = self._emerge_node(ref._node, lambda x: True)
        prev = self._prev_node(node)
        self._remove_node(prev, node)

        ref._node = ref._heap = None
        del self._refs[id(node)]

    def _emerge_node(self, node: BinHeapNode, condition: Callable[[BinHeapNode], bool]) -> BinHeapNode:
        while (parent := node.parent) is not None and condition(node):
            node_id, parent_id = id(node), id(parent)
            node_in_refs, parent_in_refs = node_id in self._refs, parent_id in self._refs

            if node_in_refs and parent_in_refs:
                self._refs[node_id]._node, self._refs[parent_id]._node = parent, node
                self._refs[node_id], self._refs[parent_id] = self._refs[parent_id], self._refs[node_id]
            elif node_in_refs:
                ref = self._refs[node_id]
                ref._node = parent
                self._refs[parent_id] = ref
                del self._refs[node_id]
            elif parent_in_refs:
                ref = self._refs[parent_id]
                ref._node = node
                self._refs[node_id] = ref
                del self._refs[parent_id]

            parent.key, node.key = node.key, parent.key
            parent.value, node.value = node.value, parent.value
            node = parent

        return node

    def _remove_node(self, prev: Optional[BinHeapNode], node: BinHeapNode) -> None:
        if prev is None:
            self._head = node.rt_sibling
        else:
            prev.rt_sibling = node.rt_sibling

        self._head = merge(self._head, child_heap(node))

    def _prev_node(self, node: BinHeapNode) -> Optional[BinHeapNode]:
        prev, tmp = None, self._head

        while tmp is not node:
            prev = tmp
            tmp = tmp.rt_sibling

        return prev

    def _get_node(self, index: int) -> BinHeapNode:
        tmp_index, tmp = 2 ** self._head.degree - 1, self._head

        while tmp_index != index:
            if tmp_index > index:
                tmp_index -= 2 ** tmp.degree - 2 ** tmp.lt_child.degree
                tmp = tmp.lt_child
            else:
                tmp_index += 2 ** tmp.rt_sibling.degree
                tmp = tmp.rt_sibling

        return tmp

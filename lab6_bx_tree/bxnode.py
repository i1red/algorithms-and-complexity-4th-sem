import bisect
from typing import *


TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


def binary_search(arr: List, item: Any) -> int:
    position = bisect.bisect_left(arr, item)
    return position if position < len(arr) and item == arr[position] else -1


class BxNodeBase(Generic[TKey]):
    def __init__(self, keys: Collection[TKey]) -> None:
        self.keys = list(keys)
        self.parent = None

    def __contains__(self, key: TKey) -> bool:
        return binary_search(self.keys, key) != -1

    def left_sibling_pos(self) -> int:
        position = self.position()
        return -1 if position <= 0 else position - 1

    def right_sibling_pos(self) -> int:
        position = self.position()
        return -1 if position == -1 or position == len(self.parent.children) - 1 \
            else position + 1

    def position(self) -> int:
        raise NotImplementedError

    @property
    def key_count(self) -> int:
        return len(self.keys)


class LeafNode(BxNodeBase, Generic[TKey, TValue]):
    def __init__(self, keys: Collection[TKey], values: Collection[TValue],
                 next_node: Optional['LeafNode'] = None) -> None:
        super().__init__(keys)
        self.values = list(values)
        self.next = next_node

    def insert(self, key: TKey, value: TValue) -> None:
        position = bisect.bisect_right(self.keys, key)

        if position == 0 or self.keys[position - 1] != key:
            self.keys.insert(position, key)
            self.values.insert(position, value)
        else:
            self.values[position - 1] = value

    def remove(self, key: TKey) -> bool:
        position = binary_search(self.keys, key)

        if position == -1:
            return False

        self.keys.pop(position)
        self.values.pop(position)

        return True

    def extend(self, keys: Iterable[TKey], values: Iterable[TValue]) -> None:
        self.keys.extend(keys)
        self.values.extend(values)

    def pop_min(self) -> Tuple[TKey, TValue]:
        return (self.keys.pop(0), self.values.pop(0))

    def pop_max(self) -> Tuple[TKey, TValue]:
        return (self.keys.pop(), self.values.pop())

    def position(self) -> int:
        if self.parent is None:
            return -1

        if len(self.keys) > 0:
            return bisect.bisect_right(self.parent.keys, self.keys[0])

        if self.next is None or self.next.parent is not self.parent:
            return self.parent.key_count

        next_pos = bisect.bisect_right(self.parent.keys, self.next.keys[0])
        return next_pos - 1

    def get(self, key: TKey) -> TValue:
        position = binary_search(self.keys, key)

        if position == -1:
            raise KeyError

        return self.values[position]


class InnerNode(BxNodeBase[TKey]):
    def __init__(self, keys: Collection[TKey], children: Collection[Union['InnerNode', LeafNode]]) -> None:
        super().__init__(keys)
        self.children = list(children)

        for child in children:
            child.parent = self

    def insert(self, key: TKey, node: Union['InnerNode', LeafNode]) -> None:
        node.parent = self

        position = bisect.bisect_right(self.keys, key)
        self.keys.insert(position, key)
        self.children.insert(position if node.keys[-1] < key else position + 1, node)

    def child(self, key: TKey) -> Union['InnerNode', LeafNode]:
        position = bisect.bisect_right(self.keys, key)
        return self.children[position]

    def extend(self, keys: Iterable[TKey], children: Iterable[Union['InnerNode', LeafNode]]) -> None:
        self.keys.extend(keys)
        self.children.extend(children)

        for child in children:
            child.parent = self

    def pop_min(self) -> Tuple[TKey, Union['InnerNode', LeafNode]]:
        return (self.keys.pop(0), self.children.pop(0))

    def pop_max(self) -> Tuple[TKey, Union['InnerNode', LeafNode]]:
        return (self.keys.pop(), self.children.pop())

    def position(self) -> int:
        if self.parent is None:
            return -1

        return bisect.bisect_right(self.parent.keys, self.smallest_child().keys[0])

    def smallest_child(self) -> Union['InnerNode', LeafNode]:
        return self.children[0]

    def min_greater_key(self, key: TKey) -> TKey:
        tmp = self.child(key)

        while not isinstance(tmp, LeafNode):
            tmp = tmp.smallest_child()

        return tmp.keys[0]


def height(node: Union[InnerNode, LeafNode]) -> int:
    if isinstance(node, LeafNode):
        return 1

    return max(height(child) for child in node.children) + 1


def split(node: Union[InnerNode, LeafNode]) -> Tuple[TKey, Union[InnerNode, LeafNode]]:
    return _split_leaf(node) if isinstance(node, LeafNode) else _split_inner(node)


def _split_leaf(node: LeafNode) -> Tuple[TKey, LeafNode]:
    mid = ((node.key_count + 1) // 2) - 1
    left_keys, right_keys, mid_key = node.keys[:mid], node.keys[mid:], node.keys[mid]
    left_values, right_values = node.values[:mid], node.values[mid:]

    node.keys, node.values = left_keys, left_values
    right_node = LeafNode(right_keys, right_values, node.next)
    node.next = right_node

    return (mid_key, right_node)


def _split_inner(node: InnerNode) -> Tuple[TKey, InnerNode]:
    mid = ((node.key_count + 1) // 2) - 1
    left_keys, right_keys, mid_key = node.keys[:mid], node.keys[mid + 1:], node.keys[mid]
    left_children, right_children = node.children[:mid + 1], node.children[mid + 1:]

    node.keys, node.children = left_keys, left_children
    right_node = InnerNode(right_keys, right_children)

    return (mid_key, right_node)


def merge(node: Union[InnerNode, LeafNode]) -> None:
    if isinstance(node, LeafNode):
        _merge_leaf(node)
    else:
        _merge_inner(node)


def _merge_node(func: Callable[[Union[LeafNode, InnerNode], Union[LeafNode, InnerNode], InnerNode, int], None]) \
        -> Callable[[Union[LeafNode, InnerNode]], None]:
    def wrap(node: Union[LeafNode, InnerNode]):
        position, parent = node.position(), node.parent

        if position != 0:
            left_sibling, right_sibling = parent.children[position - 1], node
        else:
            left_sibling, right_sibling = node, parent.children[position + 1]
            position += 1

        return func(left_sibling, right_sibling, parent, position)

    return wrap


@_merge_node
def _merge_leaf(left_sibling: LeafNode, right_sibling: LeafNode, parent: InnerNode, position: int) -> None:
    left_sibling.extend(right_sibling.keys, right_sibling.values)
    left_sibling.next = right_sibling.next

    parent.keys.pop(position - 1)
    parent.children.pop(position)


@_merge_node
def _merge_inner(left_sibling: InnerNode, right_sibling: InnerNode, parent: InnerNode, position: int) -> None:
    left_sibling.keys.append(parent.keys.pop(position - 1))
    left_sibling.extend(right_sibling.keys, right_sibling.children)

    parent.children.pop(position)

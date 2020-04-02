from __future__ import annotations
from typing import *
from collections import deque
import reprlib


NodeType = TypeVar('NodeType', bound='sNode')


class Node:
    def __init__(self, key: Any, values: Optional[Iterable[Any]] = None,
                 lt: Optional[NodeType] = None, rt: Optional[NodeType] = None) -> None:
        self.key = key
        self.values = [] if values is None else list(values)
        self.lt = lt
        self.rt = rt

    def __copy__(self) -> NodeType:
        return self.__class__(self.key, self.values, self.lt, self.rt)

    @property
    def value_count(self) -> int:
        return len(self.values)

    @property
    def lt(self) -> Optional[NodeType]:
        return self._lt

    @lt.setter
    def lt(self, son: Optional[NodeType]) -> None:
        self._set_lt(son)

    @property
    def rt(self) -> Optional[NodeType]:
        return self._rt

    @rt.setter
    def rt(self, son: Optional[NodeType]) -> None:
        self._set_rt(son)

    def _set_rt(self, son: Optional[NodeType]) -> None:
        self._rt = son

    def _set_lt(self, son: Optional[NodeType]) -> None:
        self._lt = son


class ParentedNode(Node):
    def __init__(self, key: Any, values: Iterable[Any],
                 lt: Optional[NodeType] = None, rt: Optional[NodeType] = None) -> None:
        super().__init__(key, values, lt, rt)
        self._dad = None

    def _set_lt(self, son: Optional[NodeType]) -> None:
        if son is not None:
            son._dad = self
        self._lt = son

    def _set_rt(self, son: Optional[NodeType]) -> None:
        if son is not None:
            son._dad = self
        self._rt = son

    @property
    def dad(self) -> Optional[NodeType]:
        return self._dad

    def clear_dad(self) -> None:
        self._dad = None


def assign_son(parent: Node, son: Optional[Node], assign_lt: bool) -> None:
    if assign_lt:
        parent.lt = son
    else:
        parent.rt = son


def max_node(node: NodeType) -> NodeType:
    tmp = node

    while tmp.rt is not None:
        tmp = tmp.rt

    return tmp


def min_node(node: NodeType) -> NodeType:
    tmp = node

    while tmp.lt is not None:
        tmp = tmp.lt

    return tmp


TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


class ImmutableBinTreeMixin(Generic[TKey, TValue]):
    def __init__(self):
        """
        Only initializes _root field.
        You should implement proper initialization in subclass
        """
        self._root = None

    def __iter__(self) -> Iterator[Tuple[TKey, TValue]]:
        for node in self._iter_nodes():
            for value in node.values:
                yield (node.key, value)

    def __contains__(self, key: TKey) -> bool:
        return False if self._search_node(key) is None else True

    def get(self, key: TKey) -> List[TValue]:
        node = self._search_node(key)

        if node is not None:
            return list(node.values)
        else:
            raise KeyError

    def _search_node(self, key: TKey) -> Optional[NodeType]:
        tmp = self._root

        while tmp is not None and key != tmp.key:
            tmp = tmp.lt if key < tmp.key else tmp.rt

        return tmp

    def _iter_nodes(self) -> Iterator[NodeType]:
        node_stack = deque()
        tmp = self._root
        while tmp is not None or len(node_stack) > 0:
            if tmp is not None:
                node_stack.append(tmp)
                tmp = tmp.lt
            else:
                cur = node_stack.pop()
                yield cur
                tmp = cur.rt


class BinTreeMixin(ImmutableBinTreeMixin[TKey, TValue]):
    def __init__(self, init_list: Iterable[Tuple[TKey, TValue]] = None):
        super().__init__()

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({reprlib.repr(list(iter(self)))})'

    def insert(self, key: TKey, value: Optional[TValue] = None) -> None:
        raise NotImplementedError


class BalancingTreeMixin(BinTreeMixin[TKey, TValue]):
    def _rotate_right(self, node: NodeType) -> NodeType:
        node_dad, new_root, new_left = node.dad, node.lt, node.lt.rt
        self._reset_dad(node, new_root, node_dad)
        node.lt, new_root.rt = new_left, node

        return new_root

    def _rotate_left(self, node: NodeType) -> NodeType:
        node_dad, new_root, new_right = node.dad, node.rt, node.rt.lt
        self._reset_dad(node, new_root, node_dad)
        node.rt, new_root.lt = new_right, node

        return new_root

    def _reset_dad(self, prev_son: NodeType, new_son: NodeType, dad: Optional[NodeType]) -> None:
        if dad is None:
            self._root = new_son
            new_son.clear_dad()
        else:
            assign_son(dad, new_son, prev_son is dad.lt)

from __future__ import annotations
from typing import *
import copy
from utils.treemixin import ParentedNode, TKey, TValue, BalancingTreeMixin, max_node, min_node, assign_son


def tree_size(node: Optional[ParentedNode]) -> int:
    if node is None:
        return 0

    return node.value_count + tree_size(node.lt) + tree_size(node.rt)


class SplayTree(BalancingTreeMixin[TKey, TValue]):
    def __init__(self, init_list: Iterable[Tuple[TKey, TValue]] = None) -> None:
        self._length = 0
        super().__init__(init_list)

    def __len__(self) -> int:
        return self._length

    def __contains__(self, key: TKey) -> bool:
        node = self._search_node(key)

        if node is not None:
            self._splay(node)
            return True
        else:
            return False

    def insert(self, key: TKey, value: Optional[TValue] = None) -> None:
        self._length += 1

        if self._root is None:
            self._root = ParentedNode(key, [value])
        else:
            tmp, dad, is_left = self._root, None, False

            while tmp is not None:
                if key == tmp.key:
                    tmp.values.append(value)
                    self._splay(tmp)
                    return

                dad = tmp
                tmp, is_left = (tmp.lt, True) if key < tmp.key else (tmp.rt, False)

            node = ParentedNode(key, [value])
            assign_son(dad, node, is_left)

            self._splay(node)

    def get(self, key: TKey) -> List[TValue]:
        node = self._search_node(key)

        if node is not None:
            self._splay(node)
            return list(node.values)
        else:
            raise KeyError

    def split(self, key: TKey) -> SplayTree[TKey, TValue]:
        tmp, min_greater_node = self._root, None

        while tmp is not None:
            if key <= tmp.key:
                if min_greater_node is None or min_greater_node.key > tmp.key:
                    min_greater_node = tmp
                tmp = tmp.lt
            else:
                tmp = tmp.rt

        if min_greater_node is None:
            return SplayTree()

        self._splay(min_greater_node)

        res = SplayTree()
        new_root = self._root.lt
        if new_root is not None:
            new_root.clear_dad()

        self._root.lt = None
        res._root = self._root
        self._root = new_root

        new_length = tree_size(new_root)
        res._length = self._length - new_length
        self._length = new_length

        return res

    def extend(self, other: SplayTree[TKey, TValue]) -> None:
        """
        Uses copy.deepcopy function which is recursive.
        Change recursion limit(look sys.setrecursionlimit) if tree contains a lot of data
        """
        other_root = copy.deepcopy(other._root)

        if self._root is None:
            self._root = other_root
        elif other_root is not None:
            self_max_node = max_node(self._root)
            other_min_node = min_node(other_root)

            if self_max_node.key >= other_min_node.key:
                raise ValueError('Keys of given other tree should be greater than keys in self tree')

            self._splay(self_max_node)
            self._root.rt = other_root

        self._length += other._length

    def remove(self, key: TKey, pos: Optional[int] = None) -> None:
        tmp = self._search_node(key)

        if tmp is not None:
            dad = tmp.dad

            if pos is not None and tmp.value_count > 1:
                if 0 <= pos < tmp.value_count:
                    self._length -= 1
                    tmp.values.pop(pos)
            elif pos is None or pos == 0:
                node_to_remove = tmp
                self._length -= tmp.value_count

                if tmp.lt is not None and tmp.rt is not None:
                    node_to_remove = min_node(tmp.rt)
                    tmp.key, tmp.values = node_to_remove.key, node_to_remove.values

                self._remove_node(node_to_remove)

            if dad is not None:
                self._splay(dad)

    def _remove_node(self, node: ParentedNode) -> None:
        if node is self._root:
            self._root = self._root.rt if self._root.lt is None else self._root.lt
            if self._root is not None:
                self._root.clear_dad()
        else:
            parent, is_lt = node.dad, node is node.dad.lt
            node_son = node.rt if node.lt is None else node.lt
            assign_son(parent, node_son, is_lt)

    def _splay(self, node: ParentedNode) -> None:
        while node is not self._root:
            dad = node.dad
            is_left = node is dad.lt

            if dad is self._root:
                self._zig(node, is_left)
            else:
                grand = dad.dad
                is_dad_left = dad is grand.lt

                if is_left == is_dad_left:
                    self._zig_zig(node, is_left)
                else:
                    self._zig_zag(node, is_dad_left)

    def _zig(self, node: ParentedNode, is_left: bool) -> None:
        if is_left:
            self._rotate_right(node.dad)
        else:
            self._rotate_left(node.dad)

    def _zig_zig(self, node: ParentedNode, is_left_left: bool) -> None:
        if is_left_left:
            self._rotate_right(node.dad.dad)
            self._rotate_right(node.dad)
        else:
            self._rotate_left(node.dad.dad)
            self._rotate_left(node.dad)

    def _zig_zag(self, node: ParentedNode, is_left_right: bool) -> None:
        if is_left_right:
            self._rotate_left(node.dad)
            self._rotate_right(node.dad)
        else:
            self._rotate_right(node.dad)
            self._rotate_left(node.dad)


class SplayTreeEfficiencyTest(SplayTree[TKey, TValue]):
    def __init__(self, init_list: Iterable[Tuple[TKey, TValue]] = None) -> None:
        self.total_op = 0
        super().__init__(init_list)

    def __contains__(self, key: TKey) -> bool:
        counter = 1
        node = self._root

        while node is not None and key != node.key:
            node = node.lt if key < node.key else node.rt
            counter += 1

        self.total_op += counter

        if node is not None:
            self._splay(node)
            return True
        else:
            return False

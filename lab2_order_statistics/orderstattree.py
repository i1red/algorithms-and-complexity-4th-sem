from __future__ import annotations
from enum import Enum
from typing import *
import reprlib
import collections


TKey, TValue = TypeVar('TKey'), TypeVar('TValue')


class Color(Enum):
    RED = 1
    BLACK = 2


class SizedNode:
    def __init__(self, key: Any, values: Iterable[Any], tree_size: int = 1, color: Color = Color.RED,
                 lt: Optional[SizedNode] = None, rt: Optional[SizedNode] = None):
        self.tree_size = tree_size
        self.color = color
        self.key = key
        self.values = list(values)
        self.lt = lt
        self.rt = rt
        self._dad = None

    @property
    def lt(self) -> Optional[SizedNode]:
        return self._lt

    @lt.setter
    def lt(self, son: Optional[SizedNode]) -> None:
        if son is not None:
            son._dad = self
        self._lt = son

    @property
    def rt(self) -> Optional[SizedNode]:
        return self._rt

    @rt.setter
    def rt(self, son: Optional[SizedNode]) -> None:
        if son is not None:
            son._dad = self
        self._rt = son

    @property
    def dad(self) -> Optional[SizedNode]:
        return self._dad

    @property
    def value_count(self):
        return len(self.values)

    def clear_dad(self) -> None:
        self._dad = None


def black_height(node: Optional[SizedNode]) -> int:
    if node is None:
        return 0

    return max(black_height(node.lt), black_height(node.rt)) + (0 if node.color == Color.RED else 1)


def node_color(node: Optional[SizedNode]) -> Color:
    return Color.BLACK if node is None else node.color


def has_black_sons(node: SizedNode) -> bool:
    return node_color(node.lt) == Color.BLACK and node_color(node.rt) == Color.BLACK


def tree_size_of(node: Optional[SizedNode]) -> int:
    return 0 if node is None else node.tree_size


def change_size(node: SizedNode, value: int = -1, stop_node: Optional[SizedNode] = None) -> None:
    tmp = node
    while tmp is not stop_node:
        tmp.tree_size += value
        tmp = tmp.dad


def fix_tree_size(node: SizedNode, new_root: SizedNode) -> None:
    new_root.tree_size = node.tree_size
    node.tree_size = tree_size_of(node.lt) + tree_size_of(node.rt) + node.value_count


def assign_son(parent: SizedNode, son: Optional[SizedNode], assign_lt: bool) -> None:
    if assign_lt:
        parent.lt = son
    else:
        parent.rt = son


class OrderStatTree(Generic[TKey, TValue]):
    def __init__(self, init_list: Optional[Iterable[TKey]] = None):
        self._root = None

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __iter__(self) -> Iterator[TKey]:
        for node in self._node_iter():
            for value in node.values:
                yield (node.key, value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({reprlib.repr(list(iter(self)))})'

    def __contains__(self, key: TKey) -> bool:
        tmp = self._root

        while tmp is not None and key != tmp.key:
            tmp = tmp.lt if key < tmp.key else tmp.rt

        return True if tmp is not None else False

    def __len__(self) -> int:
        return tree_size_of(self._root)

    def _node_iter(self) -> Iterator[SizedNode]:
        node_stack = collections.deque()
        tmp = self._root
        while tmp is not None or len(node_stack) > 0:
            if tmp is not None:
                node_stack.append(tmp)
                tmp = tmp.lt
            else:
                cur = node_stack.pop()
                yield cur
                tmp = cur.rt

    def select(self, index: int) -> TKey:
        if index < 0 or index >= len(self):
            raise IndexError

        tmp, cur_index = self._root, tree_size_of(self._root.lt)

        while not (cur_index <= index <= cur_index + tmp.value_count - 1):
            if cur_index < index:
                cur_index += tmp.value_count + tree_size_of(tmp.rt.lt)
                tmp = tmp.rt
            else:
                tmp = tmp.lt
                cur_index -= tmp.value_count + tree_size_of(tmp.rt)

        return tmp.key

    def rank(self, key: TKey) -> int:
        if self._root is None:
            return -1

        tmp, cur_rank = self._root, tree_size_of(self._root.lt)

        while key != tmp.key:
            if key < tmp.key:
                if tmp.lt is not None:
                    tmp = tmp.lt
                    cur_rank -= tmp.value_count + tree_size_of(tmp.rt)
                    continue
            if key > tmp.key:
                if tmp.rt is not None:
                    cur_rank += tmp.value_count + tree_size_of(tmp.rt.lt)
                    tmp = tmp.rt
                    continue

            return -1

        return cur_rank

    def get(self, key: TKey):
        tmp = self._root

        while tmp is not None and key != tmp.key:
            tmp = tmp.lt if key < tmp.key else tmp.rt

        if tmp is None:
            raise KeyError
        else:
            return tmp.values

    def insert(self, key: TKey, value: Optional[TValue] = None) -> None:
        if self._root is None:
            self._root = node = SizedNode(key, [value])
        else:
            tmp, parent, insert_lt = self._root, None, False

            while tmp is not None:
                tmp.tree_size += 1

                if key == tmp.key:
                    tmp.values.append(value)
                    return

                parent = tmp
                tmp, insert_lt = (tmp.lt, True) if key < tmp.key else (tmp.rt, False)

            node = SizedNode(key, [value])
            assign_son(parent, node, insert_lt)

        if node is not None:
            self._fix_insert(node)

    def _fix_insert(self, node: SizedNode) -> None:
        tmp = node
        while node_color(tmp.dad) == Color.RED:
            parent, grand = tmp.dad, tmp.dad.dad
            uncle, is_dad_lt = (grand.lt, False) if parent is grand.rt else (grand.rt, True)

            if node_color(uncle) == Color.RED:
                parent.color = uncle.color = Color.BLACK
                grand.color, tmp = Color.RED, grand
            else:
                is_cur_lt = tmp is parent.lt
                if is_dad_lt:
                    if not is_cur_lt:
                        self._rotate_left(parent)
                        tmp, parent = parent, tmp
                    self._rotate_right(grand)
                else:
                    if is_cur_lt:
                        self._rotate_right(parent)
                        tmp, parent = parent, tmp
                    self._rotate_left(grand)

                parent.color, grand.color = Color.BLACK, Color.RED

        if tmp is self._root:
            tmp.color = Color.BLACK

    def remove(self, key: TKey, pos: Optional[int] = None) -> None:
        tmp = self._root

        while tmp is not None and key != tmp.key:
            tmp = tmp.lt if key < tmp.key else tmp.rt

        if tmp is not None:
            if pos is not None and tmp.value_count > 1:
                if 0 <= pos < tmp.value_count:
                    change_size(tmp)
                    tmp.values.pop(pos)
            elif pos is None or pos == 0:
                change_size(tmp, -tmp.value_count)

                if tmp.lt is not None and tmp.rt is not None:
                    tmp2 = tmp.rt

                    while tmp2.lt is not None:
                        tmp2 = tmp2.lt

                    change_size(tmp2, -tmp2.value_count, tmp)
                    tmp.key, tmp.values = tmp2.key, tmp2.values
                    tmp = tmp2

                self._remove_node(tmp)

    def _remove_node(self, node: SizedNode) -> None:
        if node is self._root:
            self._root = self._root.rt if self._root.lt is None else self._root.lt
            if self._root is not None:
                self._root.clear_dad()
                self._root.color = Color.BLACK
        else:
            parent, is_lt = node.dad, node is node.dad.lt

            if node.lt is None and node.rt is None:
                assign_son(parent, None, is_lt)

                if node.color == Color.BLACK:
                    self._fix_remove(parent, parent.rt if is_lt else parent.lt)
            else:
                node_son = node.rt if node.lt is None else node.lt
                node_son.color = Color.BLACK

                assign_son(parent, node_son, is_lt)

    def _fix_remove(self, parent: SizedNode, uncle: SizedNode) -> None:
        parent_colors = {Color.RED: self._fix_rm_red_parent,
                         Color.BLACK: self._fix_rm_blk_parent}

        parent_colors[parent.color](parent, uncle, uncle is parent.lt)

    def _fix_rm_red_parent(self, parent: SizedNode, uncle: SizedNode, is_uncle_lt: bool):
        if has_black_sons(uncle):
            parent.color, uncle.color = Color.BLACK, Color.RED
        else:
            if is_uncle_lt:
                if node_color(uncle.lt) == Color.RED:
                    uncle.color, uncle.lt.color = Color.RED, Color.BLACK
                else:
                    self._rotate_left(uncle)

                self._rotate_right(parent)
            else:
                if node_color(uncle.rt) == Color.RED:
                    uncle.color, uncle.rt.color = Color.RED, Color.BLACK
                else:
                    self._rotate_right(uncle)

                self._rotate_left(parent)

            parent.color = Color.BLACK

    def _fix_rm_blk_parent(self, parent: SizedNode, uncle: SizedNode, is_uncle_lt: bool) -> None:
        uncle_color = {Color.RED: self._fix_rm_blk_parent_red_uncle,
                       Color.BLACK: self._fix_rm_blk_parent_blk_uncle}

        uncle_color[uncle.color](parent, uncle, is_uncle_lt)

    def _fix_rm_blk_parent_red_uncle(self, parent: SizedNode, uncle: SizedNode, is_uncle_lt: bool) -> None:
        if is_uncle_lt:
            if has_black_sons(uncle.rt):
                uncle.color, uncle.rt.color = Color.BLACK, Color.RED
                self._rotate_right(parent)
            else:
                if node_color(uncle.rt.lt) == Color.BLACK:
                    self._rotate_left(uncle.rt)
                    uncle.rt.color = Color.BLACK
                else:
                    uncle.rt.lt.color = Color.BLACK

                self._rotate_left(uncle)
                self._rotate_right(parent)
        else:
            if has_black_sons(uncle.lt):
                uncle.color, uncle.lt.color = Color.BLACK, Color.RED
                self._rotate_left(parent)
            else:
                if node_color(uncle.lt.rt) == Color.BLACK:
                    self._rotate_right(uncle.lt)
                    uncle.lt.color = Color.BLACK
                else:
                    uncle.lt.rt.color = Color.BLACK

                self._rotate_right(uncle)
                self._rotate_left(parent)

    def _fix_rm_blk_parent_blk_uncle(self, parent: SizedNode, uncle: SizedNode, is_uncle_lt: bool) -> None:
        if has_black_sons(uncle):
            uncle.color = Color.RED

            if (grand_parent := parent.dad) is not None:
                self._fix_remove(grand_parent, grand_parent.rt if parent is grand_parent.lt else grand_parent.lt)
        else:
            if is_uncle_lt:
                if node_color(uncle.lt) == Color.BLACK:
                    uncle.rt.color = Color.BLACK
                    self._rotate_left(uncle)
                else:
                    uncle.lt.color = Color.BLACK

                self._rotate_right(parent)
            else:
                if node_color(uncle.rt) == Color.BLACK:
                    uncle.lt.color = Color.BLACK
                    self._rotate_right(uncle)
                else:
                    uncle.rt.color = Color.BLACK

                self._rotate_left(parent)

    def _rotate_right(self, node: SizedNode) -> None:
        node_dad, new_root, new_left = node.dad, node.lt, node.lt.rt
        self._reset_dad(node, new_root, node_dad)
        node.lt, new_root.rt = new_left, node

        fix_tree_size(node, new_root)

    def _rotate_left(self, node: SizedNode) -> None:
        node_dad, new_root, new_right = node.dad, node.rt, node.rt.lt
        self._reset_dad(node, new_root, node_dad)
        node.rt, new_root.lt = new_right, node

        fix_tree_size(node, new_root)

    def _reset_dad(self, prev_son: SizedNode, new_son: SizedNode, dad: Optional[SizedNode]) -> None:
        if dad is None:
            self._root = new_son
            new_son.clear_dad()
        else:
            assign_son(dad, new_son, prev_son is dad.lt)


class OSTreeTestVersion(OrderStatTree):
    def root_color(self):
        return node_color(self._root)

    def iter_nodes(self):
        return self._node_iter()

class OSTreeEfficiencyTest(OrderStatTree):
    def __init__(self, init_list: Optional[Iterable[TKey]] = None):
        self.total_op = 0
        super().__init__(init_list)

    def __contains__(self, key: TKey) -> bool:
        counter = 1
        tmp = self._root

        while tmp is not None and key != tmp.key:
            tmp = tmp.lt if key < tmp.key else tmp.rt
            counter += 1

        self.total_op += counter

        return True if tmp is not None else False
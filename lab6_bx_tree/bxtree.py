import reprlib
from bxnode import *


class BxTree(Generic[TKey, TValue]):
    def __init__(self, b_order: int, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        if b_order < 3:
            raise ValueError('b_order should be >= 3')

        self._root = None
        self._b_order = b_order
        self._length = 0

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[Tuple[TKey, TValue]]:
        if self._root is not None:
            tmp = self._root

            while not isinstance(tmp, LeafNode):
                tmp = tmp.smallest_child()

            while tmp is not None:
                for key, value in zip(tmp.keys, tmp.values):
                    yield (key, value)

                tmp = tmp.next

    def __contains__(self, key: TKey) -> bool:
        node = self._search_leaf_node(key)

        if node is None:
            return False

        try:
            node.get(key)
            return True
        except KeyError:
            return False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._b_order}, {reprlib.repr(list(iter(self)))})'

    @property
    def b_order(self) -> int:
        return self._b_order

    def get(self, key: TKey) -> TValue:
        node = self._search_leaf_node(key)
        return node.get(key)

    def insert(self, key: TKey, value: Optional[TValue] = None) -> None:
        tmp = self._search_leaf_node(key)

        if tmp is None:
            self._root = LeafNode([key], [value])
            self._length = 1
        else:
            if key not in tmp:
                self._length += 1

            tmp.insert(key, value)

            while self._is_overfilled(tmp):
                up_key, right_node = split(tmp)

                if tmp.parent is None:
                    self._root = InnerNode([up_key], [tmp, right_node])
                    break

                tmp = tmp.parent
                tmp.insert(up_key, right_node)

    def remove(self, key: TKey) -> None:
        tmp = self._search_leaf_node(key)

        if tmp is not None and key in tmp:
            tmp.remove(key)
            self._length -= 1

            while self._is_unfilled(tmp) and not self._borrow_key(tmp):
                if tmp is self._root:
                    self._shrink_height()
                    break

                merge(tmp)
                tmp = tmp.parent

    def _shrink_height(self) -> None:
        if isinstance(self._root, LeafNode):
            self._root = None
        else:
            self._root = self._root.children[0]

    def _borrow_key(self, node: Union[InnerNode, LeafNode]) -> bool:
        return True if self._borrow_key_left(node) else self._borrow_key_right(node)

    def _borrow_key_left(self, node: Union[InnerNode, LeafNode]) -> bool:
        lt_sibl_pos, parent = node.left_sibling_pos(), node.parent

        if lt_sibl_pos == -1 or not self._can_borrow_key(left_sibling := parent.children[lt_sibl_pos]):
            return False

        if isinstance(node, LeafNode):
            # noinspection PyUnboundLocalVariable
            key, val = left_sibling.pop_max()
            parent.keys[lt_sibl_pos] = key
        else:
            key = parent.keys[lt_sibl_pos]
            # noinspection PyUnboundLocalVariable
            parent.keys[lt_sibl_pos], val = left_sibling.pop_max()

        node.insert(key, val)

        return True

    def _borrow_key_right(self, node: Union[InnerNode, LeafNode]) -> bool:
        rt_sibl_pos, parent = node.right_sibling_pos(), node.parent

        if rt_sibl_pos == -1 or not self._can_borrow_key(right_sibling := parent.children[rt_sibl_pos]):
            return False

        if isinstance(node, LeafNode):
            # noinspection PyUnboundLocalVariable
            key, val = right_sibling.pop_min()
            parent.keys[rt_sibl_pos - 1] = right_sibling.keys[0]
        else:
            key = parent.keys[rt_sibl_pos - 1]
            # noinspection PyUnboundLocalVariable
            parent.keys[rt_sibl_pos - 1], val = right_sibling.pop_min()

        node.insert(key, val)

        return True

    def _search_leaf_node(self, key: TKey) -> Optional[LeafNode]:
        if self._root is None:
            return None

        tmp = self._root
        while not isinstance(tmp, LeafNode):
            tmp = tmp.child(key)

        return tmp

    def _is_overfilled(self, node: Union[InnerNode, LeafNode]) -> bool:
        return node.key_count == self.b_order

    def _is_unfilled(self, node: Union[InnerNode, LeafNode]) -> bool:
        if node is self._root:
            return node.key_count == 0

        return node.key_count < ((self.b_order + 1) // 2) - 1

    def _can_borrow_key(self, node: Union[InnerNode, LeafNode]) -> bool:
        if node is self._root:
            return node.key_count > 1

        return node.key_count > ((self.b_order + 1) // 2) - 1

import collections
import copy
from typing import *
from utils.treemixin import BinTreeMixin, Node, TKey, TValue, assign_son


class PersistentBST(BinTreeMixin[TKey, TValue]):
    def __init__(self, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None, max_ver: int = 10) -> None:
        self._versions = collections.deque()
        self._max_ver = max_ver
        self._length = 0
        super().__init__(init_list)

    def __len__(self) -> int:
        return self._length

    def insert(self, key: TKey, value: Optional[TValue] = None) -> None:
        if len(self._versions) == self._max_ver:
            self._versions.popleft()

        self._versions.append((self._root, self._length))
        self._length += 1

        if self._root is None:
            self._root = Node(key, [value])
        else:
            route = copy.copy(self._root)
            tmp = route

            while key != tmp.key:
                if key < tmp.key:
                    tmp.lt = Node(key) if tmp.lt is None else copy.copy(tmp.lt)
                    tmp = tmp.lt
                else:
                    tmp.rt = Node(key) if tmp.rt is None else copy.copy(tmp.rt)
                    tmp = tmp.rt

            tmp.values.append(value)
            self._root = route

    def remove(self, key: TKey, pos: Optional[int] = None) -> None:
        if self._root is not None:
            route = copy.copy(self._root)
            tmp, dad = route, None

            while tmp is not None and key != tmp.key:
                dad = tmp

                if key < tmp.key:
                    tmp.lt = copy.copy(tmp.lt)
                    tmp = tmp.lt
                else:
                    tmp.rt = copy.copy(tmp.rt)
                    tmp = tmp.rt

            if tmp is not None and (pos is None or 0 <= pos < tmp.value_count):
                if len(self._versions) == self._max_ver:
                    self._versions.popleft()

                self._versions.append((self._root, self._length))

                if pos is None or tmp.value_count == 1:
                    self._length -= tmp.value_count

                    if tmp.lt is not None and tmp.rt is not None:
                        tmp.rt = copy.copy(tmp.rt)
                        sub_tmp, sub_dad = tmp.rt, tmp

                        while sub_tmp.lt is not None:
                            sub_dad = sub_tmp
                            sub_tmp.lt = copy.copy(sub_tmp.lt)
                            sub_tmp = sub_tmp.lt

                        tmp.key, tmp.values = sub_tmp.key, sub_tmp.values
                        assign_son(sub_dad, sub_tmp.rt, sub_dad is not tmp)
                    elif dad is None:
                        route = route.lt if route.rt is None else route.rt
                    else:
                        is_lt = tmp is dad.lt

                        if tmp.lt is None:
                            assign_son(dad, tmp.rt, is_lt)
                        elif tmp.rt is None:
                            assign_son(dad, tmp.lt, is_lt)
                else:
                    tmp.values.pop(pos)
                    self._length -= 1

                self._root = route

    def undo(self, amount: int = 1) -> None:
        if amount > self._max_ver:
            raise ValueError

        for _ in range(amount):
            self._root, self._length = self._versions.pop()


class PersistentBSTTestVersion(PersistentBST[TKey, TValue]):
    def total_object_count(self):
        node_ids = set()

        def traversal(node: Optional[Node]):
            if node is not None:
                node_ids.add(id(node))
                traversal(node.lt)
                traversal(node.rt)

        for tmp_root, _ in self._versions:
            traversal(tmp_root)

        return len(node_ids)

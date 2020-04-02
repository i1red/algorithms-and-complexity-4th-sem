import random
from bxtree import *


B_MIN = 4
B_MAX = 100


class BxTreeTestVersion(BxTree[TKey, TValue]):
    def __init__(self, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        super().__init__(random.randint(B_MIN, B_MAX), init_list)

    def iter_nodes(self, inner_only=False) -> Iterator[Union[LeafNode, InnerNode]]:
        def traversal(node: Union[LeafNode, InnerNode]) -> Iterator[Union[LeafNode, InnerNode]]:
            if not inner_only or isinstance(node, InnerNode):
                yield node

            if isinstance(node, InnerNode):
                for child in node.children:
                    yield from traversal(child)

        if self._root is not None:
            yield from traversal(self._root)

    def is_valid(self, node: Union[InnerNode, LeafNode]) -> bool:
        return not (self._is_overfilled(node) or self._is_unfilled(node))

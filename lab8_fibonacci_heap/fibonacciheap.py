from utils.heap import *


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

    def remove_child(self, child: 'FibHeapNode') -> None:
        if child is child.right:
            self.child = None
        else:
            child.left.right = child.right
            child.right.left = child.left

            if child is self.child:
                self.child = child.left

        child.parent = None
        self.degree -= 1

    def link_child(self, new_child: 'FibHeapNode') -> None:
        self.add_child(new_child)
        new_child.mark = False


def next_node(node: FibHeapNode) -> FibHeapNode:
    next_ = node.right
    node.left = node.right = node
    return next_


def iter_circular_list(cur_node: FibHeapNode, extract_nodes: bool = True) -> Iterator[FibHeapNode]:
    end_node = cur_node
    while True:
        nx_node = next_node(cur_node) if extract_nodes else cur_node.right
        yield cur_node

        if nx_node is end_node:
            break
        cur_node = nx_node


class FibonacciHeap(Generic[TKey, TValue], HeapMixin):
    def __init__(self, init_list: Optional[Iterable[Tuple[TKey, TValue]]] = None) -> None:
        super().__init__()
        self._min = None
        self._length = 0

        if init_list is not None:
            for key, value in init_list:
                self.insert(key, value)

    def __len__(self) -> int:
        return self._length

    def insert(self, key: TKey, value: TValue) -> None:
        self._length += 1
        self._insert_root(FibHeapNode(key, value))

    def extract_min(self) -> Tuple[TKey, TValue]:
        if self._min is None:
            raise IndexError('Empty heap')

        self._length -= 1

        minimum = self._min
        self._make_node_link_invalid(minimum)
        self._remove_root(minimum)

        return (minimum.key, minimum.value)

    def get_minimum(self) -> Tuple[TKey, TValue]:
        if self._min is None:
            raise IndexError('Empty heap')

        return (self._min.key, self._min.value)

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

        node = ref._node
        self._emerge_node(node, lambda x: True)
        self._remove_root(node)

        ref._node = ref._heap = None
        del self._refs[id(node)]

    def _get_node(self, index: int) -> FibHeapNode:
        for cur_index, node in enumerate(self._iter_nodes()):
            if cur_index == index:
                return node

    def _iter_nodes(self) -> Iterator[FibHeapNode]:
        def recursive_traversal(cur_node: FibHeapNode) -> FibHeapNode:
            for node in iter_circular_list(cur_node, extract_nodes=False):
                if node.child is not None:
                    yield from recursive_traversal(node.child)
                yield node

        if self._min is not None:
            yield from recursive_traversal(self._min)

    def _consolidate(self) -> None:
        nodes_by_degree = {}

        for node in iter_circular_list(self._min):
            node_dgr = node.degree

            while node_dgr in nodes_by_degree:
                other = nodes_by_degree[node_dgr]
                if node.key > other.key:
                    node, other = other, node

                node.link_child(other)
                del nodes_by_degree[node_dgr]
                node_dgr += 1

            nodes_by_degree[node_dgr] = node

        self._min = None

        for _, node in nodes_by_degree.items():
            self._insert_root(node)

    def _insert_root(self, node: FibHeapNode) -> None:
        if self._min is None:
            self._min = node
        else:
            node.right, node.left = self._min, self._min.left

            self._min.left.right = node
            self._min.left = node

            if self._min.key > node.key:
                self._min = node

    def _extract_tree(self, tree_root: FibHeapNode) -> None:
        """Extracts root with its children from heap"""
        if tree_root is self._min and tree_root.right is self._min:
            self._min = None
        else:
            tree_root.left.right = tree_root.right
            tree_root.right.left = tree_root.left

            if tree_root is self._min:
                self._min = self._min.right

    def _remove_root(self, old_root: FibHeapNode) -> None:
        """Removes root and restores its children"""
        child = old_root.child
        self._extract_tree(old_root)

        if child is not None:
            for node in iter_circular_list(child):
                node.parent = None
                self._insert_root(node)

        if self._min is not None:
            self._consolidate()

    def _emerge_node(self, node: FibHeapNode, condition: Callable[[FibHeapNode], bool]) -> None:
        if (parent := node.parent) is not None and condition(node):
            self._cut(node, parent)
            self._cascading_cut(parent)

        if node.key < self._min.key:
            self._min = node

    def _cut(self, node: FibHeapNode, parent: FibHeapNode) -> None:
        parent.remove_child(node)
        self._insert_root(node)
        node.mark = False

    def _cascading_cut(self, node: FibHeapNode) -> None:
        if (parent := node.parent) is not None:
            if not node.mark:
                node.mark = True
            else:
                self._cut(node, parent)
                self._cascading_cut(parent)

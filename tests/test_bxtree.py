import pytest
import random
import collections
from lab6_bx_tree.bxtreetestversion import BxTreeTestVersion, height


BOUND = 15000
INPUT_VALUES = {random.randint(-BOUND, BOUND) for _ in range(BOUND)}


@pytest.fixture
def bxtree() -> BxTreeTestVersion:
    return BxTreeTestVersion([(key, None) for key in INPUT_VALUES])


def test_height(bxtree: BxTreeTestVersion) -> None:
    for inner_node in bxtree.iter_nodes(inner_only=True):
        heights = {height(child) for child in inner_node.children}
        assert len(heights) == 1


def test_repeat_keys(bxtree: BxTreeTestVersion) -> None:
    counter = collections.Counter()

    for node in bxtree.iter_nodes():
        counter.update(node.keys)

    for key in INPUT_VALUES:
        assert counter[key] <= 2


def test_node_properties(bxtree: BxTreeTestVersion) -> None:
    for node in bxtree.iter_nodes():
        assert bxtree.is_valid(node)

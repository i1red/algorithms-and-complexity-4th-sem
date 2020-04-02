import pytest
from settings import *
from lab2_order_statistics.orderstattree import OSTreeTestVersion, Color, black_height, node_color


@pytest.fixture
def os_tree() -> OSTreeTestVersion:
    rand_keys = [random.randint(-BOUND, BOUND) in range(BOUND)]

    res_tree = OSTreeTestVersion()
    for _ in range(3):
        for key in rand_keys:
            res_tree.insert(key, None)
        for _ in range(BOUND // 2):
            res_tree.remove(random.choice(rand_keys))
    for key in rand_keys:
        res_tree.remove(key)

    for pair in START_INPUT + SORTED_INPUT:
        res_tree.insert(*pair)

    return res_tree


def test_black_height(os_tree: OSTreeTestVersion) -> None:
    for node in os_tree.iter_nodes():
        assert black_height(node.lt) == black_height(node.rt)


def test_root_is_black(os_tree: OSTreeTestVersion) -> None:
    assert os_tree.root_color() == Color.BLACK


def test_colors(os_tree: OSTreeTestVersion) -> None:
    for node in os_tree.iter_nodes():
        if node_color(node) == Color.RED:
            assert node_color(node.lt) == Color.BLACK
            assert node_color(node.rt) == Color.BLACK
    

def test_select(os_tree: OSTreeTestVersion) -> None:
    for i, (key, _) in enumerate(SORTED_VALUES):
        assert os_tree.select(i) == key


def test_rank(os_tree: OSTreeTestVersion) -> None:
    for key in ALL_KEYS:
        assert SORTED_VALUES[os_tree.rank(key)][0] == key

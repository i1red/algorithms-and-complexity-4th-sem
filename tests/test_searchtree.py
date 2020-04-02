import pytest
from typing import Union
from bintree.settings import *
from lab2_order_statistics.orderstattree import OSTreeTestVersion
from lab3_splay_tree.splaytree import SplayTree
from lab5_persistent_bst.persistentbst import PersistentBST
from lab6_bx_tree.bxtreetestversion import BxTreeTestVersion


@pytest.fixture(params=[OSTreeTestVersion, SplayTree, PersistentBST, BxTreeTestVersion])
def tree(request) -> Union[OSTreeTestVersion, SplayTree]:
    return request.param(START_INPUT + SORTED_INPUT)


def test_contains(tree) -> None:
    for key in ALL_KEYS:
        assert key in tree


def test_not_contains(tree) -> None:
    for _ in range(BOUND):
        key = random.randint(-BOUND, 10 * BOUND)
        while key in ALL_KEYS:
            key = random.randint(-BOUND, 10 * BOUND)
        assert key not in tree


def test_len(tree) -> None:
    assert len(tree) == len(SORTED_VALUES)


def test_sorted(tree) -> None:
    tree_keys = [key for key, _ in tree]
    sorted_keys = [key for key, _ in SORTED_VALUES]

    assert tree_keys == sorted_keys


def test_remove(tree) -> None:
    for key in ALL_KEYS:
        tree.remove(key)
        assert key not in tree

    assert len(tree) == 0

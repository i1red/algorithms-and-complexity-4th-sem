import pytest
from settings import *
from lab3_splay_tree.splaytree import SplayTree
import sys


sys.setrecursionlimit(10 ** 4)


@pytest.mark.parametrize('tree_to_extend, tree_extender', [(SplayTree(START_INPUT), SplayTree(SORTED_INPUT))])
def test_extend(tree_to_extend: SplayTree, tree_extender: SplayTree) -> None:
    tree_to_extend.extend(tree_extender)

    for key, _ in SORTED_INPUT:
        tree_extender.remove(key)

    tree_keys = {key for key, _ in tree_to_extend}
    assert tree_keys == ALL_KEYS
    assert len(tree_to_extend) == len(SORTED_VALUES)


@pytest.mark.parametrize('tree_to_extend, tree_extender', [(SplayTree(START_INPUT), SplayTree(SORTED_VALUES))])
def test_extend_raises(tree_to_extend: SplayTree, tree_extender: SplayTree) -> None:
    with pytest.raises(ValueError):
        tree_to_extend.extend(tree_extender)


@pytest.mark.parametrize('splay_tree', [SplayTree(START_INPUT + SORTED_INPUT)])
def test_split(splay_tree: SplayTree) -> None:
    index = random.randrange(len(SORTED_VALUES))
    while index > 0 and SORTED_VALUES[index][0] == SORTED_VALUES[index - 1][0]:
        index -= 1

    split_tree = splay_tree.split(SORTED_VALUES[index][0])

    splay_keys = [key for key, _ in splay_tree]
    split_keys = [key for key, _ in split_tree]

    p1, p2 = SORTED_VALUES[:index], SORTED_VALUES[index:]
    p1_keys, p2_keys = [key for key, _ in p1], [key for key, _ in p2]

    assert splay_keys == p1_keys
    assert split_keys == p2_keys

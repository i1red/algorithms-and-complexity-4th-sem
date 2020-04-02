import random
import itertools
from typing import *
from lab2_order_statistics.orderstattree import OSTreeEfficiencyTest
from lab3_splay_tree.splaytree import SplayTreeEfficiencyTest
from optimalbst import OptimalBSTEfficiencyTest


LENGTH = 200
KEYS_IN_ARR = [key for key in range(0, LENGTH * 2, 2)]
KEYS_NOT_IN_ARR = [key for key in range(-1, LENGTH * 2, 2)]
INPUT_ARR = [(key, [random.random()]) for key in KEYS_IN_ARR]
FREQUENCIES = [random.randint(1, 100) for _ in range(LENGTH)]
DUMMY_FREQ = [random.randint(0, 50) for _ in range(LENGTH + 1)]
QUERIES_IN = list(itertools.chain(*[list(key for _ in range(FREQUENCIES[i])) for i, key in enumerate(KEYS_IN_ARR)]))
QUERIES_NOT_IN = list(itertools.chain(*[list(key for _ in range(DUMMY_FREQ[i])) for i, key in enumerate(KEYS_NOT_IN_ARR)]))


def tree_efficiency_test(tree: Union[OptimalBSTEfficiencyTest, OSTreeEfficiencyTest, SplayTreeEfficiencyTest],
                    keys_in: List, keys_not_in: List) -> Tuple[float, bool, bool]:
    flag_keys_in = all(key in tree for key in keys_in)
    flag_keys_not_in = all(key not in tree for key in keys_not_in)
    return (tree.total_op / (len(keys_in) + len(keys_not_in)), flag_keys_in, flag_keys_not_in)


if __name__ == '__main__':
    randomized_input = list(INPUT_ARR)
    random.shuffle(randomized_input)
    random.shuffle(QUERIES_IN)

    optimal_bst = OptimalBSTEfficiencyTest(INPUT_ARR, FREQUENCIES, DUMMY_FREQ)
    os_tree = OSTreeEfficiencyTest(randomized_input)
    splay_tree = SplayTreeEfficiencyTest(randomized_input)

    print(f'EXPECTED OPTIMAL AVG: {optimal_bst.avg}')

    for tree in (optimal_bst, os_tree, splay_tree):
        print(f'RUN TEST FOR {tree.__class__.__name__}:')

        avg_op, keys_in, keys_not_in = tree_efficiency_test(tree, QUERIES_IN, QUERIES_NOT_IN)

        print(f'AVG: {avg_op}')
        print(f'KEYS IN: {"OK" if keys_in else "FAILED"}')
        print(f'KEYS NOT IN: {"OK" if keys_not_in else "FAILED"}')

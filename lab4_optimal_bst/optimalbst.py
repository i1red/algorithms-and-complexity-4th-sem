import math
from typing import *
from utils.treemixin import ImmutableBinTreeMixin, TKey, TValue, Node
import numpy as np

ERROR = 0.1 ** 5


def calc_bst_matrix(frequencies: List[float], dummy_frequencies: List[float]) -> Tuple[np.ndarray, float]:
    freq_num = len(dummy_frequencies)

    frequencies = np.array([0] + frequencies)
    dummy_frequencies = np.array(dummy_frequencies)

    cost_table = np.full(shape=(freq_num + 1, freq_num), fill_value=np.inf)
    weight_table = np.zeros(shape=(freq_num + 1, freq_num))
    roots_table = np.zeros(shape=(freq_num, freq_num), dtype=int)

    for first_i in range(1, freq_num + 1):
        cost_table[first_i][first_i - 1] = weight_table[first_i][first_i - 1] = dummy_frequencies[first_i - 1]

    for level in range(1, freq_num):
        for first_i in range(1, freq_num - level + 1):
            last_i = first_i + level - 1
            weight_table[first_i][last_i] = weight_table[first_i][last_i - 1] + \
                                            frequencies[last_i] + dummy_frequencies[last_i]

            for root_i in range(first_i, last_i + 1):
                tmp = cost_table[first_i][root_i - 1] + cost_table[root_i + 1][last_i] + weight_table[first_i][last_i]

                if tmp < cost_table[first_i][last_i]:
                    cost_table[first_i][last_i] = tmp
                    roots_table[first_i][last_i] = root_i

    avg = cost_table[1][freq_num - 1]
    return (roots_table, avg)


class OptimalBST(ImmutableBinTreeMixin[TKey, TValue]):
    def __init__(self, init_list: List[Tuple[TKey, List[TValue]]],
                 frequencies: List[Union[int, float]], dummy_frequencies: List[Union[int, float]]) -> None:
        super().__init__()

        total = sum(frequencies + dummy_frequencies)

        tree_matrix = calc_bst_matrix([freq / total for freq in frequencies],
                                      [freq / total for freq in dummy_frequencies])

        self._root = OptimalBST._set_up_tree(tree_matrix[0], 1, len(init_list), init_list)
        self._avg = tree_matrix[1]

    @property
    def avg(self) -> float:
        return self._avg

    @staticmethod
    def _set_up_tree(matrix, fi, li, init_list) -> Optional[Node]:
        if fi > li:
            return None

        index = matrix[fi][li]
        key, values = init_list[index - 1]
        return Node(key, values, lt=OptimalBST._set_up_tree(matrix, fi, index - 1, init_list),
                    rt=OptimalBST._set_up_tree(matrix, index + 1, li, init_list))


class OptimalBSTEfficiencyTest(OptimalBST):
    def __init__(self, init_list: List[Tuple[TKey, List[TValue]]],
                 frequencies: List[Union[int, float]], dummy_frequencies: List[Union[int, float]]) -> None:
        self.total_op = 0
        super().__init__(init_list, frequencies, dummy_frequencies)

    def __contains__(self, key: TKey) -> bool:
        counter = 1
        tmp = self._root

        while tmp is not None and key != tmp.key:
            tmp = tmp.lt if key < tmp.key else tmp.rt
            counter += 1

        self.total_op += counter

        return True if tmp is not None else False

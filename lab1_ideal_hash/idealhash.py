import random
import reprlib
from utils import find_greater_prime, to_vector
from typing import *


def random_hash_func(prime: int, max_hash: int) -> Callable[[Any], int]:
    a, b = random.randrange(1, prime), random.randrange(0, prime)

    def hash_func(obj: Any) -> int:
        vector = to_vector(obj)
        return ((sum((a ** i) * val for i, val in enumerate(vector, start=1)) + b) % prime) % max_hash

    return hash_func


class BasicHashMap:
    def __init__(self, elements: List[Tuple[Any, Any]], prime: int):
        self._set_up(elements, prime, len(elements) ** 2)

    def _set_up(self, elements: List[Tuple[Any, Any]], prime: int, max_hash: int) -> None:
        self._arr = [None for _ in range(max_hash)]
        self._hash_func = random_hash_func(prime, max_hash)

        for key, value in elements:
            hash_val = self._hash_func(key)
            if self._arr[hash_val] is None:
                # noinspection PyTypeChecker
                self._arr[hash_val] = (key, value)
            else:
                self._set_up(elements, prime, max_hash)
                return

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        for item in self._arr:
            if item is not None:
                yield item

    def __contains__(self, key: Any) -> bool:
        hash_val = self._hash_func(key)
        return self._arr[hash_val] is not None and self._arr[hash_val][0] == key

    def __getitem__(self, key: Any) -> Any:
        hash_val = self._hash_func(key)
        if self._arr[hash_val] is not None and self._arr[hash_val][0] == key:
            return self._arr[hash_val][1]
        else:
            raise KeyError


class HashMap:
    def __init__(self, elements: Collection[Tuple[Any, Any]], max_hash: int = 0):
        if max_hash <= 0:
            max_hash = len(elements)

        prime = find_greater_prime(len(elements) ** 2)

        self._hash_func = random_hash_func(prime, max_hash)
        self._length = self._fill_map(elements, prime, max_hash)

    def _fill_map(self, elements: Collection[Tuple[Any, Any]], prime: int, max_hash: int) -> int:
        self._arr = [None for _ in range(max_hash)]
        tmp_arr = [None for _ in range(max_hash)]

        for key, value in elements:
            hash_val = self._hash_func(key)
            if tmp_arr[hash_val] is None:
                # noinspection PyTypeChecker
                tmp_arr[hash_val] = [(key, value)]
            else:
                insert = True
                # noinspection PyTypeChecker
                for i in range(len(tmp_arr[hash_val])):
                    tmp_key = tmp_arr[hash_val][i][0]
                    if key == tmp_key:
                        tmp_arr[hash_val][i] = (key, value)
                        insert = False

                if insert:
                    tmp_arr[hash_val].append((key, value))

        len_count = 0

        for i, keys in enumerate(tmp_arr):
            if keys is not None:
                # noinspection PyTypeChecker
                self._arr[i] = BasicHashMap(keys, prime)
                # noinspection PyTypeChecker
                len_count += len(keys)

        return len_count

    def __len__(self) -> int:
        return self._length

    def __iter__(self) -> Iterator[Tuple[Any, Any]]:
        for item in self._arr:
            if item is not None:
                # noinspection PyTypeChecker
                for el in item:
                    yield el

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({reprlib.repr(list(iter(self)))}, {len(self._arr)})'

    def __contains__(self, key: Any) -> bool:
        hash_val = self._hash_func(key)
        return self._arr[hash_val] is not None and key in self._arr[hash_val]

    def __getitem__(self, key: Any) -> Any:
        hash_val = self._hash_func(key)
        if self._arr[hash_val] is not None:
            return self._arr[hash_val][key]
        else:
            raise KeyError

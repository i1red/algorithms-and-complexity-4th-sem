import random
from typing import Type
from lab1_ideal_hash.idealhash import HashMap
from utils.staff import Division, Worker
from utils import gen_items, rand_str


def gen_div(item_type: Type[Division]) -> Division:
    return item_type(rand_str(random.randint(3, 12)))


def gen_worker(item_type: Type[Worker]) -> Worker:
    return item_type(rand_str(random.randint(3, 12)))


def test_contains():
    divisions = gen_items(500, Division, gen_div)
    mapping = HashMap([(div, None) for div in divisions], max_hash=random.randint(10, 1000))

    for div in divisions:
        assert div in mapping


def test_getitem():
    divisions = [(div, gen_items(random.randint(0, 20), Worker, gen_worker))
                 for div in gen_items(500, Division, gen_div)]
    mapping = HashMap([div for div in divisions], max_hash=random.randint(10, 1000))

    for div, workers in divisions:
        assert mapping[div] == workers


def test_length_unique():
    length = 500
    divisions = gen_items(length, Division, gen_div)
    mapping = HashMap([(div, None) for div in divisions], max_hash=random.randint(10, 1000))

    assert len(mapping) == length


def test_length_non_unique():
    length = 250
    divisions = gen_items(length, Division, gen_div)
    divisions.extend(divisions)
    mapping = HashMap([(div, None) for div in divisions], max_hash=random.randint(10, 1000))

    assert len(mapping) == length


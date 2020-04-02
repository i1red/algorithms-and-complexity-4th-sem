import math
import pickle
import random
import string
import struct
from functools import singledispatch
from typing import Any, Iterator, List, Callable, Iterable
from collections import abc
from array import array
from staff import Division, Worker
from students import Stream, Student
from db.students_db import fetch_by_query


def fetch_stream_students(stream: Stream) -> Iterator[Student]:
    query = f"""SELECT stud.surname, stud.name, stud.patronymic, stud.total 
                FROM students stud LEFT JOIN streams s ON stud.stream_id=s.id 
                WHERE s.name LIKE :spec AND s.course=:course"""

    for stud in fetch_by_query(query, {'spec': f'{stream.specialty}%', 'course': stream.course}):
        yield Student(*stud)


def serialize_objects(filename: str, sequence: Iterable[Any]) -> None:
    with open(filename, 'wb') as f:
        for obj in sequence:
            byte_repr = pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)
            repr_len = struct.pack('@I', len(byte_repr))
            f.write(repr_len)
            f.write(byte_repr)


def deserialize_objects(filename: str) -> Iterator[Any]:
    with open(filename, 'rb') as f:
        while len(length := f.read(4)) == 4:
            repr_len = struct.unpack('@I', length)[0]
            byte_repr = f.read(repr_len)
            yield pickle.loads(byte_repr)


def gen_items(item_count: int, item_type: Any, init_func: Callable[[Any], Any]) -> List[Any]:
    items = []

    for _ in range(item_count):
        while (item := init_func(item_type)) in items:
            pass
        items.append(item)

    return items


@singledispatch
def to_vector(obj: Any) -> array:
    return array('I', [sym for sym in pickle.dumps(obj, pickle.HIGHEST_PROTOCOL)])


@to_vector.register
def _(s: str) -> array:
    return array('I', [ord(sym) for sym in s])


@to_vector.register
def _(integer: int) -> array:
    return array('I', [integer])


@to_vector.register
def _(iterable: abc.Iterable) -> array:
    res = array('I', [])

    for obj in iterable:
        res.extend(to_vector(obj))

    return res if len(res) > 0 else array('I', [0])


def rand_str(length: int) -> str:
    return random.choice(string.ascii_uppercase) + \
           ''.join(random.choice(string.ascii_lowercase) for _ in range(length - 1))


def possible_primes(start: int = 2, stop: int = math.inf) -> Iterator[int]:
    # noinspection PyTypeChecker
    for i in range(max(start, 2), min(stop, 4)):
        yield i

    if (tmp := start - start % 6 + 6) - 1 >= start:
        yield tmp - 1

    yield tmp + 1

    while (tmp := tmp + 6) < stop:
        yield tmp - 1
        yield tmp + 1

    if tmp - 1 < stop:
        yield tmp - 1


def is_prime(num: int) -> bool:
    if num < 2:
        return False

    top_bound = int(math.sqrt(num)) + 1
    for i in possible_primes(stop=top_bound):
        if num % i == 0:
            return False

    return True


def find_greater_prime(num: int) -> int:
    for i in possible_primes(start=num + 1):
        if is_prime(i):
            return i

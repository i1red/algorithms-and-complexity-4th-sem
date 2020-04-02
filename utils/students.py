from __future__ import annotations
from typing import *

class Stream:
    def __init__(self, specialty: str, course: int):
        self.specialty = specialty
        self.course = course

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.specialty}", {self.course})'

    def __eq__(self, other: Stream) -> bool:
        return (self.course, self.specialty) == (other.course, other.specialty)

    def __lt__(self, other: Stream) -> bool:
        return (self.course, self.specialty) < (other.course, other.specialty)


class Student:
    def __init__(self, surname: str, name: str, patronymic: str, avg: float):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.avg = avg

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self.surname}", "{self.name}", "{self.patronymic}", {self.avg})'

    def __eq__(self, other: Student) -> bool:
        return (self.avg, self.surname, self.name, self.patronymic) == \
               (other.avg, other.surname, other.name, other.patronymic)

    def __lt__(self, other: Student) -> bool:
        return (self.avg, self.surname, self.name, self.patronymic) < \
               (other.avg, other.surname, other.name, other.patronymic)

    def __le__(self, other: Student) -> bool:
        return (self.avg, self.surname, self.name, self.patronymic) <= \
               (other.avg, other.surname, other.name, other.patronymic)



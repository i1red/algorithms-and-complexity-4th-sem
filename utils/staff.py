from __future__ import annotations


class Division:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name})'

    def __eq__(self, other: Division) -> bool:
        return self.name == other.name

    @property
    def name(self) -> str:
        return self._name


class Worker:
    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def __eq__(self, other: Worker) -> bool:
        return self.name == other.name

    @property
    def name(self) -> str:
        return self._name

import sqlite3
from typing import Iterator, List


class FightersDB:
    def __init__(self, db_name: str):
        self._connection = sqlite3.connect(db_name)
        self._cursor = self._connection.cursor()
        self._set_up_db()

    def insert_division(self, name: str) -> None:
        with self._connection:
            self._cursor.execute("INSERT INTO divisions (name) VALUES (:name)", {'name': name})

    def insert_fighter(self, name: str, division_id: int) -> None:
        with self._connection:
            self._cursor.execute("INSERT INTO fighters (name, division_id) VALUES (:name, :division_id)",
                                 {'name': name, 'division_id': division_id})

    def fetch_division_fighters(self, division_name: str) -> Iterator[str]:
        self._cursor.execute("""SELECT f.name FROM divisions div LEFT JOIN fighters f ON div.id=f.division_id 
                                WHERE div.name=:division_name""", {'division_name': division_name})
        for tup in self._cursor.fetchall():
            yield tup[0]

    def send_selection_query(self, query: str) -> List:
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def _set_up_db(self) -> None:
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS divisions (
                                                           id INTEGER PRIMARY KEY,
                                                           name TEXT
                                                           );""")
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS fighters (
                                                           id INTEGER PRIMARY KEY,
                                                           name TEXT,
                                                           division_id INTEGER,
                                                           FOREIGN KEY(division_id) REFERENCES divisions(id)
                                                           );""")


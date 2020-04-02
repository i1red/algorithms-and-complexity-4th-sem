import sqlite3
import os
from typing import List, Tuple, Mapping


db_path = os.path.dirname(os.path.abspath(__file__))
connection = sqlite3.connect(f'{db_path}/students.sqlite3')
cursor = connection.cursor()


def fetch_by_query(query: str, params: Mapping) -> List[Tuple]:
    cursor.execute(query, params)
    return cursor.fetchall()


def change_with_query(query: str, params: Mapping) -> None:
    with connection:
        cursor.execute(query, params)

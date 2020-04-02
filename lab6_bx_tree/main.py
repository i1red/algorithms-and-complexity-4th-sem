import random
from bxtree import BxTree
from utils.db.students_db import fetch_by_query


def demo():
    b_min, b_max = 4, 100
    el_count = 1000
    init_keys = [random.randint(-el_count // 3, el_count // 3) for _ in range(el_count)]

    bxtree = BxTree(random.randint(b_min, b_max))

    print(f'EL_COUNT = {el_count}, UNIQUE - {len(set(init_keys))}')

    for _ in range(2):
        for key in init_keys:
            bxtree.insert(key)

        print(f'INSERTED KEYS, TREE LENGTH = {len(bxtree)}, LIST(ITER) LENGTH = {len(list(iter(bxtree)))}')
        print(bxtree)
        print()

        for key in init_keys:
            bxtree.remove(key)

        print(f'REMOVED KEYS, TREE LENGTH = {len(bxtree)}, LIST(ITER) LENGTH = {len(list(iter(bxtree)))}')
        print(bxtree)
        print()


if __name__ == '__main__':
    students = BxTree(10)

    for student in fetch_by_query("SELECT * from students", {}):
        name, surname, patronymic, avg, stream_id = student
        students.insert(' '.join([surname, name, patronymic]), (avg, stream_id))

    streams = BxTree(3)

    for stream in fetch_by_query("SELECT * from streams", {}):
        stream_id, specialty, course = stream
        streams.insert(stream_id, (specialty, course))

    input_str = ''
    print("ENTER 'q' TO EXIT")
    print()

    while True:
        input_str = input('enter student fullname: ')

        if input_str == 'q':
            break

        try:
            avg, stream_id = students.get(input_str)
            specialty, course = streams.get(stream_id)
            print(f'specialty: {specialty}')
            print(f'course: {course}')
            print(f'average: {avg}')
        except KeyError:
            print('student with such fullname was not found')

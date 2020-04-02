from orderstattree import OrderStatTree
from utils.students import Stream, Student
from utils import STREAMS, fetch_stream_students
from typing import Iterator


if __name__ == '__main__':
    specialty_tree = OrderStatTree()

    for stream in STREAMS:
        for student in fetch_stream_students(stream):
            specialty_tree.insert(stream, student)

    stream = specialty_tree.get(Stream('Інженерія програмного забезпечення', 2))
    student_tree = OrderStatTree([(student, None) for student in stream])
    print(student_tree)

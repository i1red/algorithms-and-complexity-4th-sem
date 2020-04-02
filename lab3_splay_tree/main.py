from splaytree import SplayTree
from utils.students import Stream, Student
from utils import fetch_stream_students


if __name__ == '__main__':
    stream_key = Stream('Інженерія програмного забезпечення', 2)

    students = fetch_stream_students(stream_key)
    student_tree = SplayTree([(student, None) for student in students])

    excellent_key = Student('Я', 'Я', 'Я', 90)

    exc_students = student_tree.split(excellent_key)

    for student, _ in exc_students:
        print(student)

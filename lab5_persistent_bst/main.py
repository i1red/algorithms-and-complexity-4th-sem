import itertools
import random
from typing import List
from students import Stream, Student
from utils import fetch_stream_students, SOFTWARE_ENGINEERING, COMPUTER_SCIENCE, APPLIED_MATHEMATICS
from persistentbst import PersistentBSTTestVersion


LENGTH = 10
MAX_VER = 100
MIN_AVG = 80


def fetch_student_with_avg(stream: Stream, min_avg: float) -> List[Student]:
    return list(student for student in fetch_stream_students(stream) if student.avg >= min_avg)


if __name__ == '__main__':
    software_en2 = Stream(SOFTWARE_ENGINEERING, 2)
    computer_sci2 = Stream(COMPUTER_SCIENCE, 2)
    applied_math2 = Stream(APPLIED_MATHEMATICS, 2)

    students_se2 = fetch_student_with_avg(software_en2, MIN_AVG)
    students_cs2 = fetch_student_with_avg(computer_sci2, MIN_AVG)
    students_am2 = fetch_student_with_avg(applied_math2, MIN_AVG)

    all_students = students_se2 + students_cs2 + students_am2
    random.shuffle(all_students)

    total_len = len(all_students)

    print(f'NUMBER OF STUDENTS: {total_len}')

    p_bst = PersistentBSTTestVersion(max_ver=1000000)

    for student in all_students:
        p_bst.insert(student)

    print(f'OBJECTS IN MEMORY FOR PERSISTENT BINARY SEARCH TREE: {p_bst.total_object_count()}')
    print(f'OBJECTS IN MEMORY IF EACH TREE WAS CREATED AGAIN   : {total_len * (total_len + 1) // 2}')

    for student in students_se2:
        p_bst.remove(student)

    print('OOPS! DELETED STUDENTS FROM SE2' if all(student not in p_bst for student in students_se2) else 'FAIL')

    p_bst.undo(len(students_se2))

    print('UNDO CHANGES SUCCESSFULLY' if all(student in p_bst for student in students_se2) else 'FAIL')


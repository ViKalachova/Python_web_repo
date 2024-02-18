import random
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from conf.db import session
from conf.models import Student, Group, Professor, Subject, Grade, student_m2m_grade

fake = Faker()

def insert_students():
    for _ in range(50):
        student = Student(
            fullname=fake.name(),
            group_id=random.randint(1, 3)
        )
        session.add(student)

def insert_groups():
    for _ in range(3):
        group = Group(
            group_name=fake.word()
        )
        session.add(group)

def insert_professors():
    for _ in range(5):
        professor = Professor(
            fullname=fake.name()
        )
        session.add(professor)

def insert_subjects():
    for _ in range(5):
        subject = Subject(
            subject_name=fake.word(),
            professor_id=random.randint(1, 5)
        )
        session.add(subject)

def insert_grades():
    for _ in range(100):
        grade = Grade(
            grade=random.randint(1, 100),
            received_date=fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d'),
            subject_id=random.randint(1, 5)
        )
        session.add(grade)

def insert_rel():
    students = session.query(Student).all()
    for _ in range(100):
        student = random.choice(students)
        grade = random.randint(1, 100)
        student_grade_rel = student_m2m_grade.insert().values(student_id=student.id, grade=grade)
        session.execute(student_grade_rel)
def insert_rel():
    students = session.query(Student).all()
    for _ in range(100):
        student = random.choice(students)
        grade = random.randint(1, 100)
        student_grade_rel = student_m2m_grade.insert().values(student=student.id, grade=grade)
        session.execute(student_grade_rel)


if __name__ == '__main__':
    try:
        insert_professors()
        insert_groups()
        insert_students()
        insert_subjects()
        insert_grades()
        insert_rel()
        session.commit()
    except SQLAlchemyError as err:
        print(err)
        session.rollback()
    finally:
        session.close()

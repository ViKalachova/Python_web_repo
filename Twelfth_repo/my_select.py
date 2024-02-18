from sqlalchemy import func, desc, select, and_

from conf.db import session
from conf.models import Student, Group, Professor, Subject, Grade, student_m2m_grade


# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(Student.fullname, func.avg(Grade.grade).label('average_grade')) \
        .select_from(Student).join(student_m2m_grade).join(Grade) \
        .group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    return result

# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_name):
    result = session.query(Student.fullname, func.avg(Grade.grade).label('average_grade')) \
        .select_from(Student).join(student_m2m_grade).join(Grade).join(Subject) \
        .filter(Subject.subject_name == subject_name).group_by(Student.id).order_by(desc('average_grade')).limit(1).all()
    return result

# Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    result = session.query(Group.group_name, func.avg(Grade.grade).label('average_grade')) \
        .select_from(Group).join(Student).join(student_m2m_grade).join(Grade).join(Subject) \
        .filter(Subject.subject_name == subject_name).group_by(Group.group_name).all()
    return result

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.avg(Grade.grade).label('average_grade')).scalar()
    return result

# Знайти які курси читає певний викладач.
def select_5(professor_name):
    result = session.query(Professor.fullname, Subject.subject_name) \
        .select_from(Subject).join(Professor) \
        .filter(Professor.fullname == professor_name).all()
    return result

# Знайти список студентів у певній групі.
def select_6(group_name):
    result = session.query(Group.group_name, Student.fullname) \
        .select_from(Student).join(Group) \
        .filter(Group.group_name == group_name).all()
    return result

# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_name, subject_name):
    result = session.query(Student.fullname, Group.group_name, Subject.subject_name, Grade.grade) \
        .select_from(Group).join(Student).join(student_m2m_grade).join(Grade).join(Subject) \
        .filter(Group.group_name == group_name) \
        .filter(Subject.subject_name == subject_name).all()
    return result

# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(professor_name):
    result = session.query(Professor.fullname, Subject.subject_name, func.avg(Grade.grade).label('average_grade')) \
        .select_from(Grade).join(Subject).join(Professor) \
        .filter(Professor.fullname == professor_name).group_by(Professor.fullname, Subject.subject_name).all()
    return result

# Знайти список курсів, які відвідує певний студент.
def select_9(student_name):
    result = session.query(Student.fullname, Subject.subject_name) \
        .select_from(Student).join(student_m2m_grade).join(Grade).join(Subject) \
        .filter(Student.fullname == student_name).all()
    return result

# Список курсів, які певному студенту читає певний викладач.
def select_10(student_name, professor_name):
    result = session.query(Student.fullname, Professor.fullname, Subject.subject_name) \
        .select_from(Student).join(student_m2m_grade).join(Grade).join(Subject).join(Professor) \
        .filter(Student.fullname == student_name) \
        .filter(Professor.fullname == professor_name).all()
    return result


if __name__ == '__main__':
    print('select_1:', select_1())
    print('select_2:', select_2('animal'))
    print('select_3:', select_3('dream'))
    print('select_4:', select_4())
    print('select_5:', select_5('Nicole Morrow'))
    print('select_6:', select_6('mind'))
    print('select_7:', select_7('majority', 'recent'))
    print('select_8:', select_8('Christopher Long'))
    print('select_9:', select_9('Rebecca Thomas'))
    print('select_10:', select_10('Jerry Lopez', 'Nicole Morrow'))
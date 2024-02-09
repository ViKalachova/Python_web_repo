import sqlite3
from faker import Faker
import random

fake = Faker('uk-Ua')

conn = sqlite3.connect('grades.db')
cursor = conn.cursor()

# Додамо групи
for _ in range(3):
    group = fake.word(ext_word_list=['Група A', 'Група Б', 'Група В'])
    cursor.execute('INSERT INTO groups (group_name) VALUES (?)', (group,))

# Додамо викладачів
for _ in range(5):
    cursor.execute('INSERT INTO professors (fullname) VALUES (?)', (fake.name(),))

# Додамо предмети
for _ in range(5):
    subjects = fake.word(ext_word_list=['Вища математика', 'Фінанси', 'Страхування', 'Історія України', 'Маркетинг'])
    professor = random.randint(1, 5)
    cursor.execute('INSERT INTO subjects (subject_name, professor_id) VALUES (?, ?)', (subjects, professor))

# Додамо студентів
for _ in range(50):
    fullname = fake.name()
    group_id = random.randint(1, 3)
    cursor.execute('INSERT INTO Students (fullname, group_id) VALUES (?, ?)', (fullname, group_id))
    student_id = cursor.lastrowid
    # Додамо оцінки
    for subject_id in range(1, 6):
        for _ in range(random.randint(2, 5)):
            grade = random.randint(1, 100)
            received_date = fake.date_time_between(start_date='-1y', end_date='now').strftime('%Y-%m-%d')
            cursor.execute('INSERT INTO Grades (student_id, subject_id, grade, received_date) VALUES (?, ?, ?, ?)', (student_id, subject_id, grade, received_date))


conn.commit()
conn.close()

print("База даних успішно заповнена випадковими даними.")

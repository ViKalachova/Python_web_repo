--Знайти список курсів, які відвідує студент.

SELECT students.fullname, subjects.subject_name
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE students.fullname = 'Jeanette Morgan'; --ім'я студента, за яким здійснюється пошук

--Список курсів, які певному студенту читає певний викладач.

SELECT subjects.subject_name
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN professors ON subjects.professor_id = professors.id
WHERE students.fullname = 'Ashley Novak'   --ім'я студента, за яким здійснюється пошук
AND professors.fullname = 'Mario Hill';    --ім'я викладача, за яким здійснюється пошук

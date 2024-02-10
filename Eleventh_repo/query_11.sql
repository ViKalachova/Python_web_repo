--Середній бал, який певний викладач ставить певному студентові.

SELECT AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN professors ON subjects.professor_id = professors.id
WHERE students.fullname = 'Kristina Mcclure'    --ім'я студента, за яким здійснюється пошук
AND professors.fullname = 'Reginald Brown';  --ім'я викладача, за яким здійснюється пошук

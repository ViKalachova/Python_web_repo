--Знайти середній бал, який ставить певний викладач зі своїх предметів.

SELECT professors.fullname, subjects.subject_name, AVG(grades.grade) AS average_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
JOIN professors ON subjects.professor_id = professors.id
WHERE professors.fullname = 'Wendy Barron' --ім'я викладача, за яким здійснюється пошук
GROUP BY professors.fullname;

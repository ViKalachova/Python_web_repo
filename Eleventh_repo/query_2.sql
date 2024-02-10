--Знайти студента із найвищим середнім балом з певного предмета.

SELECT students.id,
       students.fullname,
       AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
WHERE grades.subject_id = 1 --id предмета, за яким здійснюється пошук
GROUP BY students.id
ORDER BY average_grade DESC
LIMIT 1;
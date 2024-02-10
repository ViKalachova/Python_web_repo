--Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

SELECT students.fullname,
       AVG(grades.grade) AS average_grade
FROM students
JOIN grades ON students.id = grades.student_id
GROUP BY students.id
ORDER BY average_grade DESC
LIMIT 5;
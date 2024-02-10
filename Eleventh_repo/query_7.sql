--Знайти оцінки студентів у окремій групі з певного предмета.

SELECT students.fullname, grades.grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN groups ON students.group_id = groups.id
WHERE groups.group_name = 'these' --назва групи, за якою здійснюється пошук
  AND subjects.subject_name = 'interview'; --назва предмету, за якою здійснюється пошук

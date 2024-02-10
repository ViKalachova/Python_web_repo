--Знайти список студентів у певній групі.

SELECT groups.group_name, students.fullname
FROM students
JOIN groups ON students.group_id = groups.id
WHERE groups.group_name = 'eat'; --назва групи, за якою здійснюється пошук
--Знайти середній бал у групах з певного предмета.

SELECT groups.id,
       groups.group_name,
       AVG(grades.grade) AS average_grade
FROM groups
JOIN students ON groups.id = students.group_id
JOIN grades ON students.id = grades.student_id
WHERE grades.subject_id = 1 --id предмета, за яким здійснюється пошук
GROUP BY groups.id, groups.group_name;

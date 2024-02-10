--Оцінки студентів у певній групі з певного предмета на останньому занятті.

SELECT students.fullname,
        groups.group_name,
        subjects.subject_name,
        grades.grade,
        grades.received_date
FROM students
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
JOIN groups ON students.group_id = groups.id
WHERE groups.group_name = 'eat'      --назва групи, за якою здійснюється пошук
AND subjects.subject_name = 'interview' --назва предмета, за якою здійснюється пошук
AND grades.received_date = (SELECT MAX(received_date) FROM grades);

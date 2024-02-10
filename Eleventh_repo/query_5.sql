--Знайти які курси читає певний викладач.

SELECT professors.fullname, subjects.subject_name
FROM subjects
JOIN professors ON subjects.professor_id = professors.id
WHERE professors.fullname = 'Reginald Brown'; --ім'я викладача, за яким здійснюється пошук

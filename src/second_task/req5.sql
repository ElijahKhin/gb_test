-- 5.	Вывести список отличников в прошлом учебном году. Отличник - ученик, у которого все годовые оценки 5. Допускается, что оценки за полугодие и год сохраняются в отдельных полях по итогам учебного периода.

select student_name
from student_year_grades
where year = 2023
group by student_id, student_name
having count(*) = count(*) filter (where grade_final = 5);

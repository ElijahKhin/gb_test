-- 1.	Определить среднюю оценку у мальчиков и девочек за текущий учебный год.

select
  s.gender,
  round(avg(g.grade), 2) as avg_grade
from grades g
join students s on g.student_id = s.id
where g.grade_date between date '2023-09-01' and date '2024-08-31'
group by s.gender;

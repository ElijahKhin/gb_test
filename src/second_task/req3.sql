-- 3.	Вывести учебные дисциплины и среднюю оценку одного конкретного класса по ним за текущий календарный год в порядке убывания.

select
  sub.subject,
  round(avg(g.grade), 2) as avg_grade
from grades g
join class_student cs on g.student_id = cs.student_id
join classes c on cs.class_id = c.id
join subjects sub on g.subject_id = sub.id
where c.id = 2
  and extract(year from g.grade_date) = 2023
  and g.grade between 2 and 5
group by sub.subject
order by avg_grade desc;

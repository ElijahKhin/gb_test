-- 2.	Определить количество низких оценок (2 и 3) у учеников с большим числом пятерок за предыдущий месяц (больше 15 пятерок включительно).

with date_bounds as (
  select
    date_trunc('month', '2024-02-28'::date) - interval '1 month' as month_start, -- подставить current_date
    date_trunc('month', '2024-02-28'::date) - interval '1 day' as month_end -- подставить current_date
),
students_with_many_fives as (
  select
    g.student_id
  from grades g, date_bounds db
  where g.grade = 5
    and g.grade_date between db.month_start and db.month_end
  group by g.student_id
  having count(*) >= 15
)

select * from students_with_many_fives;

select
  s.student_id,
  count(*) as low_grades_count
from grades s
join students_with_many_fives swf on s.student_id = swf.student_id,
     date_bounds db
where s.grade in (2, 3)
  and s.grade_date between db.month_start and db.month_end
group by s.student_id;

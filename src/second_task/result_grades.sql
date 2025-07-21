create or replace view quarter_grades_view as
select
  s.id as student_id,
  s.last_name || ' ' || s.first_name as student_name,
  c.id as class_id,
  sub.subject,
  extract(year from g.grade_date)::int as year,
  case
    when extract(month from g.grade_date) between 9 and 10 then 'Q1'
    when extract(month from g.grade_date) between 11 and 12 then 'Q2'
    when extract(month from g.grade_date) between 1 and 2 then 'Q3'
    when extract(month from g.grade_date) between 3 and 5 then 'Q4'
    else 'Other'
  end as quarter,
  coalesce(
    round(sum(g.grade * g.weight) / nullif(sum(g.weight), 0), 2),
    2.00
  ) as final_grade
from students s
join class_student cs on s.id = cs.student_id
join classes c on cs.class_id = c.id
left join grades g on g.student_id = s.id
  and g.grade_date between cs.start_date and coalesce(cs.end_date, g.grade_date)
left join subjects sub on g.subject_id = sub.id
group by s.id, student_name, c.id, sub.subject, year, quarter;

create or replace view semester_grades_view as
select
  s.id as student_id,
  s.last_name || ' ' || s.first_name as student_name,
  c.id as class_id,
  sub.subject,
  extract(year from g.grade_date)::int as year,
  case
    when extract(month from g.grade_date) between 9 and 12 then 'S1'
    when extract(month from g.grade_date) between 1 and 5 then 'S2'
    else 'Other'
  end as semester,
  coalesce(
    round(sum(g.grade * g.weight) / nullif(sum(g.weight), 0), 2),
    2.00
  ) as final_grade
from students s
join class_student cs on s.id = cs.student_id
join classes c on cs.class_id = c.id
left join grades g on g.student_id = s.id
  and g.grade_date between cs.start_date and coalesce(cs.end_date, g.grade_date)
left join subjects sub on g.subject_id = sub.id
group by s.id, student_name, c.id, sub.subject, year, semester;

create or replace view yearly_grades_view as
select
  s.id as student_id,
  s.last_name || ' ' || s.first_name as student_name,
  c.id as class_id,
  sub.subject,
  extract(year from g.grade_date)::int as year,
  coalesce(
    round(sum(g.grade * g.weight) / nullif(sum(g.weight), 0), 2),
    2.00
  ) as final_grade
from students s
join class_student cs on s.id = cs.student_id
join classes c on cs.class_id = c.id
left join grades g on g.student_id = s.id
  and g.grade_date between cs.start_date and coalesce(cs.end_date, g.grade_date)
left join subjects sub on g.subject_id = sub.id
group by s.id, student_name, c.id, sub.subject, year;


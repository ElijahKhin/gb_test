-- 4.	Вычислить итоговую оценку для каждого ученика за первое полугодие по любому предмету на выбор. Предусмотреть округление по стандартным математическим правилам.
select
  student_name,
  final_grade
from semester_grades_view sg
where semester = 'S1' and year = 2023 and subject = 'Математика'
order by student_name;

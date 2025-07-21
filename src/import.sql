create or replace procedure import(
	_table text,
	file_name text,
	del varchar(1) default ',',
	header boolean default True
) as $$
declare
	_path varchar;
	new_seq bigint;
begin
	select '/Users/khin/Downloads/gb_test/gb_test/data/' into _path; -- Обязательно поменять путь на свой!!!
	if header = True then
		execute format('copy %s from ''%s%s'' delimiter E''%s'' csv header', _table, _path, file_name, del);
	else
		execute format('copy %s from ''%s%s'' delimiter E''%s'' csv', _table, _path, file_name, del);
	end if;
end
$$ language plpgsql;


create or replace procedure school_import() as $$
declare 
	name_list varchar[] = array[
			['students', 'students.csv'], 
			['parents', 'parents.csv'],
      ['student_parents', 'student_parents.csv'],
			['work_types', 'work_types.csv'],
			['subjects', 'subjects.csv'],
      ['classes', 'classes.csv'],
      ['class_student', 'class_student.csv'],
      ['teachers', 'teachers.csv'],
      ['teacher_subject', 'teacher_subject.csv'],
      ['class_teacher', 'class_teacher.csv'],
      ['grades', 'grades.csv']];

	match varchar[];
begin
	foreach match slice 1 IN array name_list 
	loop
		execute format('call import(%L, %L, '','', True)', match[1], match[2]);
	end loop;
end;
$$ language plpgsql;


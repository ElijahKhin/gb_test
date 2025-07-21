\i db_setup.sql
\i fun_guard.sql
\i import.sql

set client_min_messages = 'ERROR'; --use -q to quite notifications

do $$ 
begin
	create type gender as enum('male', 'female');
	create type relationship as enum('father', 'mother', 'other');
  create type current_status as enum('graduated', 'on_leave', 'enrolled');
  create type subgroup as enum('А', 'Б', 'В', 'Г');
exception
	when duplicate_object then null;
end $$;

-- ========================
-- dim: dictionaries
-- ========================

drop table if exists work_types cascade;
create table work_types (
  id serial primary key,
  work_type varchar(100) unique not null,
  weight numeric(3,2) not null
);

drop table if exists subjects cascade;
create table subjects (
  id serial primary key,
  subject varchar(100) unique not null
);

-- ========================
-- dim: students & parents
-- ========================

drop table if exists students cascade;
create table students (
  id serial primary key,
  first_name varchar(100),
  middle_name varchar(100),
  last_name varchar(100),
  birth_date date,
  gender gender,
  document_id varchar(100),
  current_status current_status,
  enrollment_date date,
  graduation_date date,
  phone_number varchar(12)
);
alter table students
add constraint check_student_first_name check(check_name(first_name)),
add constraint check_student_middle_name check(check_name(middle_name)),
add constraint check_student_last_name check(check_name(last_name)),
add constraint check_student_phone check(check_phone(phone_number)),
add constraint check_student_birthday
check(
    extract(year from birth_date) between 2000 
    and extract(year from current_date) - 3
);

drop table if exists parents cascade;
create table parents (
  id serial primary key,
  first_name varchar(100),
  middle_name varchar(100),
  last_name varchar(100),
  phone_number varchar(12),
  email varchar(100),
  relationship relationship
);
alter table parents
add constraint check_parent_first_name check(check_name(first_name)),
add constraint check_parent_middle_name check(check_name(middle_name)),
add constraint check_parent_last_name check(check_name(last_name)),
add constraint check_parent_phone check(check_phone(phone_number)),
add constraint check_parent_email check(check_email(email));

-- ========================
-- brdg: students <-> parents
-- ========================

drop table if exists student_parents cascade;
create table student_parents (
  student_id bigint references students(id),
  parent_id bigint references parents(id),
  primary key (student_id, parent_id)
);

-- ========================
-- dim: teachers & classes 
-- ========================

drop table if exists teachers cascade;
create table teachers (
  id serial primary key,
  first_name varchar(100),
  middle_name varchar(100),
  last_name varchar(100),
  gender gender,
  document_id varchar(100),
  phone_number varchar(12),
  email varchar(100)
);
alter table teachers
add constraint check_teacher_first_name check(check_name(first_name)),
add constraint check_teacher_middle_name check(check_name(middle_name)),
add constraint check_teacher_last_name check(check_name(last_name)),
add constraint check_teacher_phone check(check_phone(phone_number)),
add constraint check_teacher_email check(check_email(email));

drop table if exists classes cascade;
create table classes (
  id serial primary key,
  start_year int,
  subgroup subgroup
);
alter table classes
add constraint check_start_year check (
  start_year between 2010 and (extract(year from current_date))::int + 1
);

-- ========================
-- brdg: class <-> teacher
-- ========================

drop table if exists class_teacher cascade;
create table class_teacher (
  class_id bigint references classes(id),
  teacher_id bigint references teachers(id),
  start_date date,
  end_date date,
  primary key (class_id, teacher_id, start_date)
);
alter table class_teacher
add constraint check_class_teacher_start_date check (
  extract(year from start_date) between 2021 and 2025
),
add constraint check_class_teacher_end_date check (
  extract(year from end_date) between 2021 and 2025
),
add constraint check_class_teacher_dates_order check (start_date <= end_date);

-- ========================
-- brdg: class <-> student
-- ========================

drop table if exists class_student cascade;
create table class_student (
  class_id bigint references classes(id),
  student_id bigint references students(id),
  start_date date,
  end_date date,
  primary key (class_id, student_id, start_date)
);
alter table class_student
add constraint check_class_student_start_date check (
  extract(year from start_date) between 2021 and 2025
),
add constraint check_class_student_end_date check (
  extract(year from end_date) between 2021 and 2025
),
add constraint check_class_student_dates_order check (start_date <= end_date);

-- ========================
-- brdg: teacher <-> subject
-- ========================

drop table if exists teacher_subject cascade;
create table teacher_subject (
  teacher_id bigint references teachers(id),
  subject_id bigint references subjects(id),
  start_date date,
  end_date date,
  primary key (teacher_id, subject_id, start_date)
);
alter table teacher_subject
add constraint check_teacher_subject_start_date check (
  extract(year from start_date) between 2021 and extract(year from current_date) + 1
),
add constraint check_teacher_subject_end_date check (
  extract(year from end_date) between 2021 and extract(year from current_date)
),
add constraint check_teacher_subject_dates_order check (start_date <= end_date);


-- ===================
-- fct: regular_grades 
-- ===================

drop table if exists grades cascade;
create table grades (
  id serial primary key,
  student_id bigint not null references students(id),
  subject_id bigint not null references subjects(id),
  teacher_id bigint not null references teachers(id),
  work_type_id int not null references work_types(id),
  grade numeric(3,2) check (grade between 1 and 5),
  weight numeric(3,2) default 1.0,
  grade_date date not null,
  comment text
);
alter table grades
add constraint check_grade_date check (
  extract(year from grade_date) between 2021 and extract(year from current_date)
);

call school_import();

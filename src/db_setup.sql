\c postgres;

drop database if exists glow;
create database glow;

\c glow;

drop role if exists school_admin;
create role school_admin
    with login
    password 'admin123'
    createdb createrole;

drop role if exists school_analyst;
create role school_analyst
    with login
    password 'analyst123';

drop role if exists school_readonly;
create role school_readonly
    with login
    password 'readonly123';

create schema school authorization school_admin;
alter role school_admin set search_path to school;
alter role school_analyst set search_path to school;
alter role school_readonly set search_path to school;

grant usage on schema school to school_analyst, school_readonly;

alter default privileges in schema school
grant select on tables to school_analyst, school_readonly;

alter default privileges in schema school
grant insert, update on tables to school_analyst;

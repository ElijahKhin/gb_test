create or replace function check_name(name_text text)
returns boolean as $$
declare
    is_valid boolean;
begin
    is_valid := name_text ~ '(^[А-ЯЁ]{1}[а-яё\- ]{1,}$)';
    return is_valid;
end;
$$ language plpgsql;

create or replace function check_email(email_text text)
returns boolean as $$
declare
  is_valid boolean;
begin
  is_valid := email_text ~ '^[\w\.]+@([\w]+\.)+[\w]{2,4}$';
  return is_valid;
end;
$$ language plpgsql;

create or replace function check_phone(phone_text text)
returns boolean as $$
declare
  is_valid boolean;
begin
  is_valid := phone_text ~ '(^\+{1}7{1}[0-9]{10}$)';
  return is_valid;
end;
$$ language plpgsql;

import pandas as pd
from faker import Faker
import random
from datetime import date, datetime

fake = Faker('ru_RU')

CURRENT_YEAR = 2024
START_YEAR = 2021

gender_choices = ['male', 'female']

def generate_phone():
    return '+7' + ''.join([str(random.randint(0, 9)) for _ in range(10)])

def generate_birth_date(age):
    return fake.date_of_birth(minimum_age=age, maximum_age=age)

def generate_students_for_year(year):
    students = []
    count = random.randint(500, 700)

    for _ in range(count):
        gender = random.choice(gender_choices)
        if gender == 'male':
            first = fake.first_name_male()
            middle = fake.middle_name_male()
            last = fake.last_name_male()
        else:
            first = fake.first_name_female()
            middle = fake.middle_name_female()
            last = fake.last_name_female()

        age_at_enroll = random.randint(7, 18)
        birth_date = generate_birth_date(age_at_enroll)
        enrollment_date = date(year, 9, 1)

        if year == CURRENT_YEAR:
            current_status = random.choices(['enrolled', 'on_leave'], weights=[0.9, 0.1])[0]
            graduation_date = None
        elif year < CURRENT_YEAR:
            current_status = 'graduated'
            graduation_date = enrollment_date.replace(year=enrollment_date.year + 1)
        else:
            current_status = 'enrolled'
            graduation_date = None

        student = {
            'first_name': first,
            'middle_name': middle,
            'last_name': last,
            'birth_date': birth_date,
            'gender': gender,
            'document_id': fake.unique.bothify(text='??######'),
            'current_status': current_status,
            'enrollment_date': enrollment_date,
            'graduation_date': graduation_date,
            'phone_number': generate_phone()
        }

        students.append(student)

    return students

all_students = []
for year in range(START_YEAR, CURRENT_YEAR + 1):
    all_students.extend(generate_students_for_year(year))

df = pd.DataFrame(all_students)

df.insert(0, 'id', range(1, len(df) + 1))

df.to_csv('../data/students.csv', index=False)

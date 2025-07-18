import pandas as pd
from faker import Faker
import random

fake = Faker('ru_RU')

relationship_choices = ['mother', 'father', 'other']
gender_choices = ['male', 'female']

# Загружаем студентов
students_df = pd.read_csv('../data/students.csv')
parents = []
student_parents = []
parent_id_counter = 1
parent_pool = {}

def generate_parent(gender):
    if gender == 'male':
        first = fake.first_name_male()
        middle = fake.middle_name_male()
        last = fake.last_name_male()
        relationship = 'father'
    elif gender == 'female':
        first = fake.first_name_female()
        middle = fake.middle_name_female()
        last = fake.last_name_female()
        relationship = 'mother'
    else:
        first = fake.first_name()
        middle = fake.first_name()
        last = fake.last_name()
        relationship = 'other'

    phone = fake.unique.phone_number()
    email = fake.unique.email()

    return {
        'first_name': first,
        'middle_name': middle,
        'last_name': last,
        'phone_number': '+7' + ''.join([str(random.randint(0, 9)) for _ in range(10)]),
        'email': email,
        'relationship': relationship
    }

for _, student in students_df.iterrows():
    num_parents = random.choice([1, 2])
    used_phones = set()

    for _ in range(num_parents):
        gender = random.choice(['male', 'female'])
        parent = generate_parent(gender)

        # Уникальность по ФИО и телефону
        parent_key = (parent['first_name'], parent['middle_name'], parent['last_name'], parent['phone_number'])

        if parent_key in parent_pool:
            parent_id = parent_pool[parent_key]
        else:
            parent_id = parent_id_counter
            parent_pool[parent_key] = parent_id
            parent['id'] = parent_id
            parents.append(parent)
            parent_id_counter += 1

        student_parents.append({
            'student_id': student['id'],
            'parent_id': parent_id
        })

# Сохраняем в CSV
parents_df = pd.DataFrame(parents)
parents_df = parents_df[['id', 'first_name', 'middle_name', 'last_name', 'phone_number', 'email', 'relationship']]
parents_df.to_csv('parents.csv', index=False)

student_parents_df = pd.DataFrame(student_parents)
student_parents_df.to_csv('../data/student_parents.csv', index=False)


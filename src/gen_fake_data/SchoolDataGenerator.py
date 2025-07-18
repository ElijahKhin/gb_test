import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta, date
import os

class SchoolDataGenerator:
    def __init__(self):
        self.fake = Faker('ru_RU')
        self.START_YEAR = 2021
        self.CURRENT_YEAR = 2024
        self.STUDENTS_PER_YEAR_RANGE = (500, 700)
        self.gender_choices = ['male', 'female']
        self.relationship_choices = ['mother', 'father', 'other']

        # Paths
        self.base_path = '../data/'
        os.makedirs(self.base_path, exist_ok=True)

        # Storage
        self.students = []
        self.parents = []
        self.student_parents = []
        self.parent_pool = {}
        self.parent_id_counter = 1

    def generate_phone(self):
        return '+7' + ''.join([str(random.randint(0, 9)) for _ in range(10)])

    def generate_birth_date(self, age):
        return self.fake.date_of_birth(minimum_age=age, maximum_age=age)

    def generate_students(self):
        id_counter = 1
        for year in range(self.START_YEAR, self.CURRENT_YEAR + 1):
            count = random.randint(*self.STUDENTS_PER_YEAR_RANGE)
            for _ in range(count):
                gender = random.choice(self.gender_choices)
                if gender == 'male':
                    first = self.fake.first_name_male()
                    middle = self.fake.middle_name_male()
                    last = self.fake.last_name_male()
                else:
                    first = self.fake.first_name_female()
                    middle = self.fake.middle_name_female()
                    last = self.fake.last_name_female()

                age_at_enroll = random.randint(7, 18)
                birth_date = self.generate_birth_date(age_at_enroll)
                enrollment_date = date(year, 9, 1)

                if year == self.CURRENT_YEAR:
                    current_status = random.choices(['enrolled', 'on_leave'], weights=[0.9, 0.1])[0]
                    graduation_date = None
                else:
                    current_status = 'graduated'
                    graduation_date = enrollment_date.replace(year=enrollment_date.year + 1)

                student = {
                    'id': id_counter,
                    'first_name': first,
                    'middle_name': middle,
                    'last_name': last,
                    'birth_date': birth_date,
                    'gender': gender,
                    'document_id': self.fake.unique.bothify(text='??######'),
                    'current_status': current_status,
                    'enrollment_date': enrollment_date,
                    'graduation_date': graduation_date,
                    'phone_number': self.generate_phone()
                }
                self.students.append(student)
                id_counter += 1

        df = pd.DataFrame(self.students)
        df.to_csv(os.path.join(self.base_path, 'students.csv'), index=False)

    def generate_parent(self, gender):
        if gender == 'male':
            first, middle, last = self.fake.first_name_male(), self.fake.middle_name_male(), self.fake.last_name_male()
            relationship = 'father'
        elif gender == 'female':
            first, middle, last = self.fake.first_name_female(), self.fake.middle_name_female(), self.fake.last_name_female()
            relationship = 'mother'
        else:
            first, middle, last = self.fake.first_name(), self.fake.first_name(), self.fake.last_name()
            relationship = 'other'

        email = self.fake.unique.email()
        phone = self.generate_phone()

        return {
            'first_name': first,
            'middle_name': middle,
            'last_name': last,
            'phone_number': phone,
            'email': email,
            'relationship': relationship
        }

    def generate_parents_and_links(self):
        for student in self.students:
            num_parents = random.choice([1, 2])
            for _ in range(num_parents):
                gender = random.choice(self.gender_choices)
                parent = self.generate_parent(gender)
                parent_key = (parent['first_name'], parent['middle_name'], parent['last_name'], parent['phone_number'])

                if parent_key in self.parent_pool:
                    parent_id = self.parent_pool[parent_key]
                else:
                    parent_id = self.parent_id_counter
                    self.parent_pool[parent_key] = parent_id
                    parent['id'] = parent_id
                    self.parents.append(parent)
                    self.parent_id_counter += 1

                self.student_parents.append({
                    'student_id': student['id'],
                    'parent_id': parent_id
                })

        pd.DataFrame(self.parents)[['id', 'first_name', 'middle_name', 'last_name', 'phone_number', 'email', 'relationship']].to_csv(os.path.join(self.base_path, 'parents.csv'), index=False)

        pd.DataFrame(self.student_parents).to_csv(os.path.join(self.base_path, 'student_parents.csv'), index=False)

    def generate_classes(self):
    class_records = []
    class_id = 1

    for year in range(2021, self.CURRENT_YEAR + 1):
        for grade in range(1, 12):  # классы с 1 по 11
            num_subgroups = random.randint(2, 4)
            subgroups = random.sample(['А', 'Б', 'В', 'Г'], num_subgroups)

            for subgroup in subgroups:
                class_records.append({
                    'id': class_id,
                    'start_year': year,
                    'subgroup': subgroup
                })
                class_id += 1

    df = pd.DataFrame(class_records)
    df.to_csv('../data/classes.csv', index=False)

    def generate_teachers_and_subjects(self):
    subjects_df = pd.read_csv('../data/subjects.csv')
    all_subjects = subjects_df['subject'].tolist()
    teacher_id = 1
    teacher_subject_records = []
    teacher_records = []

    for subject in all_subjects:
        num_teachers = random.randint(3, 5)

        for _ in range(num_teachers):
            gender = random.choice(self.gender_choices)
            if gender == 'male':
                first = self.fake.first_name_male()
                middle = self.fake.middle_name_male()
                last = self.fake.last_name_male()
            else:
                first = self.fake.first_name_female()
                middle = self.fake.middle_name_female()
                last = self.fake.last_name_female()

            document_id = self.fake.unique.bothify(text='??######')
            phone_number = self.generate_phone()
            email = self.fake.unique.email()

            teacher = {
                'id': teacher_id,
                'first_name': first,
                'middle_name': middle,
                'last_name': last,
                'gender': gender,
                'document_id': document_id,
                'phone_number': phone_number,
                'email': email
            }
            teacher_records.append(teacher)

            # Назначения учителя (возможно несколько предметов)
            num_subjects = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
            chosen_subjects = random.sample(all_subjects, num_subjects)

            for subj in chosen_subjects:
                subj_id = subjects_df[subjects_df['subject'] == subj].iloc[0]['id']

                start_year = random.randint(2021, self.CURRENT_YEAR)
                end_year = random.randint(start_year, self.CURRENT_YEAR)

                start_date = f'{start_year}-09-01'
                end_date = f'{end_year}-06-01'

                teacher_subject_records.append({
                    'teacher_id': teacher_id,
                    'subject_id': subj_id,
                    'start_date': start_date,
                    'end_date': end_date
                })

            teacher_id += 1

        # Сохраняем
        pd.DataFrame(teacher_records).to_csv('../data/teachers.csv', index=False)
        pd.DataFrame(teacher_subject_records).to_csv('../data/teacher_subject.csv', index=False)


    def generate_all(self):
        self.generate_students()
        self.generate_parents_and_links()
        self.generate_classes()
        self.generate_teachers_and_subjects()
        print("[INFO] CSV files successfully generated.")


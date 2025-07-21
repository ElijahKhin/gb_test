import pandas as pd
import random
import datetime
import numpy as np
from faker import Faker
import os


class dummySchoolData:
    def __init__(self, start_year=2021, current_date=None, seed=None):
        self.start_year = start_year
        self.current_date = current_date or datetime.date(2024, 2, 1)
        self.faker = Faker('ru_RU')
        self.path = '../'

        if seed is not None:
            Faker.seed(seed)
            random.seed(seed)
            np.random.seed(seed)
        self.init_buffers()

    def init_buffers(self):
        self.subjects = []

    def getDummyData(self):
        self.genSubjects()
        self.genWorkTypes()
        self.generateTeachers()
        self.assignSubjectsToTeachers()
        self.genClasses()
        self.assignClassTeachers()
        self.genStudents()
        self.genParents()
        self.genGrades()


    def genSubjects(self):
        os.makedirs(self.path, exist_ok=True)

        subject_list = [
            "Математика", "Русский язык", "Литература", "Английский язык",
            "История", "Обществознание", "География", "Биология",
            "Химия", "Физика", "Музыка", "Технология", "Физкультура",
            "ИЗО", "ОБЖ", "Информатика", "Экология", "Астрономия"
        ]

        df = pd.DataFrame({
            "id": range(1, len(subject_list) + 1),
            "subject": subject_list
        })

        self.subjects = df
        df.to_csv(f"{self.path}/subjects.csv", index=False)

    def genWorkTypes(self):
        os.makedirs(self.path, exist_ok=True)

        work_type_list = [
            ("Итоговая работы", 0.3),
            ("Контрольная работа", 0.15),
            ("Проект", 0.15),
            ("Самостоятельная работа", 0.1),
            ("Лабораторная работа", 0.1),
            ("Практическая работа", 0.1),
            ("Тест", 0.04),
            ("Домашняя работа", 0.04),
            ("Устный ответ", 0.02)
        ]

        df = pd.DataFrame({
            "id": range(1, len(work_type_list) + 1),
            "work_type": [wt[0] for wt in work_type_list],
            "weight": [wt[1] for wt in work_type_list]
        })

        self.work_types = df
        df.to_csv(f"{self.path}/work_types.csv", index=False)

    def generateTeachers(self, count=30):
        os.makedirs(self.path, exist_ok=True)

        teachers = []
        for i in range(count):
            gender = random.choice(["male", "female"])
            if gender == "male":
                last = self.faker.last_name_male()
                first = self.faker.first_name_male()
                middle = self.faker.middle_name_male()
            else:
                last = self.faker.last_name_female()
                first = self.faker.first_name_female()
                middle = self.faker.middle_name_female()

            teacher = {
                "id": i + 1,
                "firstName": first,
                "middleName": middle,
                "lastName": last,
                "gender": gender,
                "documentId": f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}",
                "phoneNumber": f"+7{random.randint(9000000000, 9999999999)}",
                "email": self.faker.email()
            }
            teachers.append(teacher)

        df = pd.DataFrame(teachers)
        self.teachers = df
        df.to_csv(f"{self.path}/teachers.csv", index=False)

    def assignSubjectsToTeachers(self, maxSubjectsPerTeacher=3):
        os.makedirs(self.path, exist_ok=True)

        assignments = []
        for _, teacher in self.teachers.iterrows():
            subject_count = random.randint(1, maxSubjectsPerTeacher)
            subjects_sample = self.subjects.sample(subject_count)

            for _, subject in subjects_sample.iterrows():
                start_year = random.randint(self.start_year, 2023)
                start_date = datetime.date(start_year, random.randint(1, 12), random.randint(1, 28))

                if start_year == 2023:
                    end_date = None
                else:
                    end_year = random.randint(start_year, 2023)
                    end_date = datetime.date(end_year, random.randint(1, 12), random.randint(1, 28))
                    if end_date < start_date:
                        end_date = start_date

                assignments.append({
                    "teacher_id": teacher["id"],
                    "subject_id": subject["id"],
                    "start_date": start_date,
                    "end_date": end_date
                    })

        df = pd.DataFrame(assignments)
        self.teacherSubjects = df
        df.to_csv(f"{self.path}/teacher_subject.csv", index=False)

    def genClasses(self):
        os.makedirs(self.path, exist_ok=True)
    
        classes = []
        for grade in range(1, 12):
            for subgroup in ['А', 'Б']:
                classes.append({
                    "id": len(classes) + 1,
                    "start_year": 2010 + grade - 1,
                    "subgroup": subgroup
                })
    
        df = pd.DataFrame(classes)
        self.classes = df
        df.to_csv(f"{self.path}/classes.csv", index=False)

    def assignClassTeachers(self):
        os.makedirs(self.path, exist_ok=True)

        class_teachers = []

        for _, class_ in self.classes.iterrows():
            # Решаем, сколько смен классного руководителя будет (1 или 2)
            num_changes = random.choice([1, 2])

            current_start = datetime.date(class_["start_year"], 9, 1)  # начало учебного года

            for i in range(num_changes):
                # Берём случайного учителя
                teacher = self.teachers.sample(1).iloc[0]

                # Определяем end_date для периода руководства
                if i == num_changes - 1:
                    end_date = self.current_date  # текущий период до текущей даты
                else:
                    next_year = current_start.year + random.randint(1, 2)
                    # конец учебного года или не позже текущей даты
                    end_date = datetime.date(min(next_year, self.current_date.year), 6, 30)
                    if end_date > self.current_date:
                        end_date = self.current_date

                class_teachers.append({
                    "class_id": class_["id"],
                    "teacher_id": teacher["id"],
                    "start_date": datetime.date(2021, 9, 1),
                    "end_date": datetime.date(2025, 9, 1)
                })

                # Следующий период начинается сразу после предыдущего
                current_start = end_date + datetime.timedelta(days=1)
                if current_start > self.current_date:
                    break

        df = pd.DataFrame(class_teachers)
        self.classTeachers = df
        df.to_csv(f"{self.path}/class_teacher.csv", index=False)

    def genStudents(self):
        os.makedirs(self.path, exist_ok=True)
    
        students = []
        class_students = []
    
        student_id_counter = 1
    
        for _, class_ in self.classes.iterrows():
            num_students = random.randint(23, 29)
    
            # Класс (grade) от 1 до 11, считаем по start_year относительно self.start_year
            grade = (class_["start_year"] - self.start_year) + 1
            age_at_start = 5 + grade  # Возраст для поступления в класс, например 6 лет для 1-го класса
    
            for _ in range(num_students):
                gender = random.choice(['male', 'female'])
                first_name = self.faker.first_name_male() if gender == 'male' else self.faker.first_name_female()
                middle_name = self.faker.middle_name()
                last_name = self.faker.last_name()
    
                birth_date = self.faker.date_of_birth(tzinfo=None, minimum_age=6, maximum_age=17)
    
                # Определяем статус: если 11 класс уже окончен - graduated, иначе enrolled
                current_status = 'enrolled'
                graduation_date = None
                if grade == 11 and class_["start_year"] + 10 <= self.current_date.year:
                    current_status = 'graduated'
                    graduation_date = datetime.date(class_["start_year"] + 10, 6, 30)
    
                enrollment_date = datetime.date(class_["start_year"], 9, 1)
    
                phone_number = '+7' + ''.join([str(random.randint(0,9)) for _ in range(10)])
    
                students.append({
                    "id": student_id_counter,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "birth_date": birth_date,
                    "gender": gender,
                    "document_id": f"{random.randint(1000,9999)} {random.randint(100000,999999)}",
                    "current_status": current_status,
                    "enrollment_date": enrollment_date,
                    "graduation_date": graduation_date,
                    "phone_number": phone_number
                })
    
                end_date = graduation_date if graduation_date else self.current_date
    
                class_students.append({
                    "class_id": class_["id"],
                    "student_id": student_id_counter,
                    "start_date": datetime.date(2021, 9, 1),
                    "end_date": end_date
                })
    
                student_id_counter += 1
    
        df_students = pd.DataFrame(students)
        df_class_students = pd.DataFrame(class_students)
    
        self.students = df_students
        self.classStudents = df_class_students
    
        df_students.to_csv(f"{self.path}/students.csv", index=False)
        df_class_students.to_csv(f"{self.path}/class_student.csv", index=False)

    def genParents(self):
        os.makedirs(self.path, exist_ok=True)

        parents = []
        student_parents = []

        parent_id_counter = 1

        for _, student in self.students.iterrows():
            num_parents = random.choices([1, 2], weights=[0.15, 0.85])[0]  # 85% с двумя родителями, 15% с одним

            parent_ids_for_student = []

            for _ in range(num_parents):
                gender = 'male' if len(parent_ids_for_student) == 0 else 'female'  # пусть первый — папа, второй — мама
                first_name = self.faker.first_name_male() if gender == 'male' else self.faker.first_name_female()
                middle_name = self.faker.middle_name()
                last_name = student["last_name"]  # родители и дети обычно имеют одинаковую фамилию

                phone_number = '+7' + ''.join([str(random.randint(0,9)) for _ in range(10)])
                email = self.faker.email()

                relationship = 'father' if gender == 'male' else 'mother'

                parents.append({
                    "id": parent_id_counter,
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "last_name": last_name,
                    "phone_number": phone_number,
                    "email": email,
                    "relationship": relationship
                })

                student_parents.append({
                    "student_id": student["id"],
                    "parent_id": parent_id_counter
                })

                parent_ids_for_student.append(parent_id_counter)
                parent_id_counter += 1

        df_parents = pd.DataFrame(parents)
        df_student_parents = pd.DataFrame(student_parents)

        self.parents = df_parents
        self.studentParents = df_student_parents

        df_parents.to_csv(f"{self.path}/parents.csv", index=False)
        df_student_parents.to_csv(f"{self.path}/student_parents.csv", index=False)
    def genGrades(self):
        os.makedirs(self.path, exist_ok=True)

        grades = []

        # Период учебного года: сентябрь 2023 - февраль 2024
        start_date = datetime.date(2023, 9, 1)
        end_date = datetime.date(2024, 2, 28)

        # Для удобства — словарь work_type_id и веса
        work_types_weights = dict(zip(self.work_types['id'], self.work_types['weight']))

        for _, student_row in self.students.iterrows():
            student_id = student_row['id']

            # Узнаем, в каких классах учился ученик в период оценок
            student_classes = self.classStudents[
                (self.classStudents['student_id'] == student_id) &
                (self.classStudents['start_date'] <= end_date) &
                ((self.classStudents['end_date'] >= start_date) | (self.classStudents['end_date'].isna()))
            ]

            for _, cs_row in student_classes.iterrows():
                class_id = cs_row['class_id']

                # Какие предметы преподавались в этом классе в период оценки
                # И какие учителя вели предметы в это время
                class_teachers = self.classTeachers[
                    (self.classTeachers['class_id'] == class_id) &
                    (self.classTeachers['start_date'] <= end_date) &
                    ((self.classTeachers['end_date'] >= start_date) | (self.classTeachers['end_date'].isna()))
                ]

                for _, ct_row in class_teachers.iterrows():
                    teacher_id = ct_row['teacher_id']

                    # Какие предметы вел учитель в период
                    teacher_subjects = self.teacherSubjects[
                        (self.teacherSubjects['teacher_id'] == teacher_id) &
                        (self.teacherSubjects['start_date'] <= end_date) &
                        ((self.teacherSubjects['end_date'] >= start_date) | (self.teacherSubjects['end_date'].isna()))
                    ]

                    for _, ts_row in teacher_subjects.iterrows():
                        subject_id = ts_row['subject_id']

                        # Генерируем оценки по разным видам работ
                        for _, wt_row in self.work_types.iterrows():
                            # Решаем, ставим ли оценку для данного типа работы (чтобы не было одинаковых всегда)
                            if random.random() < 0.7:  # 70% шанс поставить оценку
                                grade_date = self.faker.date_between_dates(date_start=start_date, date_end=end_date)
                                grade_value = round(random.choices([2,3,4,5], weights=[0.1,0.2,0.4,0.3])[0], 2)

                                grades.append({
                                    "id": len(grades) + 1,
                                    "student_id": student_id,
                                    "subject_id": subject_id,
                                    "teacher_id": teacher_id,
                                    "work_type_id": wt_row['id'],
                                    "grade": grade_value,
                                    "weight": wt_row['weight'],
                                    "grade_date": grade_date,
                                    "comment": None
                                })

        df_grades = pd.DataFrame(grades)
        self.grades = df_grades
        df_grades.to_csv(f"{self.path}/grades.csv", index=False)



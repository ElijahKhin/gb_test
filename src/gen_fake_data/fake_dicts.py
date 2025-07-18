import pandas as pd

# 1. Work types with weights
work_types_data = [
    ("Домашняя работа", 0.10),
    ("Контрольная работа", 0.30),
    ("Самостоятельная работа", 0.15),
    ("Лабораторная работа", 0.20),
    ("Практическая работа", 0.15),
    ("Проект", 0.25),
    ("Тест", 0.20),
    ("Экзамен", 0.40),
    ("Ответ у доски", 0.10),
    ("Проверочная работа", 0.25)
]
df_work = pd.DataFrame(work_types_data, columns=["work_type", "weight"])
df_work.to_csv("work_types.csv", index_label="id")

# 2. Period types
period_types = ["quarter", "semester", "yearly"]
df_periods = pd.DataFrame({'period_type': period_types})
df_periods.to_csv("period_types.csv", index_label="id")

# 3. Subjects
subjects = [
    "Математика", "Алгебра", "Геометрия", "Русский язык", "Литература", "История",
    "Обществознание", "Биология", "Физика", "Химия", "География", "Информатика",
    "Английский язык", "Технология", "ИЗО", "Музыка", "Физкультура"
]
df_subjects = pd.DataFrame({'subject': subjects})
df_subjects.to_csv("../data/subjects.csv", index_label="id")


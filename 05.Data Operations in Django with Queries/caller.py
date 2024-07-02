import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Student


def add_students():
    student = Student()
    student.student_id = "FC5204"
    student.first_name = "John"
    student.last_name = "Doe"
    student.birth_date = "1995-05-15"
    student.email = "john.doe@university.com"
    student.save()

    Student.objects.create(
        student_id="FE0054",
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@university.com",
    )

    Student.objects.create(
        student_id="FH2014",
        first_name="Alice",
        last_name="Johnson",
        birth_date="1998-02-10",
        email="alice.johnson@university.com",
    )

    Student.objects.create(
        student_id="FH2015",
        first_name="Bob",
        last_name="Wilson",
        birth_date="1996-11-25",
        email="bob.wilson@university.com",
    )


def get_students_info():
    result = []
    students = Student.objects.all()

    for s in students:
        result.append(f"Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}")

    return "\n".join(result)


def update_students_emails():
    students = Student.objects.all()

    for s in students:
        s.email = s.email.replace(s.email.split("@")[1], "uni-students.com")
        s.save()


def truncate_students():
    students = Student.objects.all()
    for s in students:
        s.delete()


# Run and print your queries
#
# add_students()
# print(Student.objects.all())

# print(get_students_info())
# update_students_emails()
# for student in Student.objects.all():
#     print(student.email)

#
# truncate_students()
# print(Student.objects.all())
# print(f"Number of students: {Student.objects.count()}")

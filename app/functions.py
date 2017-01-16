from .models import Semester, Group, Classes, ClassesDate, Student, Topic
from .helpers import *


def create_group_from_files(upload_grp, upload_sem):
    upload_grp_lines = upload_grp.readlines()
    upload_sem_lines = upload_sem.readlines()

    group_data_list = []
    sem_data_list = []

    for line in upload_grp_lines:
        line = (line.decode('utf-8')).strip()
        group_data_list.append(line)

    for line in upload_sem_lines:
        line = (line.decode('utf-8')).strip()
        sem_data_list.append(line)

    group_data_first_line = group_data_list[0].split(' -- ')
    academic_year = group_data_first_line[0].split()[-1]
    sem_type = group_data_first_line[1].split()[-1]
    studies_type = group_data_first_line[2].split()[-1]
    grade = group_data_first_line[3].split()[0]
    grade_arabic = roman_to_arabic(grade)
    year_of_study = group_data_first_line[4].split()[0]
    year_of_study_arabic = roman_to_arabic(year_of_study)
    sem_nr = group_data_first_line[5].split()[0]

    group_data_second_line = group_data_list[1].split(' -- ')
    specialization = group_data_second_line[0]
    subject = ' '.join(group_data_second_line[1].split()[:-1])
    classes_type = group_data_second_line[1].split()[-1]

    group_data_third_line = group_data_list[2].split()
    first_date = group_data_third_line[0]
    start_time = group_data_third_line[1].split('-')[0]
    end_time = group_data_third_line[1].split('-')[1]
    place = group_data_third_line[2]

    students = []
    for student in group_data_list[3:]:
        student_data = {'surname': student.split()[0], 'name': student.split()[1]}
        students.append(student_data)

    last_day_sem = sem_data_list[0]
    holiday_start = str_to_date(sem_data_list[1].split()[0])
    holiday_end = str_to_date(sem_data_list[1].split()[1])
    day_off = sem_data_list[2].split()
    not_stationary_dates = sem_data_list[3].split()

    try:
        semester = Semester.objects.get(academic_year=academic_year, sem_type=get_sem_type(sem_type))
    except Semester.DoesNotExist:
        semester = Semester(academic_year=academic_year, sem_type=get_sem_type(sem_type))
        semester.save()

    try:
        Group.objects.get(
            specialization=specialization,
            stationary=is_stationary(studies_type),
            grade=grade_arabic,
            year_of_study=year_of_study_arabic,
            sem_nr=sem_nr,
            semester=semester,
            classes__subject=subject,
            classes__classes_type=get_classes_type(classes_type)
        )
        return "Taka grupa już istnieje."
    except Group.DoesNotExist:
        group = Group(
            short_name=get_short_name(specialization, is_stationary(studies_type), grade, year_of_study, sem_nr),
            specialization=specialization,
            stationary=is_stationary(studies_type),
            grade=grade_arabic,
            year_of_study=year_of_study_arabic,
            sem_nr=sem_nr,
            semester=semester
        )
        group.save()

        classes = Classes(
            subject=subject,
            classes_type=get_classes_type(classes_type),
            start_time=str_to_time(start_time),
            end_time=str_to_time(end_time),
            place=place,
            group=group
        )
        classes.save()

        if studies_type == 'niestacjonarne':
            if str_to_date(first_date) == str_to_date(not_stationary_dates[0]):
                for i, date in enumerate(not_stationary_dates, start=1):
                    ClassesDate(date=str_to_date(date), nr_of_week=i, classes=classes).save()
            else:
                for i, date in enumerate(not_stationary_dates, start=1):
                    ClassesDate(date=str_to_date(date) + datetime.timedelta(days=1), nr_of_week=i, classes=classes).save()
        else:
            current_date = str_to_date(first_date)
            max_date = str_to_date(last_day_sem)
            day_off_dates = []
            for date in day_off:
                day_off_dates.append(str_to_date(date))

            i = 0
            while current_date <= max_date:
                i += 1
                if (current_date < holiday_start or current_date > holiday_end) and (current_date not in day_off_dates):
                    ClassesDate(date=current_date, nr_of_week=i, classes=classes).save()
                else:
                    i -= 1
                current_date = current_date + datetime.timedelta(days=7)

        for student in students:
            Student(name=student['name'], surname=student['surname'], group=group).save()

        try:
            active_semester = Semester.objects.get(active=True)
            if active_semester != semester:
                active_semester.active = False
                semester.active = True
                active_semester.save()
                semester.save()
        except Semester.DoesNotExist:
            semester.active = True
            semester.save()

        return "Pomyślnie utworzono grupę."


def import_topics(group_id, upload_topic):
    uploaded_lines = upload_topic.readlines()
    uploaded_list = []

    classesdates_size = ClassesDate.objects.filter(classes_id=group_id).count()

    if classesdates_size < len(uploaded_lines):
        return "Za mało zajęć."
    else:
        for i, line in enumerate(uploaded_lines, start=1):
            line = (line.decode('utf-8')).strip()
            topic, created = Topic.objects.update_or_create(
                classesdate=ClassesDate.objects.get(classes_id=group_id, nr_of_week=i),
                defaults={'topic': line}
            )

    return "Zaimportowano tematy."

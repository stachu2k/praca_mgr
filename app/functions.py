from .models import Semester


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
    year_of_study = group_data_first_line[4].split()[0]
    sem_nr = group_data_first_line[5].split()[0]

    Semester.objects.get(academic_year=academic_year)

    return group_data_first_line

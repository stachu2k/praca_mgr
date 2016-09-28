from django.db import models


class Semester(models.Model):
    LETNI = 'l'
    ZIMOWY = 'z'
    SEM_CHOICES = (
        (LETNI, 'letni'),
        (ZIMOWY, 'zimowy'),
    )
    academic_year = models.CharField(max_length=7)
    sem_type = models.CharField(max_length=1, choices=SEM_CHOICES, default=ZIMOWY)


class Group(models.Model):
    PIERWSZY = '1'
    DRUGI = '2'
    TRZECI = '3'
    GRADES = (
        (PIERWSZY, 'I-ST'),
        (DRUGI, 'II-ST'),
        (TRZECI, 'III-ST'),
    )
    specialization = models.CharField(max_length=50)
    stationary = models.BooleanField(default=True)
    grade = models.CharField(max_length=1, choices=GRADES, default=PIERWSZY)
    year_of_study = models.SmallIntegerField()
    sem_nr = models.SmallIntegerField()
    semester = models.ForeignKey(Semester)


class Student(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    group = models.ForeignKey(Group)


class Classes(models.Model):
    WYKLAD = 'WYK'
    CWICZENIA = 'CW'
    LABORATORIUM = 'LAB'
    PROJEKT = 'PR'
    SEMINARIUM = 'SEM'
    CLASSES = (
        (WYKLAD, 'Wykład'),
        (CWICZENIA, 'Ćwiczenia'),
        (LABORATORIUM, 'Laboratorium'),
        (PROJEKT, 'Projekt'),
        (SEMINARIUM, 'Seminarium dyplomowe'),
    )
    subject = models.CharField(max_length=100)
    classes_type = models.CharField(max_length=3, choices=CLASSES, default=WYKLAD)
    start_time = models.TimeField()
    end_time = models.TimeField()
    group = models.OneToOneField(Group, primary_key=True)


class ClassesDate(models.Model):
    date = models.DateField()
    nr_of_week = models.SmallIntegerField()
    classes = models.ForeignKey(Classes)


class Presence(models.Model):
    OBECNY = 'O'
    NIEOBECNY = 'N'
    SPOZNIONY = 'S'
    USPRAWIEDLIWIONY = 'U'
    PRESENCE_CHOICES = (
        (OBECNY, 'obecny'),
        (NIEOBECNY, 'nieobecny'),
        (SPOZNIONY, 'spóźniony'),
        (USPRAWIEDLIWIONY, 'usprawiedliwiony'),
    )
    presence_type = models.CharField(max_length=3, choices=PRESENCE_CHOICES)
    student = models.ForeignKey(Student)
    classes_date = models.ForeignKey(ClassesDate)

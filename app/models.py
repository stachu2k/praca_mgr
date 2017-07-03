# -*- coding: utf-8 -*-

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
    active = models.BooleanField(default=False)


class Group(models.Model):
    PIERWSZY = '1'
    DRUGI = '2'
    TRZECI = '3'
    CZWARTY = '4'
    PIATY = '5'
    SZOSTY = '6'
    SIODMY = '7'
    GRADES = (
        (PIERWSZY, 'I'),
        (DRUGI, 'II'),
        (TRZECI, 'III'),
        (CZWARTY, 'IV'),
        (PIATY, 'V'),
        (SZOSTY, 'VI'),
        (SIODMY, 'VII'),
    )
    SEM_NAMES = (
        (PIERWSZY, 'pierwszy'),
        (DRUGI, 'drugi'),
        (TRZECI, 'trzeci'),
        (CZWARTY, 'czwarty'),
        (PIATY, 'piąty'),
        (SZOSTY, 'szósty'),
        (SIODMY, 'siódmy'),
    )
    STATIONARY = ((True, 'stacjonarne'), (False, 'niestacjonarne'))

    short_name = models.CharField(max_length=30)
    specialization = models.CharField(max_length=50)
    stationary = models.BooleanField(choices=STATIONARY, default=True)
    grade = models.CharField(max_length=1, choices=GRADES, default=PIERWSZY)
    year_of_study = models.CharField(max_length=1, choices=GRADES, default=PIERWSZY)
    sem_nr = models.CharField(max_length=1, choices=SEM_NAMES, default=PIERWSZY)
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
    place = models.CharField(max_length=6)
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
    BRAK_ZAJEC = 'N/A'
    PRESENCE_CHOICES = (
        (OBECNY, 'obecny'),
        (NIEOBECNY, 'nieobecny'),
        (SPOZNIONY, 'spóźniony'),
        (USPRAWIEDLIWIONY, 'usprawiedliwiony'),
        (BRAK_ZAJEC, 'zajęcia odwołane'),
    )
    presence_type = models.CharField(max_length=3, choices=PRESENCE_CHOICES)
    student = models.ForeignKey(Student)
    classesdate = models.ForeignKey(ClassesDate)


class Topic(models.Model):
    topic = models.TextField()
    classesdate = models.OneToOneField(ClassesDate, primary_key=True)


class Comment(models.Model):
    comment = models.TextField()
    classesdate = models.OneToOneField(ClassesDate, primary_key=True)


class Note(models.Model):
    text = models.TextField()
    student = models.ForeignKey(Student)
    classesdate = models.ForeignKey(ClassesDate)

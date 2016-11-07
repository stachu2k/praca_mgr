from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Semester, Group, Classes, ClassesDate, Student
from .forms import AddGroupForm
from .functions import create_group_from_files
import datetime

# Create your views here.


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'app/home.html', context)


@login_required(login_url='/login/')
def register(request):
    c = ClassesDate.objects.filter(date__gte=datetime.date(2016, 2, 24), date__lte=datetime.date(2016, 2, 28))
    context = {
        'c': c,
        'title': 'Dziennik zajęć',
    }
    return render(request, 'app/register/register.html', context)


@login_required(login_url='/login/')
def browse_group(request):
    try:
        semester = Semester.objects.get(active=True)
        classes = Classes.objects.filter(group=Group.objects.filter(semester=semester)).select_related('group')
    except Semester.DoesNotExist:
        semester = None
        classes = None
    context = {
        'semester': semester,
        'classes': classes,
        'title': 'Przeglądaj grupy',
    }
    return render(request, 'app/browse_group/browse_group.html', context)


@login_required(login_url='/login/')
def browse_group_show(request, group_id):
    group = Group.objects.filter(pk=group_id)
    classes = Classes.objects.get(group=group)
    classes_dates = classes.classesdate_set.all()
    students = Student.objects.filter(group=group).order_by('surname')
    context = {
        'classes': classes,
        'classes_dates': classes_dates,
        'students': students,
        'title': 'Szczegóły grupy',
    }
    return render(request, 'app/browse_group/browse_group_show.html', context)


@login_required(login_url='/login/')
def manage_semesters(request):
    semesters = Semester.objects.all().values()
    for semester in semesters:
        semester['groups'] = Group.objects.filter(semester_id=semester['id']).count()
    context = {
        'semesters': semesters,
        'title': 'Zarządzaj semestrami',
    }
    return render(request, 'app/manage_semesters/manage_semesters.html', context)


@login_required(login_url='/login/')
@transaction.atomic
def add_group(request):
    if request.method == 'POST':
        add_group_form = AddGroupForm(request.POST, request.FILES)
        if add_group_form.is_valid():
            result_msg = create_group_from_files(request.FILES['upload_grp'], request.FILES['upload_sem'])
            context = {
                'result_msg': result_msg,
                'title': 'Dodaj grupę',
            }
            return render(request, 'app/add_group/result.html', context)
    else:
        add_group_form = AddGroupForm()
    context = {
        'add_group_form': add_group_form,
        'title': 'Dodaj grupę',
    }
    return render(request, 'app/add_group/add_group.html', context)
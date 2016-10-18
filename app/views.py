from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Semester, Group
from .forms import AddGroupForm
from .functions import create_group_from_files

# Create your views here.


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'app/home.html', context)


@login_required(login_url='/login/')
def browse_group(request):
    context = {
        'title': 'Przeglądaj grupy',
    }
    return render(request, 'app/browse_group/browse_group.html', context)


@login_required(login_url='/login/')
def manage_semesters(request):
    semesters = Semester.objects.all().values()
    for semester in semesters:
        semester['groups'] = Group.objects.filter(semester_id=semester['id']).count()
    context = {
        'semesters': semesters,
        'title': 'Wybór semestru',
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
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import AddGroupForm
from .functions import create_group_from_files

# Create your views here.


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'app/home.html', context)


@transaction.atomic
def add_group(request):
    if request.method == 'POST':
        add_group_form = AddGroupForm(request.POST, request.FILES)
        if add_group_form.is_valid():
            message = create_group_from_files(request.FILES['upload_grp'], request.FILES['upload_sem'])
            context = {
                'message': message,
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
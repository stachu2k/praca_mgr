from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import AddGroupForm

# Create your views here.


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'app/home.html', context)


def add_group(request):
    upload_form = AddGroupForm()
    context = {
        'upload_form': upload_form,
        'title': 'Dodaj grupę',
    }
    return render(request, 'app/add_group.html', context)
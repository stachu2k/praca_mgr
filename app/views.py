from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'Home',
    }
    return render(request, 'app/home.html', context)
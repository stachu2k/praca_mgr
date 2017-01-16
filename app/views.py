from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Semester, Group, Classes, ClassesDate, Student, Topic, Comment
from .forms import AddGroupForm, ImportTopicsForm
from .functions import create_group_from_files, import_topics
import datetime
import json


# Create your views here.


@login_required(login_url='/login/')
def home(request):
    context = {
        'title': 'e-Dziennik Mobile',
    }
    return render(request, 'app/home/index.html', context)


@login_required(login_url='/login/')
def register(request):
    try:
        semester = Semester.objects.get(active=True)
    except Semester.DoesNotExist:
        context = {
            'title': 'Dziennik zajęć',
        }
        return render(request, 'app/shared/noseminfo.html', context)
    c = ClassesDate.objects.filter(date__gte=datetime.date(2016, 2, 24), date__lte=datetime.date(2016, 2, 28))
    context = {
        'semester': semester,
        'c': c,
        'title': 'Dziennik zajęć',
    }
    return render(request, 'app/register/index.html', context)


def ajax_get_classes(request):
    if request.is_ajax():
        date = request.GET.get('date', '')
        c = ClassesDate.objects.filter(date=datetime.datetime.strptime(date, "%d.%m.%Y")).order_by('classes__start_time')
        result = []
        for item in c:
            item_json = {
                'id': item.classes_id,
                'short_name': item.classes.group.short_name,
                'subject': item.classes.subject,
                'classes_type': item.classes.classes_type,
                'start_time': item.classes.start_time.strftime("%H:%M"),
                'end_time': item.classes.end_time.strftime("%H:%M"),
                'place': item.classes.place
            }
            result.append(item_json)
        data = json.dumps(result)
    else:
        raise Http404()

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required(login_url='/login/')
def groups(request):
    try:
        semester = Semester.objects.get(active=True)
    except Semester.DoesNotExist:
        context = {
            'title': 'Przeglądaj grupy',
        }
        return render(request, 'app/shared/noseminfo.html', context)
    classes_stationary = Classes.objects.filter(
        group__in=Group.objects.filter(
            semester=semester, stationary=True)).order_by('group__short_name').select_related('group')
    classes_notstationary = Classes.objects.filter(
        group__in=Group.objects.filter(
            semester=semester, stationary=False)).order_by('group__short_name').select_related('group')
    context = {
        'semester': semester,
        'classes_stationary': classes_stationary,
        'classes_notstationary': classes_notstationary,
        'title': 'Przeglądaj grupy',
    }
    return render(request, 'app/groups/index.html', context)


@login_required(login_url='/login/')
def groups_details(request, group_id):
    try:
        semester = Semester.objects.get(active=True)
    except Semester.DoesNotExist:
        context = {
            'title': 'Szczegóły grupy',
        }
        return render(request, 'app/shared/noseminfo.html', context)
    group = Group.objects.filter(pk=group_id)
    classes = Classes.objects.get(group=group)
    classes_dates = classes.classesdate_set.all()
    students = Student.objects.filter(group=group).order_by('surname')
    context = {
        'semester': semester,
        'classes': classes,
        'classes_dates': classes_dates,
        'students': students,
        'title': 'Szczegóły grupy',
    }
    return render(request, 'app/groups/details.html', context)


@login_required(login_url='/login/')
@transaction.atomic
def groups_add(request):
    if request.method == 'POST':
        add_group_form = AddGroupForm(request.POST, request.FILES)
        if add_group_form.is_valid():
            result_msg = create_group_from_files(request.FILES['upload_grp'], request.FILES['upload_sem'])
            context = {
                'result_msg': result_msg,
                'title': 'Dodaj grupę',
            }
            return render(request, 'app/groups/add.results.html', context)
    else:
        add_group_form = AddGroupForm()
    context = {
        'add_group_form': add_group_form,
        'title': 'Dodaj grupę',
    }
    return render(request, 'app/groups/add.html', context)


@login_required(login_url='/login/')
def groups_classes(request, group_id):
    try:
        semester = Semester.objects.get(active=True)
    except Semester.DoesNotExist:
        context = {
            'title': 'Prowadzenie zajęć',
        }
        return render(request, 'app/shared/noseminfo.html', context)

    result = None
    import_topics_form = ImportTopicsForm(request.POST or None, request.FILES or None)
    if import_topics_form.is_valid():
        result = import_topics(group_id, request.FILES['upload_topic'])

    group = Group.objects.filter(pk=group_id)
    classes = Classes.objects.get(group=group)
    classes_dates = classes.classesdate_set.all()
    students = Student.objects.filter(group=group).order_by('surname')
    context = {
        'semester': semester,
        'classes': classes,
        'classes_dates': classes_dates,
        'students': students,
        'import_topics_form': import_topics_form,
        'result': result,
        'title': 'Prowadzenie zajęć',
    }
    return render(request, 'app/groups/classes.html', context)


def ajax_edit_topic(request, classesdate_id):
    if request.is_ajax():
        new_topic = request.POST.get('value', '')
        topic, created = Topic.objects.update_or_create(
            pk=classesdate_id,
            defaults={'topic': new_topic}
        )

        msg = 'success'

    else:
        raise Http404()

    mimetype = 'text/html'
    return HttpResponse(msg, mimetype)


def ajax_edit_comment(request, classesdate_id):
    if request.is_ajax():
        new_comment = request.POST.get('value', '')
        comment, created = Comment.objects.update_or_create(
            pk=classesdate_id,
            defaults={'comment': new_comment}
        )

        msg = 'success'

    else:
        raise Http404()

    mimetype = 'text/html'
    return HttpResponse(msg, mimetype)


def ajax_get_topictable(request):
    if request.is_ajax():
        classes_id = request.GET.get('classes_id', '')
        classesdates = ClassesDate.objects.filter(classes_id=classes_id)
        result = []
        for item in classesdates:
            date = ""
            if item.date.day < 10:
                date += "0"
            date += str(item.date.day) + "."
            if item.date.month < 10:
                date += "0"
            date += str(item.date.month)

            item_json = {
                'id': item.id,
                'date': date,
                'nr_of_week': item.nr_of_week
            }

            try:
                topic = Topic.objects.get(classesdate=item)
                item_json['topic'] = topic.topic
            except Topic.DoesNotExist:
                item_json['topic'] = ''

            try:
                comment = Comment.objects.get(classesdate=item)
                item_json['comment'] = comment.comment
            except Comment.DoesNotExist:
                item_json['comment'] = ''

            result.append(item_json)
        data = json.dumps(result)
    else:
        raise Http404()

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required(login_url='/login/')
def semesters(request):
    semesters = Semester.objects.all().values()
    for semester in semesters:
        semester['groups'] = Group.objects.filter(semester_id=semester['id']).count()
    context = {
        'semesters': semesters,
        'title': 'Zarządzaj semestrami',
    }
    return render(request, 'app/semesters/index.html', context)
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Semester, Group, Classes, ClassesDate, Student, Topic, Comment, Presence, Note
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
    context = {
        'semester': semester,
        'title': 'Dziennik zajęć',
    }
    return render(request, 'app/register/index.html', context)


def ajax_get_classes(request):
    if request.is_ajax():
        date = request.GET.get('date', '')
        c = ClassesDate.objects.filter(date=datetime.datetime.strptime(date, "%d.%m.%Y"), classes__group__semester=Semester.objects.get(active=True)).order_by('classes__start_time')
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
    group = Group.objects.get(pk=group_id)
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
            result = create_group_from_files(request.FILES['upload_grp'], request.FILES['upload_sem'])
            context = {
                'result': result,
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
    presences = Presence.objects.filter(classesdate__classes__group_id=group_id)
    notes = Note.objects.filter(classesdate__classes__group_id=group_id)
    context = {
        'semester': semester,
        'classes': classes,
        'classes_dates': classes_dates,
        'students': students,
        'presences': presences,
        'notes': notes,
        'import_topics_form': import_topics_form,
        'result': result,
        'title': 'Prowadzenie zajęć',
    }
    return render(request, 'app/groups/classes.html', context)


def ajax_edit_topic(request, classesdate_id):
    if request.is_ajax():
        new_topic = request.POST.get('value', '')
        Topic.objects.update_or_create(
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
        Comment.objects.update_or_create(
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


def ajax_check_presence(request, classesdate_id):
    if request.is_ajax():
        no_classes = request.POST.get('no_classes', '')
        checked_students = request.POST.getlist('students')
        all_students = Student.objects.filter(group__classes__classesdate__id=classesdate_id)
        if no_classes == 'no_classes':
            for student in all_students:
                presence, created = Presence.objects.update_or_create(
                    student=student,
                    classesdate=ClassesDate.objects.get(pk=classesdate_id),
                    defaults={'presence_type': 'N/A'}
                )
        else:
            for student in all_students:
                if str(student.id) in checked_students:
                    presence, created = Presence.objects.update_or_create(
                        student=student,
                        classesdate=ClassesDate.objects.get(pk=classesdate_id),
                        defaults={'presence_type': 'O'}
                    )
                else:
                    presence, created = Presence.objects.update_or_create(
                        student=student,
                        classesdate=ClassesDate.objects.get(pk=classesdate_id),
                        defaults={'presence_type': 'N'}
                    )
        msg = 'success'
    else:
        raise Http404()

    mimetype = 'text/html'
    return HttpResponse(msg, mimetype)


def ajax_edit_presence(request, classesdate_id, student_id):
    if request.is_ajax():
        presence_type = request.POST.get('presence', '')
        new_note = request.POST.get('note', '')
        if new_note == '':
            try:
                Note.objects.get(classesdate__id=classesdate_id, student__id=student_id).delete()
            except Note.DoesNotExist:
                pass
        else:
            Note.objects.update_or_create(
                student=Student.objects.get(pk=student_id),
                classesdate=ClassesDate.objects.get(pk=classesdate_id),
                defaults={'text': new_note}
            )
        if presence_type == 'o':
            presence, created = Presence.objects.update_or_create(
                student=Student.objects.get(pk=student_id),
                classesdate=ClassesDate.objects.get(pk=classesdate_id),
                defaults={'presence_type': 'O'}
            )
        elif presence_type == 'n':
            presence, created = Presence.objects.update_or_create(
                student=Student.objects.get(pk=student_id),
                classesdate=ClassesDate.objects.get(pk=classesdate_id),
                defaults={'presence_type': 'N'}
            )
        elif presence_type == 's':
            presence, created = Presence.objects.update_or_create(
                student=Student.objects.get(pk=student_id),
                classesdate=ClassesDate.objects.get(pk=classesdate_id),
                defaults={'presence_type': 'S'}
            )
        elif presence_type == 'u':
            presence, created = Presence.objects.update_or_create(
                student=Student.objects.get(pk=student_id),
                classesdate=ClassesDate.objects.get(pk=classesdate_id),
                defaults={'presence_type': 'U'}
            )
        msg = 'success'
    else:
        raise Http404()

    mimetype = 'text/html'
    return HttpResponse(msg, mimetype)


def ajax_get_presencetable(request):
    if request.is_ajax():
        classes_id = request.GET.get('classes_id', '')
        classesdates = ClassesDate.objects.filter(classes__group_id=classes_id)
        students = Student.objects.filter(group_id=classes_id)
        presences = Presence.objects.filter(classesdate__classes_id=classes_id)
        notes = Note.objects.filter(classesdate__classes_id=classes_id)

        html_code = ""
        for student in students:
            html_code += '<tr><td style="white-space:nowrap">' + student.surname + ' ' + student.name + '</td>'
            for date in classesdates:
                html_code += '<td onclick="editPresence(this, ' + str(student.id) + ',' + str(date.id) + ')">'
                for presence in presences:
                    if presence.student == student and presence.classesdate == date:
                        if not presence.presence_type == 'N/A':
                            html_code += '<div class="' + presence.presence_type + '">'
                            for note in notes:
                                if note.student == student and note.classesdate == date:
                                    html_code += '<img style="float:left" src="/static/mobile/images/icons-png/info-black.png">'
                                    html_code += '<textarea style="display:none">' + note.text + '</textarea>'
                            html_code += presence.presence_type + '</div>'
                        else:
                            html_code += presence.presence_type
                html_code += '</td>'
            html_code += '</tr>'

    else:
        raise Http404()

    mimetype = 'text/html'
    return HttpResponse(html_code, mimetype)


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


@login_required(login_url='/login/')
def semesters_details(request, semester_id):
    semester = get_object_or_404(Semester, pk=semester_id)
    groups_count = semester.group_set.count()
    context = {
        'semester': semester,
        'group_count': groups_count,
        'title': 'Szczegóły semestru',
    }
    return render(request, 'app/semesters/details.html', context)


@login_required(login_url='/login/')
def semesters_activate(request, semester_id):
    semester = get_object_or_404(Semester, pk=semester_id)
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
    context = {
        'semester': semester,
        'title': 'Szczegóły semestru',
    }
    return render(request, 'app/semesters/details.html', context)


@login_required(login_url='/login/')
def semesters_delete(request, semester_id):
    context = {
        'semester_id': semester_id,
    }
    return render(request, 'app/semesters/delete.confirmation.html', context)


@login_required(login_url='/login/')
def semesters_delete_confirmation(request, semester_id, choice):
    if choice == "yes":
        # get_object_or_404(Semester, pk=semester_id).delete()
        return render(request, 'app/semesters/delete.result.html')
    elif choice == "no":
        return redirect('semesters')

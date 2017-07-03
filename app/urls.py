from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^ajax/get_classes/$', views.ajax_get_classes, name='ajax_get_classes'),

    url(r'^groups/$', views.groups, name='groups'),
    url(r'^groups/(?P<group_id>\d+)/details/$', views.groups_details, name='groups_details'),
    url(r'^groups/(?P<group_id>\d+)/classes/$', views.groups_classes, name='groups_classes'),
    url(r'^groups/add/$', views.groups_add, name='groups_add'),
    url(r'^ajax/edit_topic/(?P<classesdate_id>\d+)/$', views.ajax_edit_topic, name='ajax_edit_topic'),
    url(r'^ajax/edit_comment/(?P<classesdate_id>\d+)/$', views.ajax_edit_comment, name='ajax_edit_comment'),
    url(r'^ajax/get_topictable/$', views.ajax_get_topictable, name='ajax_get_topictable'),
    url(r'^ajax/check_presence/(?P<classesdate_id>\d+)/$', views.ajax_check_presence, name='ajax_check_presence'),
    url(r'^ajax/edit_presence/date(?P<classesdate_id>\d+)/student(?P<student_id>\d+)/$', views.ajax_edit_presence, name='ajax_edit_presence'),
    url(r'^ajax/get_presencetable/$', views.ajax_get_presencetable, name='ajax_get_presencetable'),

    url(r'^semesters/$', views.semesters, name='semesters'),
    url(r'^semesters/details/(?P<semester_id>\d+)/$', views.semesters_details, name='semesters_details'),
    url(r'^semesters/activate/(?P<semester_id>\d+)/$', views.semesters_activate, name='semesters_activate'),
    url(r'^semesters/delete/(?P<semester_id>\d+)/$', views.semesters_delete, name='semesters_delete'),
    url(r'^semesters/delete/(?P<semester_id>\d+)/confirmation/(?P<choice>yes|no)/$',
        views.semesters_delete_confirmation, name='semesters_delete_confirmation'),

    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]

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


    url(r'^semesters/$', views.semesters, name='semesters'),

    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]
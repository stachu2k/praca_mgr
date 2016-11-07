from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^browse_group/$', views.browse_group, name='browse_group'),
    url(r'^browse_group/show/(?P<group_id>\d+)$', views.browse_group_show, name='browse_group_show'),
    url(r'^manage_semesters/$', views.manage_semesters, name='manage_semesters'),
    url(r'^add_group/$', views.add_group, name='add_group'),
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]
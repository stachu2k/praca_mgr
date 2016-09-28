from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add_group/$', views.add_group, name='add_group'),
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]
from django.conf.urls import url
from . import views

app_name = 'shifts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/filter_user_shifts/$', views.filter_user_shifts, name='filter_user_shifts'),
    url(r'^ajax/filter_open_shifts/$', views.filter_open_shifts, name='filter_open_shifts'),
    url(r'^ajax/filter_near_shifts/$', views.filter_near_shifts, name='filter_near_shifts'),
]

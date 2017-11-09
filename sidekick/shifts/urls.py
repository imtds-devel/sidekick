from django.conf.urls import url
from . import views

app_name = 'shifts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/filter_shifts/$', views.filter_shifts, name='filter_shifts'),
]

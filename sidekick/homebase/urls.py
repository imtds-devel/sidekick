from django.urls import path
from . import views

app_name = 'homebase'
urlpatterns = [
    path('', views.index, name='index'),
    path('test', views.roster_test),
]

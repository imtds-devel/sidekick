from django.urls import path
from . import views

app_name = 'printinfo'
urlpatterns = [
    path('', views.index, name='index'),
]

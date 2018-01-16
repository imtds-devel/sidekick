from django.conf.urls import url
from . import views

app_name = 'printinfo'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]

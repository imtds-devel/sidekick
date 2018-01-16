from django.conf.urls import url
from . import views

app_name = 'passwords'
urlpatterns = [
    url(r'^$', views.index, name='index'),
]

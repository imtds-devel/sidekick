from django.urls import path
from . import views

app_name = 'homebase'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/newannounce', views.new_announcement),
    path('ajax/newevent', views.new_event),
]

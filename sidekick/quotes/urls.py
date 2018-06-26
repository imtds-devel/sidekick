from django.urls import path
from . import views
from sidekick.views import new_task, complete_task

app_name = 'quotes'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task)
]

from django.urls import path
from . import views
from sidekick.views import new_task, complete_task

app_name = 'printinfo'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/printreportsget/', views.get_reports),
    path('ajax/printreportupdate/', views.update_report),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task)
]

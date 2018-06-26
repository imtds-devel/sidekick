from django.urls import path
from . import views
from sidekick.views import new_task, complete_task

app_name = 'roster'
urlpatterns = [
    path('', views.index, name='index'),
    path('overview', views.overview, name='overview'),
    path('ajax/awardpost/', views.post_award),
    path('ajax/awardsget/', views.get_trophies),
    path('ajax/commentpost/', views.post_comment),
    path('ajax/commentsget/', views.get_comments),
    path('ajax/commentdelete/', views.delete_comment),
    path('ajax/disciplinepost/', views.post_discipline),
    path('ajax/employeeupdate/', views.update_bio),
    path('ajax/employeedelete/', views.delete_employee),
    path('ajax/proficienciesupdate/', views.update_prof),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task)
]

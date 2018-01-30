from django.urls import path
from . import views

app_name = 'roster'
urlpatterns = [
    path(r'^$', views.index, name='index'),
    path(r'^ajax/awardpost/', views.post_award),
    path(r'^ajax/awardsget/', views.get_trophies),
    path(r'^ajax/commentpost/', views.post_comment),
    path(r'^ajax/commentsget/', views.get_comments),
    path(r'^ajax/commentdelete/', views.delete_comment),
    path(r'^ajax/disciplinepost/', views.post_discipline),
    path(r'^ajax/employeeupdate/', views.update_bio),
    path(r'^ajax/employeedelete/', views.delete_employee),
    path(r'^ajax/proficienciesupdate/', views.update_prof)
]

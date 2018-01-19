from django.conf.urls import url
from . import views

app_name = 'roster'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/awardpost/', views.post_award),
    url(r'^ajax/awardsget/', views.get_trophies),
    url(r'^ajax/commentpost/', views.post_comment),
    url(r'^ajax/commentsget/', views.get_comments),
    url(r'^ajax/commentdelete/', views.delete_comment),
    url(r'^ajax/disciplinepost/', views.post_discipline),
    url(r'^ajax/employeeupdate/', views.update_bio),
    url(r'^ajax/employeedelete/', views.delete_employee),
    url(r'^ajax/proficienciesupdate/', views.update_prof)
]

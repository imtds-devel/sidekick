from django.conf.urls import url
from . import views

app_name = 'roster'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/postaward/', views.post_award),
    url(r'^ajax/postcomment/', views.post_comment),
    url(r'^ajax/postdiscipline/', views.post_discipline),
    url(r'^ajax/getcomments/', views.get_comments),
    url(r'^ajax/gettrophies/', views.get_trophies),
    url(r'^ajax/updatebio/', views.update_bio),
    url(r'^ajax/updateprof/', views.update_prof),
    url(r'^ajax/deleteemployee/', views.delete_employee),
    url(r'^ajax/deletecomment/', views.delete_comment)
]

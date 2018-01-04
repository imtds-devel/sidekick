from django.conf.urls import url
from . import views

app_name = 'roster'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/postaward/', views.post_award),
    url(r'^ajax/postcomment/', views.post_comment),
    url(r'^ajax/postdiscipline/', views.post_discipline),
    url(r'^ajax/getcomments/', views.get_comments)
]

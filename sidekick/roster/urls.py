from django.urls import path
from . import views

app_name = 'roster'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/postaward/', views.post_award),
    path('ajax/postcomment/', views.post_comment),
    path('ajax/postdiscipline/', views.post_discipline),
    path('ajax/getcomments/', views.get_comments),
    path('ajax/gettrophies/', views.get_trophies)
]

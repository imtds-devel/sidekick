from django.conf.urls import url
from . import views

app_name = 'roster'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/postcomment/', views.post_comment),
]

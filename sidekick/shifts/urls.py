from django.conf.urls import url
from . import views

app_name = 'shifts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/filter_user_shifts/$', views.filter_user_shifts, name='filter_user_shifts'),
    url(r'^ajax/filter_open_shifts/$', views.filter_open_shifts, name='filter_open_shifts'),
    url(r'^ajax/filter_near_shifts/$', views.filter_near_shifts, name='filter_near_shifts'),
<<<<<<< HEAD
=======
    url(r'^ajax/post_cover/$', views.post_cover, name='post_cover'),
    url(r'^ajax/take_cover/$', views.take_cover, name='take_cover'),
>>>>>>> develop
    # url(r'test/', views.post_cover),
]

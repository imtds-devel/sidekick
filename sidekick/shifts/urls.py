from django.urls import path
from . import views

app_name = 'shifts'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/filter_user_shifts/', views.filter_user_shifts, name='filter_user_shifts'),
    path('ajax/filter_open_shifts/', views.filter_open_shifts, name='filter_open_shifts'),
    path('ajax/filter_near_shifts/', views.filter_near_shifts, name='filter_near_shifts'),
    path('ajax/post_cover/', views.post_cover, name='post_cover'),
    path('ajax/take_cover/', views.take_cover, name='take_cover'),
    # path('test/', views.post_cover),
]


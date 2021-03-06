from django.urls import path
from . import views
from sidekick.views import new_task, complete_task, update_note, load_note, clear_note

app_name = 'shifts'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/filter_user_shifts/', views.filter_user_shifts, name='filter_user_shifts'),
    path('ajax/filter_open_shifts/', views.filter_open_shifts, name='filter_open_shifts'),
    path('ajax/filter_all_shifts/', views.filter_all_shifts, name='filter_all_shifts'),
    path('ajax/filter_near_shifts/', views.filter_near_shifts, name='filter_near_shifts'),
    path('ajax/post_cover/', views.push_cover, name='post_cover'),
    path('ajax/take_cover/', views.push_cover, name='take_cover'),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task),
    path('ajax/updatenote', update_note),
    path('ajax/loadnote', load_note),
    path('ajax/clearnote', clear_note)
    # path('test/', views.post_cover),
]


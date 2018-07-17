from django.urls import path
from . import views
from sidekick.views import new_task, complete_task, update_note, load_note, clear_note

app_name = 'homebase'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/checkinpost/', views.post_checkin),
    path('ajax/newannounce', views.new_announcement),
    path('ajax/newevent', views.new_event),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task),
    path('ajax/updatenote', update_note),
    path('ajax/loadnote', load_note),
    path('ajax/clearnote', clear_note)
]

from django.urls import path
from . import views
from sidekick.views import new_task, complete_task, update_note, load_note, clear_note

app_name = 'passwords'
urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/newtask', new_task),
    path('ajax/completetask', complete_task),
    path('ajax/updatenote', update_note),
    path('ajax/loadnote', load_note),
    path('ajax/clearnote', clear_note)

]

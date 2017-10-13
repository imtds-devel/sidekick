# -*- coding: utf-8 -*-
from sidekick import views
from django.http import HttpResponseRedirect
from homebase.models import Announcements, Events
from .forms import AnnouncmentForm, EventForm

# Create your views here.
def index(request):
    # If this is a form submission
    if request.method == "POST":
        #need to validate which form is being submitted (give the input a name attribute)
        import copy
        data = copy.copy(request.POST)

        if 'e-form' in request.POST:
            # In case we're not in production
            # Remove this line before production!
            request = views.get_current_user(request)
            data['announcer'] = request.user
            form = EventForm(data)
            print(form.fields)
        if 'a-form' in request.POST:
            # In case we're not in production
            # Remove this line before production!
            request = views.get_current_user(request)
            data['announcer'] = request.user
            form = AnnouncmentForm(data)
            print(form)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return views.load_page(request, 'homebase/index.html', prep_context())

def prep_context():
    announcement_list = Announcements.objects.all().order_by('posted')
    event_list = Events.objects.all().order_by('event_start')

    ordered_list = order(announcement_list, event_list)
    a_form = AnnouncmentForm()
    e_form = EventForm()
    return {
        'ordered_list': ordered_list,
        'a_form': a_form,
        'e_form': e_form
    }

def order(a_list, e_list):
    ordered = list(a_list) + list(e_list)
    #Combines the two lists, then sorts using lambda function with the announcement posted
    #attribute and event event_start attribute
    ordered_list = sorted(ordered, key=lambda x: x.posted if hasattr(x, 'posted') else x.event_start, reverse=True)
    return ordered_list[:8]

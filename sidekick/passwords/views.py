# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views
from sidekick import access

# Create your views here.
def index(request):
    context = prep_context(request)
    return views.load_page(request, 'passwords/index.html', context)

def prep_context(request):
    context = {}
    context.lab_access = access.get_access(request.user, "passwords_lab")
    context.support_access = access.get_access(request.user, "passwords_support")
    context.mod_access = access.get_access(request.user, "passwords_manager")

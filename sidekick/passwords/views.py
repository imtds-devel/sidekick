# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views
from sidekick import access
from .models import PassPermission
from .models import Passwords


def index(request):
    context = {}

    # First, get a list of areas that the user is allowed to access
    access_areas = []
    if access.get_access(str(request.user), "passwords_lab"):
        access_areas.append('lab')  # Notice that these correspond to the names from the passwords models file
    if access.get_access(str(request.user), "passwords_support"):
        access_areas.append('spt')
    if access.get_access(str(request.user), "passwords_manager"):
        access_areas.append('mgr')
    if access.get_access(str(request.user), "passwords_all"):
        access_areas.append('all')

    # Next, get a list of passwords based off of that list

    passwords = []
    for area in access_areas:  # for each access area
        # get all passwords the current area is authorized to access
        accesses = PassPermission.objects.filter(permission=area).order_by('pass_id')
        for permitted_pass in accesses:  # Copy passwords for this area to our list of passwords
            if permitted_pass.pass_id not in passwords:
                passwords.append(permitted_pass.pass_id)

    context['passwords'] = passwords

<<<<<<< HEAD
    return views.load_page(request, 'passwords/index.html', context)
=======
    return views.load_page(request, 'passwords/index.html', context)
>>>>>>> d41c5d16ef058133bddc86709d513bf06ee0d2ca

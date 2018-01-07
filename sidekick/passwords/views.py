# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sidekick import views
from sidekick import access
from .models import PassPermission
from .models import Passwords


def index(request):
    context = prep_context(request)

    # First, get a list of areas that the user is allowed to access
    access_areas = []
    if context['lab_access']:
        access_areas.append('lab')  # Notice that these correspond to the names from the passwords models file
    if context['support_access']:
        access_areas.append('spt')
    if context['mod_access']:
        access_areas.append('mgr')
    if context['all_access']:
        access_areas.append('all')

    # Next, get a list of passwords based off of that list
    
    passwords = []
    for area in access_areas:  # for each access area
        # get all passwords the current area is authorized to access
        accesses = PassPermission.objects.filter(permission=area).order_by('pass_id')
        for pass_perm in accesses:  # Copy passwords for this area to our list of passwords
            if pass_perm.pass_id not in passwords:
                passwords.append(pass_perm.pass_id)

    context['passwords'] = passwords

    return views.load_page(request, 'passwords/index.html', context)


def prep_context(request):
    return {
                'lab_access': access.get_access(request.user, "passwords_lab"),
                'support_access': access.get_access(request.user, "passwords_support"),
                'mod_access': access.get_access(request.user, "passwords_manager"),
                'all_access': access.get_access(request.user, "passwords_all")
            }

# -*- coding: utf-8 -*-
from sidekick import views

def index(request):
    employee_list = Employee.objects.all()
    context = {'employee_list':employee_list}
    return render(request, 'homebase/index.html', context)

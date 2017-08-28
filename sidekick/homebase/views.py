# -*- coding: utf-8 -*-
from sidekick import views

<<<<<<< HEAD
#from .models import Employee

def index(request):
    context = {}
    return views.load_page(request, 'homebase/index.html', context)
=======
from .models import Employee

def index(request):
    employee_list = Employee.objects.all()
    context = {'employee_list':employee_list}
    return render(request, 'homebase/index.html', context)
>>>>>>> 23b1ee5234f66710cfee5accef6369ac46f8cf12

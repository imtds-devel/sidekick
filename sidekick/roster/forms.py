from django import forms
from homebase.models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model= Employee
        fields=('netid', 'fname', 'lname', 'phone', 'apuid', 'codename', 'position', 'position_desc',
                'standing', 'birthday', 'aboutme', 'developer')

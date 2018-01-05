from django import forms
from homebase.models import Employees


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model= Employees
        fields=('netid', 'fname', 'lname', 'phone', 'apuid', 'codename', 'position', 'position_desc',
                'standing', 'birthday', 'aboutme')

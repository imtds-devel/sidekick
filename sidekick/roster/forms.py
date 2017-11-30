from django import forms
from homebase.models import Employees
from .models import Discipline

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


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['poster'].widget = forms.HiddenInput()
        self.fields['about'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['val'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['violation'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['description'].attrs={'row': 'length:5'},
    class Meta:
        model = Discipline
        fields = ('poster', 'about', 'description', 'val', 'violation')

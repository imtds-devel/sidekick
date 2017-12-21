from django import forms
from homebase.models import Employees
from .models import Discipline
from .models import Trophies


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Employees
        fields = ('netid', 'fname', 'lname', 'phone', 'apuid', 'codename', 'position', 'position_desc',
                  'standing', 'birthday', 'aboutme')


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Discipline
        fields = ('subject', 'poster', 'about', 'description')


class StarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StarForm, self).__init__(*args, **kwargs)
        self.fields['giver'].widget = forms.HiddenInput()
        self.fields['recipient'].widget = forms.HiddenInput()
        self.fields['name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['reason'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['trophy_type'].widget.attrs.update({
            'class': 'form-control',
        })

    class Meta:
        model = Trophies
        fields = ('giver', 'recipient', 'trophy_type', 'reason', 'name')

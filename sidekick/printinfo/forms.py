from django import forms
from .models import StatusLog

class StatusLogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StatusLogForm, self).__init__(*args, **kwargs)
        self.fields['print_id'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['print_id'].widget = forms.HiddenInput()
        self.fields['date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['print_stat'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['desc'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['date'].widget.attrs['readonly'] = True
    class Meta:
        model = StatusLog
        fields = ('print_id', 'date', 'print_stat', 'desc') #add field netid

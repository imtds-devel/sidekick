from django import forms
from .models import StatusLog

class StatusLogForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StatusLogForm, self).__init__(*args, **kwargs)
        self.fields['printer'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['printer'].widget = forms.HiddenInput()
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
        self.fields['netid'].widget = forms.HiddenInput()
    class Meta:
        model = StatusLog
        fields = ('printer', 'date', 'print_stat', 'desc', 'netid')

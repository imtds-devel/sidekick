from django.forms import forms
from .models import Library

class PrintInfo(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrintInfo, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class Meta:
    model = Library
    fields = ('libid', 'printtype', 'printid', 'iplink', 'status', 'report')

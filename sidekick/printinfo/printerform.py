from django.forms import forms
from .models import StatusLog

class PrinterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PrinterForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class Meta:
    forms= StatusLog,
    fields= ('print_id', 'print_stat', 'date', 'desc')
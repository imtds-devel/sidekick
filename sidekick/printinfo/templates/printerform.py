from django.db import forms
import Printers

class PrinterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PrinterForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model= Printers
        fields=('library', 'libnum' 'printid', 'iplink', 'status', 'description')


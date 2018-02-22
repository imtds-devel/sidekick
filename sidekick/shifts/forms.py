from django import forms
from .models import ShiftCovers

class ShiftCoverForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
    class Meta:
        model= ShiftCovers
        fields=('shift', 'poster', 'taker', 'type', 'sobstory', 'post_date')
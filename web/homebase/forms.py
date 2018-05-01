from django import forms
from homebase.models import Announcements, Events, StaffStatus


class DateInput(forms.DateInput):
    input_type = 'date'


class StatusForm(forms.ModelForm):
    def __index__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields['netid'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['status'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = StaffStatus
        fields = '__all__'

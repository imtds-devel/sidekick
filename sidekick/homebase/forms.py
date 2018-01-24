from django import forms
from homebase.models import Announcements, Events, StaffStatus


class DateInput(forms.DateInput):
    input_type = 'date'

class AnnouncmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnnouncmentForm, self).__init__(*args, **kwargs)

        self.fields['announcement'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['subject'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['sticky'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['announcer'].widget = forms.HiddenInput()

    class Meta:
        model = Announcements
        fields = ('announcer', 'announcement', 'subject', 'sticky')


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['event_start'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['event_end'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['location'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['announcer'].widget = forms.HiddenInput()

    class Meta:
        model = Events
        fields = ('announcer', 'title', 'description', 'event_start', 'event_end', 'location')
        widgets = {
            'event_start': DateInput(),
            'event_end': DateInput()
        }


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

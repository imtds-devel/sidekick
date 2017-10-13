from django import forms
from homebase.models import Announcements, Events

class DateInput(forms.DateInput):
    input_type = 'date'

class AnnouncmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnnouncmentForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Announcements
        fields=('announcement', 'subject', 'sticky')

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Events
        fields=('announcer', 'title', 'description', 'event_start', 'event_end', 'location')
        widgets = {
            'event_start': DateInput(),
            'event_end': DateInput()
        }

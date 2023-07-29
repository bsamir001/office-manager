from django import forms
from .models import Doctor,Appointment

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())

    class Meta:
        model = Appointment
        fields = ['doctor', 'start_date', 'end_date','start_time', 'end_time']

class DoctorDelayForm(forms.Form):
    delay_time = forms.IntegerField(label='Delay Time')
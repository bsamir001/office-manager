from django import forms
from .models import Doctor,Appointment
class DoctorDelayForm(forms.Form):
    delay_time = forms.IntegerField(label='Delay Time')
from django import forms
from account.models import patent
from turn.models import Appointment



class bime_form(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['start_date', 'end_date']

class bimepatent_form(forms.ModelForm):
    class Meta:
        model=patent
        fields=['typebime',]
class expance_form(forms.Form):
    start_date1=forms.DateField()
    end_data1=forms.DateField()
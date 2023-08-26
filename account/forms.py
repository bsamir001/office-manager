
from django import forms
from .models import User,patent


class UserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('phone_number',)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('phone_number', 'last_login')


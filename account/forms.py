
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

class User_RegisterForm(forms.ModelForm):
    class Meta:
        model =patent
        fields = ('codeID','firstname','lastname','age','typeSickness','typebime','infopatent','textSickness',)



class userregisterform(forms.Form):
    phone=forms.CharField(max_length=11)
class LoginForm(forms.Form):
    phone_number = forms.CharField()


class VerifycodeForm(forms.Form):
    code=forms.IntegerField()
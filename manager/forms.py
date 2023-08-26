from django import forms


class InfoForm(forms.Form):
    user_presence = forms.BooleanField(label="حضور در مطب", required=False)
    payment = forms.BooleanField(label='پرداخت', required=False)
    user_phone_number = forms.CharField(label='شماره تلفن', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    user_codeID = forms.CharField(label='کد ملی', widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    user_firstname = forms.CharField(label="نام", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    user_lastname = forms.CharField(label="نام خانوادگی", widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    start_time = forms.TimeField(label="زمان حضور در مطب", widget=forms.TimeInput(attrs={'readonly': 'readonly'}))
    user_filing = forms.CharField(label="تشکیل پرونده", required=False, widget=forms.TextInput(attrs={}))
    # user_print_bill = forms.CharField(label="برای چاپ قبض خود از این دکمه استفاده کنید",widget=forms.TextInput(attrs={'type': 'button', 'value': 'پرینت قبض'}))

"""
class ListForm (forms.Form):
    payment = forms.BooleanField(label='پرداخت', required=False)
    user_presence = forms.BooleanField(label="حضور در مطب", required=False)
"""
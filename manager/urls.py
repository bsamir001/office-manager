from django.urls import path
from .views import *

app_name = 'manager'

urlpatterns = [
    path('', ShowFormView.as_view(), name='show_form'),
    path('form/<str:phone_number>/', ShowInfoForm.as_view(), name='show_info'),
    ]

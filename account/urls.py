from django.urls import path
from .views import *
app_name='account'

urlpatterns=[
            path('send/', userregisterviews.as_view(), name='send'),
            path('send1/', userregisterverifycodeview.as_view(), name='verify_code'),
            path('register/', User_register.as_view(), name='register'),
            path('logout/', UserLogoutView.as_view(), name='logout'),
            path('deatel/', Deatel_register.as_view(), name='deatel'),

]



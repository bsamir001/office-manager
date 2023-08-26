from django.urls import path
from .views import *

app_name = 'account'

urlpatterns = [
    # path('send/', userregisterviews.as_view(), name='send'),
    # path('send1/', userregisterverifycodeview.as_view(), name='verify_code'),
    # path('register/', User_register.as_view(), name='register'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('deatel/', Deatel_register.as_view(), name='deatel'),

    path('api/v1/send/', UserRegisterViews.as_view(), name='send_api'),
    path('api/v1/send1/', UserRegisterVerifyCodeView.as_view(), name='verify_code_api'),
    path('api/v1/register/', UserCompleteInfoView.as_view(), name='register_api'),
    path('api/v1/logout/', UserLogoutView.as_view(), name='logout_api'),
    path('api/v1/detail/', DetailRegisterView.as_view(), name='detail_api'),
]


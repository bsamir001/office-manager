from django.urls import path
from .views import CreateAppointmentsView, DoctorDelayView, ReservedAppointmentsListView, PayView, VerifyView, \
    AllDaysAppointmentsView, DayAppointmentsView,UserToPatientView

app_name = 'turn'
urlpatterns = [
    # ...
    # path('create/', CreateAppointmentsView.as_view(), name='create_appointment'),
    # path('delay/', doctor_delay_view.as_view(), name='doctor_delay'),
    # path('reserved_list/',ReservedAppointments_listView.as_view(), name='reserved_list'),
    # path('pay/<int:appointment_id>/', pay_view.as_view(), name='pay'),
    # path('verify/', Verify_View.as_view(), name='verify'),
    # path('all_days/', AllDaysAppointmentsView.as_view(), name='all_days_appointments'),
    # path('all_days/<str:appointment_date>/', DayAppointmentsView.as_view(), name='day_appointments'),
    path('api/v1/create/', CreateAppointmentsView.as_view(), name='create_appointment_api'),
    path('api/v1/delay/', DoctorDelayView.as_view(), name='doctor_delay_api'),
    path('api/v1/reserved_list/', ReservedAppointmentsListView.as_view(), name='reserved_list_api'),
    path('api/v1/pay/<int:appointment_id>/', PayView.as_view(), name='pay_api'),
    path('api/v1/verify/', VerifyView.as_view(), name='verify_api'),
    path('api/v1/all_days/', AllDaysAppointmentsView.as_view(), name='all_days_appointments_api'),
    path('api/v1/all_days/<str:appointment_date>/', DayAppointmentsView.as_view(), name='day_appointments_api'),
    path('api/v1/getpatient/', UserToPatientView.as_view(), name='user_to_patient'),
]




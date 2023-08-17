from django.urls import path
from .views import CreateAppointmentsView,doctor_delay_view,ReservedAppointments_listView,pay_view,Verify_View,AllDaysAppointmentsView,DayAppointmentsView
app_name='turn'
urlpatterns = [
    # ...
    path('create/', CreateAppointmentsView.as_view(), name='create_appointment'),
    path('delay/', doctor_delay_view.as_view(), name='doctor_delay'),
    path('reserved_list/',ReservedAppointments_listView.as_view(), name='reserved_list'),
    path('pay/<int:appointment_id>/', pay_view.as_view(), name='pay'),
    path('verfy/', Verify_View.as_view(), name='verify'),
    path('all_days/', AllDaysAppointmentsView.as_view(), name='all_days_appointments'),
    path('day_appointments/<str:appointment_date>/', DayAppointmentsView.as_view(), name='day_appointments'),

]
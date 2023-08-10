from django.urls import path
from .views import SameInsuranceAppointmentsView
app_name='hesab'
urlpatterns = [
    #('daily-summary/', DailySummaryView.as_view(), name='daily_summary'),
    #path('monthly-summary/', MonthlySummaryView.as_view(), name='monthly_summary'),
    #path('yearly-summary/', YearlySummaryView.as_view(), name='yearly_summary'),
    path('sam/', SameInsuranceAppointmentsView.as_view(), name='sam'),
]

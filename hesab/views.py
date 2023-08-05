from django.shortcuts import render
from django.db.models import Sum
from datetime import datetime, timedelta
from django.views import View
from .models import Expense
from django.db.models import Count
from turn.models import Appointment
from account.models import patent
from django.contrib import messages
from datetime import date
from .forms import bime_form,bimepatent_form
class SameInsuranceAppointmentsView(View):
    form_class=bime_form
    def get(self, request,):
        form = self.form_class()
        form1=bimepatent_form
        return render(request, 'same_insurance_appointments.html',{'form':form,'form1':form1})
    def post(self,request):
        form = self.form_class(request.POST)
        form1=bimepatent_form(request.POST)
        if form.is_valid():
            if form1.is_valid():
               try:
                    typebime1 = form1.cleaned_data['typebime']
                    start_date = form.cleaned_data['start_date']
                    end_date = form.cleaned_data['end_date']
                    matching_patents = patent.objects.get(typebime=typebime1)

                    appointments = Appointment.objects.filter(patent=matching_patents, start_date__gte=start_date,
                                                      end_date__lte=end_date)
                    appointmentsall = Appointment.objects.filter( start_date__gte=start_date,
                                                              end_date__lte=end_date,payment=True)
                    expense_count_all=appointmentsall.count()
                    expense_count = appointments.count()
                    return render(request, 'same_insurance_appointments.html',
                            {'appointments': appointments, 'patent': matching_patents, 'expence': expense_count,'form':form,'form1':form1,'expense_count_all':expense_count_all})


               except patent.DoesNotExist:
                    messages.ERROR(request, 'موردی با مشخصات داده شده وجود ندارد.')



class DailySummaryView(View):
    def get(self, request):
        today = datetime.now().date()
        daily_total = Expense.objects.filter(date=today).aggregate(total=Sum('price'))['total'] or 0
        context = {
            'daily_total': daily_total,
        }

        return render(request, 'daily_summary.html', context)


class MonthlySummaryView(View):
    def get(self, request):
        today = datetime.now().date()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = first_day_of_month + timedelta(days=31)
        monthly_total = Expense.objects.filter(date__range=[first_day_of_month, last_day_of_month]).aggregate(total=Sum('price'))['total'] or 0

        context = {
            'monthly_total': monthly_total,
        }

        return render(request, 'monthly_summary.html', context)


class YearlySummaryView(View):
    def get(self, request):
        today = datetime.now().date()
        first_day_of_year = today.replace(month=1, day=1)
        last_day_of_year = first_day_of_year.replace(month=12, day=31)
        yearly_total = Expense.objects.filter(date__range=[first_day_of_year, last_day_of_year]).aggregate(total=Sum('price'))['total'] or 0

        context = {
            'yearly_total': yearly_total,
        }
        return render(request, 'yearly_summary.html', context)

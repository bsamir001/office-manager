from django.shortcuts import render,redirect
from django.views import View
from .models import Doctor, Appointment
from datetime import datetime, timedelta
from .forms import DoctorDelayForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class CreateAppointmentsView(View):
    def get(self, request):
        doctors = Doctor.objects.all()
        return render(request, 'create_appointment.html', {'doctors': doctors})

    def post(self, request):
        doctor_id = request.POST.get('doctor')
        start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d').date()
        start_time = datetime.strptime(request.POST.get('start_time'), '%H:%M').time()
        end_time = datetime.strptime(request.POST.get('end_time'), '%H:%M').time()

        doctor = Doctor.objects.get(id=doctor_id)
        doctor.create_appointments(start_date, end_date, start_time, end_time)

        return render(request, 'appointment_success.html')

@method_decorator(login_required, name='dispatch')
class ReserveAppointmentView(View):
    def get(self, request):
        appointments = Appointment.objects.filter(is_reserved=False)

        return render(request, 'reserved_appointments.html', {'appointments': appointments})

    def post(self, request):
        appointment_id = request.POST.get('appointment_id')
        print(appointment_id)
        appointment = Appointment.objects.get(id=appointment_id)
        appointment.user = request.user
        print(appointment.user)
        appointment.is_reserved = True
        appointment.save()
        return redirect('turn:reserved_appointments')

class doctor_delay_view(View):
    def get(self, request):
        form = DoctorDelayForm()
        return render(request, 'doctor_delay.html', {'form': form})

    def post(self, request):
        form = DoctorDelayForm(request.POST)
        if form.is_valid():
            delay_time = form.cleaned_data['delay_time']
            appointments = Appointment.objects.filter(doctor=request.user)
            for appointment in appointments:
                appointment.start_time += timedelta(minutes=delay_time)
                appointment.end_time += timedelta(minutes=delay_time)
                appointment.save()
            return redirect('turn:reserved_appointments')
        return render(request, 'doctor_delay.html', {'form': form})

class ReservedAppointments_listView(View):
    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(is_reserved=True)
        return render(request, 'reserved_appoint_list.html', {'appointments': appointments})

from django.shortcuts import render,redirect
from django.views import View
from rest_framework.response import Response
from .models import Doctor, Appointment
from datetime import datetime, timedelta,date
from rest_framework import status
from .forms import DoctorDelayForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
import requests
import json
from django.shortcuts import get_object_or_404
from account.models import patent
from rest_framework.views import APIView
from .serializers import AppointmentSerializer,DoctorSerializer
class CreateAppointmentsView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)  # سریالیزه کردن کوئری‌ست
        return Response(serializer.data)

    def post(self, request):
        doctor_name = request.data.get('doctor')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        print(start_date)
        if start_date is None or end_date is None or start_time is None or end_time is None:
            return Response({'message': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(name=doctor_name)
        except Doctor.DoesNotExist:
            return Response({'message': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time, '%H:%M').time()
            end_time = datetime.strptime(end_time, '%H:%M').time()
        except ValueError:
            return Response({'message': 'Invalid date or time format'}, status=status.HTTP_400_BAD_REQUEST)

        doctor.create_appointments(start_date, end_date, start_time, end_time)
        return Response({'message': 'Appointments created successfully'}, status=status.HTTP_201_CREATED)
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

class ReservedAppointments_listView(APIView):
    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(is_reserved=True)
        serializer = AppointmentSerializer(appointments, many=True)  # سریالیزه کردن کوئری‌ست
        return Response(serializer.data)
#######################################################################################################
# ? sandbox merchant
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"

amount = 95000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = 'YOUR_PHONE_NUMBER'  # Optional

CallbackURL = 'http://127.0.0.1:8080/verify/'
class pay_view(View):
    def get(self, request, appointment_id):
        appointment = Appointment.objects.get(id=appointment_id)
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Description": description,
            "Phone": phone,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        req = requests.Request('POST', ZP_API_REQUEST, data=data, headers={'content-type': 'application/json'})
        prepared_req = req.prepare()
        try:
            response = requests.Session().send(prepared_req, timeout=10)
            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    appointment.user = request.user
                    appointment.is_reserved=True
                    appointment.patent=get_object_or_404(patent, user=request.user)
                    appointment.save()
                    return redirect(ZP_API_STARTPAY + str(response_data['Authority']))
                else:
                    return render(request, 'error.html', {'message': 'Payment request failed'})
            return render(request, 'error.html', {'message': 'Unknown error occurred'})

        except requests.exceptions.Timeout:
            return render(request, 'error.html', {'message': 'Payment request timed out'})
        except requests.exceptions.ConnectionError:
            return render(request, 'error.html', {'message': 'Connection error occurred'})
class Verify_View(View):
    def get(self, request):
        authority = request.GET.get('Authority')
        if authority:
            verification_result = self.verify(authority)
            if verification_result['status']:
                return render(request, 'success.html', {'ref_id': verification_result['RefID']})
            else:
                return render(request, 'error.html', {'message': 'Payment verification failed'})
        else:
            return render(request, 'error.html', {'message': 'Invalid payment request'})

    def verify(self, authority):

        data = {
            "MerchantID": settings.MERCHANT,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data['Status'] == 100:
                return {'status': True, 'RefID': response_data['RefID']}
            else:
                return {'status': False, 'code': str(response_data['Status'])}
        return {'status': False, 'code': 'Unknown error occurred'}
#####################################################
class AllDaysAppointmentsView(APIView):
    def get(self, request):
        today = date(2023,6, 29)
        all_days = [today + timedelta(days=i) for i in range(30)]
        return Response({'all_days': all_days})

class DayAppointmentsView(APIView):
    def get(self, request, appointment_date):
        appointments = Appointment.objects.filter(start_date=appointment_date, is_reserved=False)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request,appointment_date):
        appointment_id = request.data.get('appointment_id')
        try:
            appointment = Appointment.objects.get(id=appointment_id, is_reserved=False)
        except Appointment.DoesNotExist:
            return Response({'message': 'Appointment not found or already reserved'}, status=status.HTTP_404_NOT_FOUND)

        if appointment.is_reserved:
            return Response({'message': 'Appointment is already reserved'}, status=status.HTTP_400_BAD_REQUEST)
        payment_url = reverse('turn:pay', args=[appointment.id])

        return Response({'message': 'Appointment reserved successfully', 'payment_url': payment_url},
                        status=status.HTTP_200_OK)












from django.shortcuts import render, get_object_or_404, HttpResponse
from account.models import User, patent
from turn.models import Appointment
from .forms import InfoForm
from django.views import View
from manager.models import Backup
from django.db import models


class ShowFormView(View):

    def get(self, request):
        users = User.objects.all().order_by('phone_number')
        appointments = Appointment.objects.filter(is_reserved=True).order_by('-start_time')
        return render(request, 'manager/users.html', {'users': users, 'appointments': appointments})


    def pos(self, request):
        pass


class ShowInfoForm(View):
    form = InfoForm

    def get(self, request, phone_number):
        user = get_object_or_404(User, phone_number=phone_number)
        user_patent = patent.objects.get(user=user)
        user_appointment = Appointment.objects.get(user=user)
        payment = user_appointment.payment
        user_presence = user_appointment.user_presence
        form = self.form(initial={
            'user_firstname': user_patent.firstname,
            'user_lastname': user_patent.lastname,
            'start_time': user_appointment.start_time,
            'user_phone_number': user_patent.user,
            'user_codeID': user_patent.codeID,
            'user_presence': user_presence,
            'payment': payment,
        })
        return render(request, 'manager/info.html', {'form': form, "user_patent": user_patent})

    def post(self, request, phone_number):
        form = self.form(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, phone_number=phone_number)
            user_patent = patent.objects.get(user=user)
            cd = {
                'user_phone_number': form.cleaned_data['user_phone_number'],
                'payment': form.cleaned_data['payment'],
                'user_filing': form.cleaned_data['user_filing'],
                'user_presence': form.cleaned_data['user_presence'],
                'user_code_id': form.cleaned_data['user_codeID'],
                'user_firstname': form.cleaned_data['user_firstname'],
                'user_lastname': form.cleaned_data['user_lastname'],
                'user_start_time': form.cleaned_data['start_time'],
            }
            backup_user, created = Backup.objects.get_or_create(
                user=user,
                defaults={
                    'filing': cd['user_filing'],
                    'codeID': cd['user_code_id'],
                    'firstname': cd['user_firstname'],
                    'lastname': cd['user_lastname'],
                    'start_time': cd['user_start_time'],
                }
            )
            if not created:
                backup_user.filing = cd['user_filing']
                backup_user.codeID = cd['user_code_id']
                backup_user.firstname = cd['user_firstname']
                backup_user.lastname = cd['user_lastname']
                backup_user.start_time = cd['user_start_time']
                backup_user.save()

            user_appointment = Appointment.objects.filter(user=user)
            user_appointment.update(payment=cd['payment'], user_presence=cd['user_presence'])
            return HttpResponse("your form send successfully")
        else:
            return HttpResponse("field")

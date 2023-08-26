from django.db import models
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from account.models import patent


# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def create_appointments(self, start_date, end_date, start_time, end_time):
        current_date = start_date
        current_time = datetime.combine(datetime.min.date(), start_time)

        while current_date <= end_date:
            while current_time.time() < end_time:
                appointment_start = datetime.combine(current_date, current_time.time())
                appointment_end = appointment_start + timedelta(minutes=20)
                appointment = Appointment(doctor=self, start_date=current_date, end_date=current_date,
                                          start_time=appointment_start.time(), end_time=appointment_end.time())
                appointment.save()
                current_time += timedelta(minutes=20)

            current_date += timedelta(days=1)
            current_time = datetime.combine(datetime.min.date(), start_time)


class Appointment(models.Model):
    patent = models.ForeignKey(patent, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_reserved = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    user_presence = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment with {self.doctor} from {self.start_date} {self.start_time} to {self.end_date} {self.end_time}"




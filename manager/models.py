from django.db import models
from account.models import User


# Create your models here.


class Backup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    filing = models.CharField(max_length=255)
    codeID = models.CharField(max_length=11, )
    firstname = models.CharField(max_length=11, )
    lastname = models.CharField(max_length=11, )
    start_time = models.TimeField()

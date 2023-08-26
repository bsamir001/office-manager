from django.db import models

# Create your models here.



class Expense(models.Model):
    name=models.CharField(max_length=20,)
    data=models.DateField()
    price=models.IntegerField()
    descraptions=models.TextField()
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from .managers import UserManager
from django.contrib.auth.models import Permission


# Create your models here.
class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=25, unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = True

    USERNAME_FIELD = 'phone_number'  # unique must be True #this field is for authenticate by email or username or ...
    objects = UserManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otpcode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code}- {self.created}'


class patent(models.Model):
    my_choices_bime = [
        #1:save to database , #2 show to user
        ('tamin_ejtemaee ', 'تامین اجتماعی'),
        ('farhanghi ', ' فرهنگی'),
        ('azad', 'آزاد')
    ]
    my_choices_info = [
        ('picture', 'option1'),
        ('test', 'option2'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    codeID = models.CharField(max_length=11, )
    firstname = models.CharField(max_length=11, )
    lastname = models.CharField(max_length=11, )
    typebime = models.CharField(max_length=20, choices=my_choices_bime)
    infopatent = models.CharField(max_length=20, choices=my_choices_info, )
    typeSickness = models.CharField(max_length=11, )
    age = models.CharField(max_length=10, )
    textSickness = models.TextField()


from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number):#password
        if not phone_number:
            raise ValueError("you have is must phone_number")
        user = self.model(phone_number=phone_number)
        #user.set_password(password)
        user.save(using=self._db)
        return user
    def create_usersuper(self, phone_number,password):
        if not phone_number:
            raise ValueError("you have is must phone_number")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number,password):#password
        user = self.create_usersuper(phone_number,password)#password
        user.is_admin = True
        user.save(using=self._db)
        return user


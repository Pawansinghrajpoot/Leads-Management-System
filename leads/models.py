from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_master=False):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_master = is_master
        user.save(using=self._db)
        return user

    def create_master(self, email, password):
        return self.create_user(email, password, is_master=True)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_master = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

class Lead(models.Model):
    name = models.CharField(max_length=255)
    number = models.CharField(max_length=10)
    database = models.CharField(max_length=255)
    demo_lecture_attended = models.BooleanField(default=False)
    interested_in = models.CharField(max_length=255, default='Not Specified')
    last_whatsapp_blast = models.DateTimeField(null=True, blank=True)
    response_to_whatsapp_blast = models.TextField(null=True, blank=True)
    last_call_date = models.DateField(null=True, blank=True)
    followup_of_last_call = models.DateField(null=True, blank=True)
    close_reason = models.TextField(null=True, blank=True)
    call_made = models.BooleanField(default=False)

    def __str__(self):
        return self.name

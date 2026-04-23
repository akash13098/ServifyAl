from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')

        # provide default values if missing
        extra_fields.setdefault('phone', '0000000000')
        extra_fields.setdefault('name', 'Admin')

        return self.create_user(email, password, **extra_fields)
# ////////////////////////////////////////////////////////////////////


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('PROVIDER', 'Provider'),
        ('USER', 'User'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(null=True, blank=True)

    # location (for future live tracking)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']

    objects = UserManager()

    def __str__(self):
        return self.email
    



class ProviderApplication(models.Model):

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    service_type = models.CharField(max_length=100)
    experience = models.IntegerField()

    # professional fields
    skills = models.TextField()
    available = models.BooleanField(default=True)

    # status system (important upgrade)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email    






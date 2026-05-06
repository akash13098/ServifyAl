from django.db import models
from accounts.models import User
from services.models import ServiceCategory

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)

    is_available = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.email
    
class ProviderLocation(models.Model):
    provider = models.OneToOneField(Provider, on_delete=models.CASCADE)

    latitude = models.FloatField()
    longitude = models.FloatField()

    address = models.TextField()
    
    
class ProviderService(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

    price = models.FloatField()
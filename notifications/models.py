from django.db import models
from accounts.models import User

class Notification(models.Model):

    TYPE_CHOICES = (
        ('booking', 'Booking'),
        ('system', 'System'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    message = models.TextField()

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
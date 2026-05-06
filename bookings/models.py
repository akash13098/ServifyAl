from django.db import models
from accounts.models import User
from providers.models import Provider, ProviderService

class Booking(models.Model):

    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service = models.ForeignKey(ProviderService, on_delete=models.CASCADE)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')

    scheduled_time = models.DateTimeField()
    address = models.TextField()

    price = models.FloatField()
    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    rating = models.IntegerField()  # 1 to 5
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
class Payment(models.Model):
    
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    razorpay_order_id = models.CharField(max_length=255)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)

    amount = models.FloatField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    created_at = models.DateTimeField(auto_now_add=True)
    
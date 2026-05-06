from .models import Provider
from django.db.models import Avg
from bookings.models import Review

def create_provider(user, data):
    provider = Provider.objects.create(user=user, **data)
    return provider


def update_provider_rating(provider):

    avg_rating = Review.objects.filter(
        provider=provider
    ).aggregate(avg=Avg('rating'))['avg']

    provider.rating = avg_rating or 0
    provider.save()
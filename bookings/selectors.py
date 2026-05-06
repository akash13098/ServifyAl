from .models import Booking

def is_provider_available(provider, scheduled_time):
    return not Booking.objects.filter(
        provider=provider,
        scheduled_time=scheduled_time,
        status__in=['accepted', 'in_progress']
    ).exists()
from rest_framework.exceptions import ValidationError
from .models import Booking
from .selectors import is_provider_available
from .models import Review
from providers.services import update_provider_rating
from notifications.tasks import send_booking_notification
# import razorpay
from django.conf import settings
from .models import Booking, Payment

def create_booking(user, provider, service, scheduled_time, address):

    if not is_provider_available(provider, scheduled_time):
        raise ValidationError("Provider not available at this time")

    booking = Booking.objects.create(
        user=user,
        provider=provider,
        service=service,
        scheduled_time=scheduled_time,
        address=address,
        price=service.price
    )

    return booking

def accept_booking(booking, provider):
    
    if booking.provider != provider:
        raise ValidationError("Unauthorized")

    if booking.status != 'requested':
        raise ValidationError("Invalid state transition")

    booking.status = 'accepted'
    booking.save()

    return booking

def start_service(booking, provider):
    
    if booking.provider != provider:
        raise ValidationError("Unauthorized")

    if booking.status != 'accepted':
        raise ValidationError("Cannot start service")

    booking.status = 'in_progress'
    booking.save()

    return booking

def complete_service(booking, provider):
    
    if booking.provider != provider:
        raise ValidationError("Unauthorized")

    if booking.status != 'in_progress':
        raise ValidationError("Cannot complete service")

    booking.status = 'completed'
    booking.save()

    return booking

def cancel_booking(booking, user):
    
    if booking.user != user:
        raise ValidationError("Unauthorized")

    if booking.status in ['completed']:
        raise ValidationError("Cannot cancel completed booking")

    booking.status = 'cancelled'
    booking.save()

    return booking


def create_review(booking, user, rating, comment):

    if booking.user != user:
        raise ValidationError("Unauthorized")

    if booking.status != 'completed':
        raise ValidationError("Cannot review incomplete booking")

    review = Review.objects.create(
        booking=booking,
        user=user,
        provider=booking.provider,
        rating=rating,
        comment=comment
    )

    # update provider rating
    update_provider_rating(booking.provider)

    return review



def create_booking(user, provider, service, scheduled_time, address):

    if not is_provider_available(provider, scheduled_time):
        raise ValidationError("Provider not available")

    booking = Booking.objects.create(
        user=user,
        provider=provider,
        service=service,
        scheduled_time=scheduled_time,
        address=address,
        price=service.price
    )

    # notify provider
    send_booking_notification(
        provider.user.id,
        "New Booking Request",
        "You have a new booking request"
    )

    return booking

def accept_booking(booking, provider):
    
    if booking.provider != provider:
        raise ValidationError("Unauthorized")

    if booking.status != 'requested':
        raise ValidationError("Invalid state")

    booking.status = 'accepted'
    booking.save()

    # notify user
    send_booking_notification(
        booking.user.id,
        "Booking Accepted",
        "Your service provider accepted the booking"
    )

    return booking


def complete_service(booking, provider):
    
    if booking.status != 'in_progress':
        raise ValidationError("Invalid state")

    booking.status = 'completed'
    booking.save()

    send_booking_notification(
        booking.user.id,
        "Service Completed",
        "Please rate your experience"
    )

    return booking



# client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))


def create_payment_order(booking):

    amount = int(booking.price * 100)  # convert to paisa

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    payment = Payment.objects.create(
        booking=booking,
        razorpay_order_id=order["id"],
        amount=booking.price
    )

    return payment

def verify_payment(payment, razorpay_payment_id):
    
    payment.razorpay_payment_id = razorpay_payment_id
    payment.status = 'paid'
    payment.save()

    # update booking
    booking = payment.booking
    booking.is_paid = True
    booking.save()
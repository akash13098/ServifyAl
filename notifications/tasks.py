# from celery import shared_task
# from .services import create_notification

# @shared_task
# def send_booking_notification(user_id, title, message):
#     from accounts.models import User

#     user = User.objects.get(id=user_id)

#     create_notification(user, title, message)
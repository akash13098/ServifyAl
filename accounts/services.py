from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import random
from django.utils import timezone
from datetime import timedelta
from .models import EmailOTP
# from .tasks import send_otp_email
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail
from .models import PendingUser
from .models import PendingUser, User

def generate_otp():
    return str(random.randint(100000, 999999))


def register_user(data):

    otp = generate_otp()

    pending_user = PendingUser.objects.create(
        email=data["email"],
        name=data["name"],
        password=data["password"],  # will hash later
        role=data["role"],
        otp=otp
    )

    return pending_user, otp

def login_user(email, password):
    user = authenticate(email=email, password=password)

    if not user:
        raise AuthenticationFailed("Invalid credentials")

    if not user.is_verified:
        raise AuthenticationFailed("Account not verified")

    return user

def create_email_otp(email):
    otp = generate_otp()

    expires_at = timezone.now() + timedelta(minutes=10)

    EmailOTP.objects.create(
        email=email,
        otp=otp,
        expires_at=expires_at
    )

    return otp

def send_otp_to_email(email):
    otp = create_email_otp(email)

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP is {otp}",
        from_email="noreply@servifyai.com",
        recipient_list=[email],
    )
    


def verify_otp_and_create_user(email, otp):

    pending_user = PendingUser.objects.filter(email=email).last()

    if not pending_user:
        raise ValidationError("No registration found")

    if pending_user.otp != otp:
        raise ValidationError("Invalid OTP")

    # create real user
    user = User.objects.create_user(
        email=pending_user.email,
        name=pending_user.name,
        password=pending_user.password,
        role=pending_user.role
    )

    user.is_verified = True
    user.save()

    # delete pending user
    pending_user.delete()

    return user
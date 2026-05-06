from django.urls import path
from .views import RegisterAPIView

from .views import RegisterAPIView, VerifyOTPAPIView, LoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('verify-otp/', VerifyOTPAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
]
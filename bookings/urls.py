from django.urls import path
from .views import *

urlpatterns = [
    path('create/', CreateBookingAPIView.as_view()),
    path('<int:booking_id>/accept/', AcceptBookingAPIView.as_view()),
    path('<int:booking_id>/start/', StartServiceAPIView.as_view()),
    path('<int:booking_id>/complete/', CompleteServiceAPIView.as_view()),
    path('<int:booking_id>/cancel/', CancelBookingAPIView.as_view()),
]
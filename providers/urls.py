from django.urls import path
from .views import NearbyProvidersAPIView

urlpatterns = [
    path('nearby/', NearbyProvidersAPIView.as_view()),
]